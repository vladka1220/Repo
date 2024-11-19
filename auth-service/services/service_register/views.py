from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from config.decorators.handle_auth_errors import handle_auth_errors
from config.decorators.handle_registration_errors import handle_registration_errors
from config.decorators.handle_server_errors import handle_server_errors
from config.decorators.handle_validation_errors import handle_validation_errors
from config.decorators.handle_success_messages import handle_success_messages
from config.decorators.handle_log_messages import log_messages
from config.system_messages_config.error_messages import get_message
from config.system_messages_config.error_codes import ERROR_CODES
from .serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
    """
    Представление для регистрации нового пользователя.

    Методы:
    - post(request, *args, **kwargs): Обрабатывает POST-запрос
    для регистрации нового пользователя.
    """

    permission_classes = [AllowAny]

    @handle_server_errors
    @handle_validation_errors
    @handle_registration_errors
    @handle_auth_errors
    @handle_success_messages
    @log_messages
    def post(self, request):
        """
        Обрабатывает POST-запрос для регистрации нового пользователя.

        Параметры:
        - request (Request): HTTP-запрос с данными для регистрации.

        Возвращает:
        - Response: HTTP-ответ с кодом статуса 201 и сообщением об успешной регистрации.
        - В случае ошибок, возвращает коды и описание ошибки.
        """

        serializer = UserRegistrationSerializer(data=request.data)

        # Проверка на валидность входящих данных
        serializer.is_valid(raise_exception=True)

        # Создание пользователя
        serializer.save()  # Изменено: убрали возврат user и token

        # Формирование данных ответа
        return Response(
            {"registration_successful": get_message("registration_successful")},
            status=ERROR_CODES["HTTP_201_CREATED"],
        )
