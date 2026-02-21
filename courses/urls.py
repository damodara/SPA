from rest_framework.routers import SimpleRouter

from courses.apps import CoursesConfig
from courses.views import CourseViewSet

app_name = CoursesConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = []
urlpatterns += router.urls