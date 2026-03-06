from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson, Subscription

User = get_user_model()


class CoursesTestCase(APITestCase):
    def setUp(self):
        # Создаём пользователей ТОЛЬКО с email и password
        self.user = User.objects.create_user(email="user@test.ru", password="test123")
        self.moderator = User.objects.create_user(
            email="moderator@test.ru", password="test123"
        )
        self.owner = User.objects.create_user(email="owner@test.ru", password="test123")

        # Добавляем модератора в группу
        from django.contrib.auth.models import Group

        group, created = Group.objects.get_or_create(name="moderators")
        self.moderator.groups.add(group)

        # Создаём курс и урок
        self.course = Course.objects.create(
            name="Тестовый курс", description="Описание курса", owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            name="Тестовый урок",
            description="Описание урока",
            video_link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            course=self.course,
            owner=self.owner,
        )

        # URL-адреса
        self.course_list_url = "/api/courses/"
        self.course_detail_url = f"/api/courses/{self.course.id}/"

        self.lesson_list_url = "/api/lessons/"
        self.lesson_create_url = "/api/lessons/create/"
        self.lesson_detail_url = f"/api/lessons/{self.lesson.id}/"
        self.lesson_update_url = f"/api/lessons/{self.lesson.id}/update/"
        self.lesson_delete_url = f"/api/lessons/{self.lesson.id}/delete/"

        self.subscription_url = "/api/subscription/"

    # --- Тесты ---

    def test_lesson_create_by_owner(self):
        """Проверка создания урока владельцем."""
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Новый урок",
            "description": "Описание",
            "video_link": "https://www.youtube.com/watch?v=abc123",
            "course": self.course.id,
        }
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_by_moderator_denied(self):
        """Модератор не может создавать уроки."""
        self.client.force_authenticate(user=self.moderator)
        data = {
            "name": "Урок от модератора",
            "course": self.course.id,
            "video_link": "https://www.youtube.com/watch?v=abc123",
        }
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_by_owner(self):
        """Владелец может редактировать свой урок."""
        self.client.force_authenticate(user=self.owner)
        data = {"name": "Обновлённый урок"}
        response = self.client.patch(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Обновлённый урок")

    def test_lesson_update_by_moderator(self):
        """Модератор может редактировать любой урок."""
        self.client.force_authenticate(user=self.moderator)
        data = {"name": "Модератор обновил урок"}
        response = self.client.patch(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Модератор обновил урок")

    def test_lesson_update_by_other_user_denied(self):
        """Другой пользователь не может редактировать чужой урок."""
        self.client.force_authenticate(user=self.user)
        data = {"name": "Чужой урок"}
        response = self.client.patch(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_by_owner(self):
        """Владелец может удалить свой урок."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_delete_by_moderator_denied(self):
        """Модератор не может удалять уроки."""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list_access(self):
        """Пользователь видит только свои уроки, модератор — все."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(len(response.data["results"]), 1)

    def test_subscribe_to_course(self):
        """Пользователь может подписаться на курс."""
        self.client.force_authenticate(user=self.owner)
        data = {"course_id": self.course.id}
        response = self.client.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.owner, course=self.course).exists()
        )

    def test_unsubscribe_from_course(self):
        """Пользователь может отписаться от курса."""
        Subscription.objects.create(user=self.owner, course=self.course)
        self.client.force_authenticate(user=self.owner)
        data = {"course_id": self.course.id}
        response = self.client.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.owner, course=self.course).exists()
        )

    def test_is_subscribed_in_course_serializer(self):
        """Поле is_subscribed корректно отображается в сериализаторе курса."""
        Subscription.objects.create(user=self.owner, course=self.course)
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_subscribed"])

    def test_is_not_subscribed(self):
        """Поле is_subscribed = False, если нет подписки."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_subscribed"])
