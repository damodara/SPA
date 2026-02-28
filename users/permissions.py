from typing import Any

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from courses.models import Course, Lesson

User = get_user_model()


class IsModerator(BasePermission):
    """
    Пользователь состоит в группе модераторов.
    """

    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.groups.filter(name="moderators").exists()
        )

    def has_object_permission(self, request, view, obj) -> bool:
        return self.has_permission(request, view)


class IsOwner(BasePermission):
    """
    Пользователь является владельцем объекта (курса или урока).
    Для урока владельцем считается владелец связанного курса.
    """

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj: Any) -> bool:
        user = request.user

        owner = None
        if isinstance(obj, Course):
            owner = obj.owner
        elif isinstance(obj, Lesson):
            owner = getattr(obj.course, "owner", None)
        else:
            owner = getattr(obj, "owner", None)

        return owner == user
