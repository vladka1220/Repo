"""
Модуль сериализаторов (для отображения в swagger)

Функции:
    - ChoiceSerializer: сериализатор для отображения choice в swagger
    - AnswerSerializer: сериализатор для отображения answer в swagger
    - QuestionSerializer: сериализатор для отображения question в swagger
    - SurveySerializer: сериализатор для отображения survey в swagger
    - ChoiceRequestSerializer: сериализатор для отображения choice в swagger
    - AnswerRequestSerializer: сериализатор для отображения answer в swagger
    - QuestionRequestSerializer: сериализатор для отображения question в swagger

Модели:
    - Choice
    - Answer
    - Question
    - Survey

"""
from rest_framework import serializers

from .models import Survey, Question, Answer, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'count']


class AnswerSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Answer
        fields = ['text', 'count', 'other', 'choices']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['nameTitleQuestion', 'answers']


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['questions', 'language']


class ChoiceRequestSerializer(serializers.Serializer):
    text = serializers.CharField()


class AnswerRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
    choices = serializers.ListField(
        child=ChoiceRequestSerializer(),
        required=False
    )
    other = serializers.CharField(required=False)


class QuestionRequestSerializer(serializers.Serializer):
    nameTitleQuestion = serializers.CharField()
    answers = serializers.ListField(
        child=AnswerRequestSerializer()
    )


class SurveyRequestSerializer(serializers.Serializer):
    questions = serializers.ListField(
        child=QuestionRequestSerializer()
    )
    language = serializers.CharField()


class ContactDataSerializer(serializers.Serializer):
    email = serializers.EmailField()
    telegram = serializers.CharField(default='@example')


class ContactRequestSerializer(serializers.Serializer):
    modal = serializers.ListField(
        child=ContactDataSerializer()
    )
    language = serializers.CharField(default='RU')
