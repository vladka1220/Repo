from django.core.exceptions import ValidationError
import re
import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _
from .validators import PersonalQualityValidator, ProfileValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Profile(models.Model):
    """
    Класс профиля пользователя
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=150, blank=True, unique=True)
    first_name = models.CharField(max_length=30, blank=True, validators=[ProfileValidator.validate_name])
    last_name = models.CharField(max_length=30, blank=True, validators=[ProfileValidator.validate_name])
    tg_nick = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    date_of_birth = models.CharField(max_length=10, blank=True, validators=[ProfileValidator.validate_date_format])
    gender = models.CharField(max_length=10, blank=True, validators=[ProfileValidator.validate_gender])
    location = models.CharField(max_length=50, blank=True, validators=[ProfileValidator.validate_location])
    phone = models.CharField(max_length=20, blank=True)
    token = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        # Удаление лишних пробелов перед сохранением
        self.first_name = re.sub(r'\s+', ' ', self.first_name.strip())
        self.last_name = re.sub(r'\s+', ' ', self.last_name.strip())
        self.location = re.sub(r'\s+', ' ', self.location.strip())
        super().save(*args, **kwargs)


def user_avatar_directory_path(instance: "UserAvatar", filename: str) -> str:
    """
    Генерация пути к файлу аватара пользователя
    """
    return f"avatars/{instance.user.pk}/{filename}"


class UserAvatar(models.Model):
    """
    Класс аватара пользователя
    """
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='avatar')
    avatar = models.ImageField(
        upload_to=user_avatar_directory_path,
        default=settings.DEFAULT_AVATAR_URL  # Используем URL из настроек
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete_old_avatar(self):
        if self.avatar and self.avatar.name != settings.DEFAULT_AVATAR_URL:
            storage = self.avatar.storage
            if storage.exists(self.avatar.name):
                storage.delete(self.avatar.name)


class UserSpecialization(models.Model):
    """
    Класс специализации пользователя
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='specializations')
    specialization = models.CharField(
        max_length=100,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[а-яА-Яa-zA-Z\s]+$',
                message='Специализация может содержать только кириллицу, латиницу и пробелы.'
            )
        ]
    )

    def save(self, *args, **kwargs):
        # Проверка на количество специализаций только при создании
        if not self.pk and self.user.specializations.count() >= 3:
            raise ValidationError("Пользователь не может иметь более 3 специализаций.")
        super().save(*args, **kwargs)


class PersonalQuality(models.Model):
    """
    Класс личных качеств пользователя, "о себе"
    """
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='personal_quality')
    quality = models.TextField(max_length=150, blank=True, validators=[PersonalQualityValidator.validate_quality])
    link = models.URLField(max_length=200, blank=True, validators=[PersonalQualityValidator.validate_portfolio_link])

    def save(self, *args, **kwargs):
        # Экранирование спецсимволов в тексте
        self.quality = escape(self.quality)
        super().save(*args, **kwargs)


class PlaceOfWorkUser(models.Model):
    """
    Класс места работы пользователя
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='place_of_work')
    company = models.TextField(max_length=25, blank=True)
    position = models.TextField(max_length=25, blank=True)
    work_period = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}$|^\d{2}\.\d{2}\.\d{4}-Настоящее время$',
                message='Период работы должен быть в формате "дд.мм.гггг-дд.мм.гггг" или "дд.мм.гггг-Настоящее время".'
            )
        ],
        help_text='Формат: "дд.мм.гггг-дд.мм.гггг" или "дд.мм.гггг-Настоящее время"'
    )

    def save(self, *args, **kwargs):
        if not self.pk and self.user.place_of_work.count() >= 3:
            raise ValidationError("Пользователь не может иметь более 3 мест работы.")
        super().save(*args, **kwargs)


class EducationUser(models.Model):
    """
    Класс образования пользователя
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    college = models.TextField(max_length=500, blank=True)
    speciality = models.TextField(max_length=500, blank=True)
    year_of_study = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}$|^\d{2}\.\d{2}\.\d{4}-Настоящее время$',
                message='Период учебы должен быть в формате "дд.мм.гггг-дд.мм.гггг" или "дд.мм.гггг-Настоящее время".'
            )
        ],
        help_text='Формат: "дд.мм.гггг-дд.мм.гггг" или "дд.мм.гггг-Настоящее время"'
    )
    link = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and self.user.education.count() >= 3:
            raise ValidationError("Пользователь не может иметь более 3 образований.")
        super().save(*args, **kwargs)


class UserSkill(models.Model):
    """
    Класс навыков пользователя, ключевые и технические
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    skill_type = models.CharField(
        max_length=20,
        choices=[
            ('key', 'Ключевые'),
            ('technical', 'Технические')
        ]
    )
