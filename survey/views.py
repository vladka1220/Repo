from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.http import HttpRequest
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Survey, Question, Answer, Choice, Contact
from .serializers import (
    ContactRequestSerializer
)
from .serializers import QuestionSerializer, AnswerSerializer, ChoiceSerializer, SurveySerializer, \
    SurveyRequestSerializer
from .validators import validate_telegram_nick, validate_email_address


class ContactView(APIView):
    """
    APIView для обработки POST-запроса, принимающего список словарей с данными email и/или telegram,
    которые добавляются в список email_list и/или telegram_list соответственно.
    """

    @extend_schema(
        tags=['contact'],
        request=ContactRequestSerializer,
        responses={200: OpenApiExample('Success', value={'message': 'success'})}
    )
    @transaction.atomic
    def post(self, request: HttpRequest) -> Response:
        """
        Обрабатывает POST-запрос с данными email и/или telegram, которые добавляются в список email_list и/или
        telegram_list соответственно.

        Args:
            request (HttpRequest): HTTP запрос с данными email и/или telegram.

        Returns:
            Response: HTTP ответ с сообщением об успехе или ошибке.
        """
        contact_data_list = request.data.get('modal', [])
        language = request.data.get('language', 'RU').upper()

        # Проверка, что входные данные являются списком
        if not isinstance(contact_data_list, list):
            return Response({'message': 'Invalid data format, expected a list'}, status=400)

        # Инициализация списков для email и telegram
        email_list = []
        telegram_list = []

        for contact_data in contact_data_list:
            email = contact_data.get('email')
            telegram = contact_data.get('telegram')

            # Валидация email
            if email:
                try:
                    validate_email_address(email)
                    email_list.append(email)
                except ValidationError:
                    return Response({'message': f'Invalid email: {email}'}, status=400)

            # Валидация telegram
            if telegram:
                if not validate_telegram_nick(telegram):
                    return Response({'message': f'Invalid telegram: {telegram}'}, status=400)
                telegram_list.append(telegram)

        # Обновление модели Contact
        try:
            contact = Contact.objects.filter(language=language).first()
            if not contact:
                return Response({'message': 'Contact not found'}, status=404)

            if email_list:
                if contact.email_list is None:
                    contact.email_list = []
                contact.email_list.extend(email_list)

            if telegram_list:
                if contact.telegram_list is None:
                    contact.telegram_list = []
                contact.telegram_list.extend(telegram_list)

            contact.save()
        except Exception as e:
            return Response({'message': f'Error updating contact: {str(e)}'}, status=500)

        return Response({'message': 'success'})


class CountSurveyView(APIView):
    """
    APIView для подсчета ответов на вопросы опроса.
    """

    @extend_schema(
        tags=['countsurvey'],
        request=SurveyRequestSerializer,
        responses={200: OpenApiExample('Success', value={'message': 'success'})}
    )
    @transaction.atomic
    def post(self, request: HttpRequest) -> Response:
        """
        Обрабатывает POST-запрос для подсчета ответов на вопросы опроса.

        Args:
            request (HttpRequest): HTTP запрос с данными опроса.

        Returns:
            Response: HTTP ответ с сообщением об успехе или ошибке.
        """

        try:
            survey_data = request.data.get('questions', [])
            language = request.data.get('language', 'RU').upper()
            # Проверка, что входные данные являются списком
            if not isinstance(survey_data, list):
                return Response({'message': 'Invalid data format, expected a list'}, status=400)

            # Определение опроса в зависимости от языка
            survey = Survey.objects.filter(language=language).first()
            if not survey:
                return Response({'message': f'Survey with language {language} not found'}, status=404)

            for question_data in survey_data:
                question_text = question_data.get('nameTitleQuestion')
                question, created = Question.objects.get_or_create(nameTitleQuestion=question_text, survey=survey)

                for answer_data in question_data.get('answers', []):
                    other_text = answer_data.get('other')
                    if other_text is not None:
                        answer, created = Answer.objects.get_or_create(text='other', question=question)
                        if answer.other is None:
                            answer.other = []
                        answer.other.append(other_text)
                        answer.count += 1
                        # answers_to_update.append(answer)
                        answer.save()
                        continue
                    else:
                        answer_text = answer_data.get('text')
                        answer, created = Answer.objects.get_or_create(text=answer_text, question=question)
                        if not answer_data.get('choices'):
                            if created:
                                answer.count = 1
                            else:
                                answer.count += 1
                            answer.save()

                        else:
                            for choice_data in answer_data.get('choices', []):
                                choice_text = choice_data.get('text')
                                choice, created = Choice.objects.get_or_create(text=choice_text, answer=answer)
                                if created:
                                    choice.count = 1
                                else:
                                    choice.count += 1
                                choice.save()

            # Увеличение счетчика count опроса
            survey.count += 1
            survey.save()

        except Exception as e:
            return Response({'message': f'Error processing survey data: {str(e)}'}, status=500)

        return Response({'message': 'success'})


