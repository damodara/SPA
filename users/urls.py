from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentViewSet,
    UserCreateAPIView,
    UserProfileDetailView,
    UserProfileUpdateView,
    UserViewSet,
)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("users", UserViewSet, basename="user")
router.register("payments", PaymentViewSet, basename="payment")

urlpatterns = router.urls + [
    path("profile/", UserProfileUpdateView.as_view(), name="profile-update"),
    path("profiles/<int:pk>/", UserProfileDetailView.as_view(), name="profile-detail"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
