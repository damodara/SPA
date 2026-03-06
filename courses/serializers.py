from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
from courses.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Урока (Lesson).

    Преобразует объекты модели Lesson в JSON и обратно.
    Обеспечивает валидацию поля video_url с помощью кастомного валидатора.

    Поля:
        video_url: URL-ссылка на видео, привязанная к полю video_link модели.
                   Допускает пустые значения, но при наличии — должна вести на YouTube.
    """

    video_link = serializers.URLField(
        validators=[validate_youtube_url],
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    class Meta:
        """
        Мета-настройки сериализатора.
        """

        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Курса (Course).

    Преобразует объекты модели Course в JSON.
    Добавляет дополнительные поля:
        - lessons_count: количество уроков в курсе.
        - is_subscribed: подписан ли текущий пользователь на курс.

    Используется в списке и детальном просмотре курсов.
    """

    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """
        Мета-настройки сериализатора.
        """

        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        """
        Возвращает количество уроков, связанных с курсом.

        Args:
            obj (Course): Экземпляр модели Course.

        Returns:
            int: Количество уроков в курсе.
        """
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
        Определяет, подписан ли текущий пользователь на данный курс.

        Если пользователь не авторизован — возвращает False.

        Args:
            obj (Course): Экземпляр модели Course.

        Returns:
            bool: True — если пользователь подписан, иначе False.
        """
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