# class CountSurveyView(APIView):
#     """
#     APIView для подсчета ответов на вопросы опроса.
#     """
#
#     @extend_schema(
#         tags=['countsurvey'],
#         request=SurveyRequestSerializer,
#         responses={200: OpenApiExample('Success', value={'message': 'success'})}
#     )
#     @transaction.atomic
#     def post(self, request: HttpRequest) -> Response:
#         """
#         Обрабатывает POST-запрос для подсчета ответов на вопросы опроса.
#
#         Args:
#             request (HttpRequest): HTTP запрос с данными опроса.
#
#         Returns:
#             Response: HTTP ответ с сообщением об успехе или ошибке.
#         """
#
#         try:
#             survey_data = request.data.get('questions', [])
#             language = request.data.get('language', 'RU').upper()
#             # Проверка, что входные данные являются списком
#             if not isinstance(survey_data, list):
#                 return Response({'message': 'Invalid data format, expected a list'}, status=400)
#
#             # Создаем списки для создания новых записей и обновления существующих (не реализовано до конца)
#             questions_to_create = []
#             answers_to_create = []
#             choices_to_create = []
#             answers_to_update = []
#             choices_to_update = []
#
#             # Определение опроса в зависимости от языка
#             survey = Survey.objects.filter(language=language).first()
#             if not survey:
#                 return Response({'message': f'Survey with language {language} not found'}, status=404)
#
#             # Обработка каждого вопроса из полученных данных
#             for question_data in survey_data:
#                 question_text = question_data.get('nameTitleQuestion')
#                 question, created = Question.objects.get_or_create(nameTitleQuestion=question_text, survey=survey)
#                 if created:
#                     questions_to_create.append(question)
#
#                 # Обработка каждого ответа на конкретный вопрос из цикла
#                 for answer_data in question_data.get('answers', []):
#                     other_text = answer_data.get('other')
#
#                     # Если в ответе есть текст "other", то обрабатываем его
#                     if other_text is not None:
#                         answer, created = Answer.objects.get_or_create(text='other', question=question)
#
#                         if answer.other is None:
#                             answer.other = []
#                         answer.other.append(other_text)
#                         answer.count += 1
#                         if created:
#                             answers_to_create.append(answer)
#                         else:
#                             answers_to_update.append(answer)
#                         continue
#
#                     # Иначе обрабатываем текст ответа
#                     else:
#                         answer_text = answer_data.get('text')
#                         answer, created = Answer.objects.get_or_create(text=answer_text, question=question)
#
#                         # Если в ответ не содержит 'choices', то обрабатываем его
#                         if not answer_data.get('choices'):
#                             if created:
#                                 answer.count = 1
#                                 answers_to_create.append(answer)
#                             else:
#                                 answer.count += 1
#                                 answers_to_update.append(answer)
#
#                         # Если ответ содержит 'choices', то обрабатываем их
#                         else:
#                             for choice_data in answer_data.get('choices', []):
#                                 choice_text = choice_data.get('text')
#                                 choice, created = Choice.objects.get_or_create(text=choice_text, answer=answer)
#                                 if created:
#                                     choice.count = 1
#                                     choices_to_create.append(choice)
#                                 else:
#                                     choice.count += 1
#                                     choices_to_update.append(choice)
#
#             # Массовое создание новых записей
#             if questions_to_create:
#                 Question.objects.bulk_create(questions_to_create)
#             if answers_to_create:
#                 Answer.objects.bulk_create(answers_to_create)
#             if choices_to_create:
#                 Choice.objects.bulk_create(choices_to_create)
#
#             # Массовое обновление существующих записей
#             if answers_to_update:
#                 Answer.objects.bulk_update(answers_to_update, ['count', 'other'])
#             if choices_to_update:
#                 Choice.objects.bulk_update(choices_to_update, ['count'])
#
#             # Увеличение счетчика count опроса
#             survey.count += 1
#             survey.save()
#
#         except Exception as e:
#             return Response({'message': f'Error processing survey data: {str(e)}'}, status=500)
#
#         return Response({'message': 'success'})


