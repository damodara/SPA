from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['video_url'] = instance.video_link
        return data


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
