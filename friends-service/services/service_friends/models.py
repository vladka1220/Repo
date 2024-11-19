from django.contrib.auth.models import User
from django.db import models
import uuid


class Friend(models.Model):
    """
    Модель для хранения информации о друзьях.
    """

    user = models.UUIDField(default=uuid.uuid4)
    friend = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "friend")


class FriendRequest(models.Model):
    """
    Модель для хранения запросов на добавление в друзья.
    """

    from_user = models.UUIDField(default=uuid.uuid4)
    to_user = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)  # Статус запроса

    class Meta:
        unique_together = (
            "from_user",
            "to_user",
        )


class FavoriteUser(models.Model):
    """
    Модель для хранения избранных пользователей.
    """

    user = models.UUIDField(default=uuid.uuid4)
    favorite = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "favorite",
        )


class UserProfile(models.Model):
    """
    Модель для хранения информации о профиле пользователя.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    is_mentor = models.BooleanField(
        default=False
    )
    rating = models.FloatField(default=0.0)
