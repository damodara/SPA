from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from courses.models import Course, Subscription


@shared_task
def send_course_update_email(course_id: int) -> None:
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return

    subscribers = Subscription.objects.filter(course=course).select_related("user")
    recipient_list = [sub.user.email for sub in subscribers if sub.user.email]
    if not recipient_list:
        return

    subject = f"Обновление материалов курса «{course.name}»"
    message = (
        f"Материалы курса «{course.name}» были обновлены.\n\n"
        "Зайдите в личный кабинет, чтобы посмотреть изменения."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=recipient_list,
        fail_silently=True,
    )
