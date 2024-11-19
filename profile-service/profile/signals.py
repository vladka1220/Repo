from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile, UserAvatar

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Создаем профиль пользователя с дополнительными данными
        profile = Profile.objects.create(
            user=instance,
            id=instance.id,
            username=instance.username,
            email=instance.email,
            first_name=instance.first_name
        )

        # Создаем аватар по умолчанию
        UserAvatar.objects.create(user=profile, avatar='uploads/default.jpg')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
