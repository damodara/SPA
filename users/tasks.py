from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def deactivate_inactive_users() -> None:
    """
    Блокирует пользователей, которые не заходили более месяца.
    Использует поля last_login и is_active.
    """
    now = timezone.now()
    border_date = now - timedelta(days=30)

    users_to_deactivate = User.objects.filter(
        is_active=True, last_login__lt=border_date
    )
    users_to_deactivate.update(is_active=False)
