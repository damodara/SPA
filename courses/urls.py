from django.urls import path
from rest_framework.routers import SimpleRouter

from courses.apps import CoursesConfig
from courses.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    SubscriptionAPIView,
)

app_name = CoursesConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
]

# Добавляем маршруты ViewSet
urlpatterns += router.urls
