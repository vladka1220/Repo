from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = service_register_customuser.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            service_register_customuser.DoesNotExist,
        ):
            return Response(
                {"error": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST
            )

        if default_token_generator.check_token(user, token):
            serializer = PasswordResetConfirmSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response(
                    {"message": "Password has been reset."}, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
