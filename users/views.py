from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserProfileSerializer

class UserProfileUpdateView(UpdateAPIView):
    """
    API endpoint для редактирования профиля пользователя.
    Доступен только аутентифицированным пользователям.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user