from rest_framework import serializers

from courses.models import Course, Lesson
from courses.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        source='video_link',
        validators=[validate_youtube_url],
        required=False,
        allow_blank=True,
        allow_null=True
    )
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "preview",
            "owner",
            "lessons_count",
            "lessons",
        ]

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()
