from django.urls import path

from .apps import UsersConfig
from .views import UserProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('profile/', UserProfileUpdateView.as_view(), name='profile-update'),
]