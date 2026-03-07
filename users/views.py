from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import (PaymentSerializer, UserProfileSerializer,
                               UserPublicProfileSerializer, UserSerializer)
from users.services import (create_stripe_checkout_session,
                            create_stripe_price, create_stripe_product)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["payment_date"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.query_params.get("course")
        lesson_id = self.request.query_params.get("lesson")
        method = self.request.query_params.get("method")
        if course_id:
            qs = qs.filter(course_id=course_id)
        if lesson_id:
            qs = qs.filter(lesson_id=lesson_id)
        if method:
            qs = qs.filter(method=method)
        return qs

    def perform_create(self, serializer):
        """
        При создании платежа через API:
        - создаём продукт и цену в Stripe,
        - создаём checkout-сессию,
        - сохраняем ссылку и id сессии в Payment,
        - метод оплаты выставляем как 'card'.
        """
        payment: Payment = serializer.save(user=self.request.user, method="card")

        # Определяем название продукта
        if payment.course:
            product_name = f"Курс: {payment.course.name}"
        elif payment.lesson:
            product_name = f"Урок: {payment.lesson.name}"
        else:
            product_name = f"Оплата #{payment.pk}"

        # Создание объектов в Stripe
        product_id = create_stripe_product(product_name)
        price_id = create_stripe_price(product_id, payment.amount)

        # URL-ы для успешной / неуспешной оплаты
        request = self.request
        domain = request.build_absolute_uri("/").rstrip("/")
        success_url = f"{domain}/payments/success/"
        cancel_url = f"{domain}/payments/cancel/"

        session_data = create_stripe_checkout_session(price_id, success_url, cancel_url)

        payment.stripe_session_id = session_data["id"]
        payment.link = session_data["url"]
        payment.save(update_fields=["stripe_session_id", "link"])


class UserProfileUpdateView(UpdateAPIView):
    """
    API endpoint для редактирования профиля пользователя.
    Доступен только аутентифицированным пользователям.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileDetailView(RetrieveAPIView):
    """
    Просмотр профиля любого пользователя.
    Свой профиль — полная информация,
    чужой профиль — только общая (без фамилии, истории платежей и пароля).
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            serializer_class = UserProfileSerializer
        else:
            serializer_class = UserPublicProfileSerializer
        serializer = serializer_class(instance)
        return Response(serializer.data)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserViewSet(ModelViewSet):
    """
    Полный CRUD по пользователям.
    Доступен только администратору.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
