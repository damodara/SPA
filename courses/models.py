from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    preview = models.ImageField(
        upload_to="courses/image", verbose_name="Превью", blank=True, null=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс"
    )
    name = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    preview = models.ImageField(
        upload_to="courses/image", verbose_name="Превью", blank=True, null=True
    )
    video_link = models.URLField(
        unique=True, verbose_name="Ссылка на видео", blank=True, null=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Курс",
        related_name="lesson_set",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
