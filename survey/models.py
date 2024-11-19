"""
Файл моделей опроса

Модели:
    - Survey, имеет связь с моделью Question один ко многим и имеет поля:
        - title
        - description
    - Question, имеет связь с моделью Answer один ко многим и имеет поля:
        - nameTitleQuestion
        - survey, связь с моделью Survey
    - Answer, имеет связь с моделью Choice один ко многим и имеет поля:
        - text
        - question, связь с моделью Question
    - Choice, имеет связь с моделью Answer один ко многим и имеет поля:
        - text
        - answer, связь с моделью Answer
"""
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Survey(models.Model):
    """
    Модель опроса
    """
    title = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    language = models.CharField(max_length=3, null=True, default='RU')

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['id']
        db_table = 'survey_survey'

    def __str__(self):
        return f'Survey=(id: {self.id}, {self.title})'


class Question(models.Model):
    """
    Модель вопроса
    """
    nameTitleQuestion = models.CharField(max_length=255, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['id']
        db_table = 'survey_question'

    def __str__(self):
        return f'Question=(id: {self.id}, {self.nameTitleQuestion})'


class Answer(models.Model):
    """
    Модель ответа
    """
    text = models.CharField(max_length=255, blank=True, null=True)
    other = ArrayField(models.TextField(max_length=3000), blank=True, null=True)
    count = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['id']
        db_table = 'survey_answer'

    def __str__(self):
        return f'Answer=(id: {self.id}, {self.text})'


class Choice(models.Model):
    """
    Модель выбора
    """
    text = models.CharField(max_length=255, null=True)
    count = models.IntegerField(default=0)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='choices')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        ordering = ['id']
        db_table = 'survey_choice'

    def __str__(self):
        return f'Choice=(id: {self.id}, {self.text})'


class Contact(models.Model):
    """
    Модель контактов, хранящая списки email и telegram контакты
    """
    email_list = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    telegram_list = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    language = models.CharField(max_length=3, null=True, default='RU')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['id']
        db_table = 'survey_contact'

    def __str__(self):
        return f'Contacts=(id: {self.id}'
