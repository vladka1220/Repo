"""
Файл маршрутизации URL для приложения survey.
Этот модуль определяет URL-шаблоны для API-эндпоинтов, связанных с работой опроса.

Содержит роутеры для API, CRUD-эндпоинтов, таких как get, get_id, create, update, delete, put, patch:
    -survey:
    -question,
    -answer,
    -choice,

Содержит URL-шаблоны:
    -countsurvey: post запрос принимающий на вход для обработки опрос

"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SurveyViewSet,
    QuestionViewSet,
    AnswerViewSet,
    ChoiceViewSet,
    CountSurveyView,
    ContactView,
)

app_name = "survey"
routers = DefaultRouter()
routers.register("survey", SurveyViewSet, basename="survey")
# routers.register("question", QuestionViewSet, basename="question")
# routers.register("answer", AnswerViewSet, basename="answer")
# routers.register("choice", ChoiceViewSet, basename="choice")

urlpatterns = [
    path("api/", include(routers.urls)),
    path("ru/", CountSurveyView.as_view(), name="countsurvey"),
    path("en/", CountSurveyView.as_view(), name="countsurvey"),
    path("ru/contact/", ContactView.as_view(), name="contact"),
    path("en/contact/", ContactView.as_view(), name="contact"),
]
