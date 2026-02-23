from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserProfileUpdateView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("payments", PaymentViewSet, basename="payment")

urlpatterns = router.urls + [
    path("profile/", UserProfileUpdateView.as_view(), name="profile-update"),
]
