from rest_framework.filters import OrderingFilter
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserProfileSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["payment_date"]

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


class UserProfileUpdateView(UpdateAPIView):
    """
    API endpoint для редактирования профиля пользователя.
    Доступен только аутентифицированным пользователям.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
