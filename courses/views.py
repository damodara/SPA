from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson, Subscription
from courses.paginators import CourseLessonPagination
from courses.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    """
    ViewSet для управления курсами.

    Предоставляет полный набор операций CRUD:
    - Создание, чтение, обновление, удаление курсов.
    - Пагинация результатов.
    - Разграничение прав доступа в зависимости от роли пользователя.

    Атрибуты:
        queryset (QuerySet): Все курсы с оптимизированными связями.
        serializer_class (CourseSerializer): Сериализатор для курсов.
        pagination_class (CourseLessonPagination): Пагинатор для постраничного вывода.
        permission_classes (list): Базовые права доступа — только авторизованные пользователи.
    """

    queryset = (
        Course.objects.all()
        .select_related("owner")
        .prefetch_related("lessons", "subscriptions")
        .order_by("id")
    )
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает queryset курсов в зависимости от прав пользователя.

        Логика:
            - Анонимные пользователи: пустой queryset.
            - Модераторы: видят все курсы.
            - Обычные пользователи: только свои курсы (по owner).

        Returns:
            QuerySet: Отфильтрованный набор курсов.
        """
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()
        if user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=user)

    def get_permissions(self):
        """
        Динамически назначает права доступа в зависимости от действия (action).

        Логика:
            - create: Только авторизованные и НЕ модераторы.
            - retrieve/update/partial_update: Модераторы или владельцы.
            - destroy: Только владельцы, не являющиеся модераторами.
            - list: Авторизованные пользователи (фильтрация в get_queryset).

        Returns:
            list: Список экземпляров классов разрешений.
        """
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ("retrieve", "update", "partial_update"):
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModerator, IsOwner]
        else:  # list и прочее
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """
        Выполняет дополнительные действия при создании курса.

        Привязывает текущего пользователя как владельца (owner) курса.

        Args:
            serializer (CourseSerializer): Сериализатор с валидированными данными.
        """
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(CreateAPIView):
    """
    APIView для создания урока.

    Только авторизованные пользователи, не являющиеся модераторами, могут создавать уроки.
    При создании урока автоматически устанавливается владелец.
    """

    queryset = Lesson.objects.all().select_related("owner", "course")
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """
        Привязывает текущего пользователя как владельца урока.

        Args:
            serializer (LessonSerializer): Сериализатор с валидированными данными.
        """
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(UpdateAPIView):
    """
    APIView для редактирования урока.

    Редактировать урок могут:
        - Владельцы урока.
        - Пользователи из группы модераторов.
    """

    queryset = Lesson.objects.all().select_related("owner", "course")
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    """
    APIView для удаления урока.

    Удалять урок могут только его владельцы, не являющиеся модераторами.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator, IsOwner]


class LessonListAPIView(ListAPIView):
    """
    APIView для получения списка уроков.

    Поддерживает пагинацию и фильтрацию по владельцу.
    Модераторы видят все уроки, обычные пользователи — только свои.
    """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPagination

    def get_queryset(self):
        """
        Возвращает queryset уроков в зависимости от прав пользователя.

        Логика:
            - Анонимные: пустой queryset.
            - Модераторы: все уроки.
            - Остальные: только уроки, принадлежащие пользователю.

        Returns:
            QuerySet: Отфильтрованный набор уроков.
        """
        qs = Lesson.objects.all().select_related("owner", "course").order_by("id")
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.none()
        if user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=user)


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    APIView для просмотра одного урока.

    Доступ разрешён владельцам урока или модераторам.
    """

    queryset = Lesson.objects.all().select_related("owner", "course")
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionAPIView(APIView):
    """
    APIView для управления подпиской пользователя на курс.

    POST-запрос переключает состояние подписки:
        - Если подписка есть — удаляет её.
        - Если нет — создаёт новую.

    Требует аутентификации.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для добавления или удаления подписки.

        Ожидает параметр `course_id` в теле запроса.

        Args:
            request (Request): Объект запроса DRF с данными и пользователем.

        Returns:
            Response: JSON-ответ с сообщением о результате операции.
                     Пример: {"message": "подписка добавлена"}
        """
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response({"error": "Требуется course_id"}, status=400)

        try:
            course_id = int(course_id)
        except (TypeError, ValueError):
            return Response({"error": "Некорректный формат course_id"}, status=400)

        course = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "подписка добавлена"

        return Response({"message": message})
