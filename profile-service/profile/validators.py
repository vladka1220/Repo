import re
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


# Валидация Profile
class ProfileValidator(models.Model):
    @staticmethod
    def validate_date_format(value):
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', value):
            raise ValidationError(_("Дата рождения должна быть в формате дд.мм.гггг."))

    def validate_name(value):
        # Удаление лишних пробелов
        value = re.sub(r'\s+', ' ', value.strip())
        # Проверка длины
        if not (2 <= len(value) <= 30):
            raise ValidationError(_("Имя должно содержать от 2 до 30 символов."))
        # Проверка допустимых символов
        if not re.match(r'^[a-zA-Zа-яА-Я\'-]+$', value):
            raise ValidationError(_("Имя может содержать только буквы, тире и апостроф."))

    def validate_location(value):
        # Удаление лишних пробелов
        value = re.sub(r'\s+', ' ', value.strip())
        # Проверка длины
        if not (2 <= len(value) <= 30):
            raise ValidationError(_("Локация должна содержать от 2 до 30 символов."))
        # Проверка допустимых символов
        if not re.match(r'^[a-zA-Zа-яА-Я\s,()-]+$', value):
            raise ValidationError(_("Локация может содержать только буквы, пробелы, запятые, скобки и тире."))

    def validate_gender(value):
        # Проверка длины
        if len(value) > 10:
            raise ValidationError(_("Пол может содержать до 10 символов."))
        # Проверка допустимых символов
        if not re.match(r'^[a-zA-Zа-яА-Я]+$', value):
            raise ValidationError(_("Пол может содержать только буквы."))


# Список проверенных доменов
ALLOWED_DOMAINS = [
    "github.com", "gitlab.com", "bitbucket.org", "linkedin.com", "behance.net",
    "dribbble.com", "portfoliobox.net", "deviantart.com", "carbonmade.com",
    "wix.com", "squarespace.com", "wordpress.com", "codepen.io", "jsfiddle.net",
    "dev.to", "hashnode.com", "visualcv.com", "tilda.cc", "cargo.site",
    "kaggle.com", "replit.com", "medium.com", "notion.so", "clippings.me",
    "dunked.com", "jekyllrb.com", "stackoverflow.com/story", "devfolio.co",
    "coroflot.com", "angel.co", "upwork.com", "freelancer.com", "toptal.com",
    "talent.hubstaff.com", "fiverr.com", "about.me", "krop.com", "the-dots.com",
    "coda.io", "designhill.com"

]


# Валидация PersonalQuality
class PersonalQualityValidator(models.Model):

    def validate_quality(value):
        # Регулярное выражение для проверки допустимых символов
        if not re.match(r'^[a-zA-Zа-яА-Я0-9\s.,:;\'"-]+$', value):
            # logger.warning(f"Подозрительная активность: {value}")
            raise ValidationError(_("Недопустимые символы в тексте."))

    def validate_portfolio_link(value):
        # Проверка домена в URL
        if not any(domain in value for domain in ALLOWED_DOMAINS):
            raise ValidationError(_("Повторите попытку, URL не входит в список проверенных."))