# class CountSurveyView(APIView):
#     """
#     APIView для подсчета ответов на вопросы опроса.
#     """
#
#     @extend_schema(
#         tags=['countsurvey'],
#         request=SurveyRequestSerializer,
#         responses={200: OpenApiExample('Success', value={'message': 'success'})}
#     )
#     @transaction.atomic
#     def post(self, request: HttpRequest) -> Response:
#         """
#         Обрабатывает POST-запрос для подсчета ответов на вопросы опроса.
#
#         Args:
#             request (HttpRequest): HTTP запрос с данными опроса.
#
#         Returns:
#             Response: HTTP ответ с сообщением об успехе или ошибке.
#         """
#         survey_data = request.data.get('questions', [])
#         language = request.data.get('language', 'RU').upper()
#
#         # Проверка, что входные данные являются списком
#         if not isinstance(survey_data, list):
#             return Response({'message': 'Invalid data format, expected a list'}, status=400)
#
#         try:
#             # Определение опроса в зависимости от языка
#             survey = Survey.objects.filter(language=language).first()
#             if not survey:
#                 return Response({'message': f'Survey with language {language} not found'}, status=404)
#
#             questions_to_create = []
#             answers_to_create = []
#             choices_to_create = []
#             answers_to_update = []
#             choices_to_update = []
#
#             for question_data in survey_data:
#                 question_text = question_data.get('nameTitleQuestion')
#                 question, created = Question.objects.get_or_create(nameTitleQuestion=question_text, survey=survey)
#                 if created:
#                     questions_to_create.append(question)
#
#                 for answer_data in question_data.get('answers', []):
#                     other_text = answer_data.get('other')
#                     if other_text is not None:
#                         answer, created = Answer.objects.get_or_create(text='other', question=question)
#                         if created:
#                             answer.count = 1
#                             answer.other = [other_text]
#                             answers_to_create.append(answer)
#                         else:
#                             if answer.other is None:
#                                 answer.other = []
#                             answer.other.append(other_text)
#                             answer.count += 1
#                             answers_to_update.append(answer)
#                         continue
#
#                     answer_text = answer_data.get('text')
#                     answer, created = Answer.objects.get_or_create(text=answer_text, question=question)
#                     if created:
#                         answer.count = 1
#                         answers_to_create.append(answer)
#                     else:
#                         answer.count += 1
#                         answers_to_update.append(answer)
#
#                     for choice_data in answer_data.get('choices', []):
#                         choice_text = choice_data.get('text')
#                         choice, created = Choice.objects.get_or_create(text=choice_text, answer=answer)
#                         if created:
#                             choice.count = 1
#                             choices_to_create.append(choice)
#                         else:
#                             choice.count += 1
#                             choices_to_update.append(choice)
#
#             # Массовое создание новых записей
#             if questions_to_create:
#                 Question.objects.bulk_create(questions_to_create)
#             if answers_to_create:
#                 Answer.objects.bulk_create(answers_to_create)
#             if choices_to_create:
#                 Choice.objects.bulk_create(choices_to_create)
#
#             # Массовое обновление существующих записей
#             if answers_to_update:
#                 Answer.objects.bulk_update(answers_to_update, ['count', 'other'])
#             if choices_to_update:
#                 Choice.objects.bulk_update(choices_to_update, ['count'])
#
#             # Увеличение счетчика count опроса
#             survey.count += 1
#             survey.save()
#
#         except Exception as e:
#             return Response({'message': f'Error processing survey data: {str(e)}'}, status=500)
#
#         return Response({'message': 'success'})


@extend_schema(tags=['survey'])
class SurveyViewSet(ModelViewSet):
    """
    ViewSet для управления опросами.
    """
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


@extend_schema(tags=['question'])
class QuestionViewSet(ModelViewSet):
    """
    ViewSet для управления вопросами.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


@extend_schema(tags=['answer'])
class AnswerViewSet(ModelViewSet):
    """
    ViewSet для управления ответами.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


@extend_schema(tags=['choice'])
class ChoiceViewSet(ModelViewSet):
    """
    ViewSet для управления вариантами ответов.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
