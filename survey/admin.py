"""
Файл подключение моделей опроса в панели администратора.

Подключенные модели:
    - Survey
    - Question
    - Answer
    - Choice
"""
from django.contrib import admin

from .models import Survey, Question, Answer, Choice, Contact
from .admin_mixins import ExportAsCSVMixin


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    """
    Класс отображения "опросов" в админке
    """
    actions = ['export_csv']
    list_display = ('id', 'title', 'count')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Класс отображения "вопросов" в админке
    """
    list_display = ('id', 'text_short', 'survey')

    def text_short(self, obj):
        if len(obj.nameTitleQuestion) > 48:
            return obj.nameTitleQuestion[:48] + '...'
        return obj.nameTitleQuestion

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('survey')  # Подгружает связанные объекты: survey


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Класс отображения "ответов" в админке
    """
    list_display = ('id', 'count', 'text', 'other', 'question')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """
    Класс отображения "выборов" в админке
    """
    list_display = ('id', 'count', 'text', 'answer')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Класс отображения "контактов" в админке
    """
    list_display = ('id', 'email_list', 'telegram_list')
