from botocore.exceptions import ClientError
from django.contrib.auth import get_user_model
from django.db.models import Q
from uuid import UUID
import uuid
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .error_messages import get_message
from .models import (
    Profile,
    UserAvatar,
    PersonalQuality,
    PlaceOfWorkUser,
    EducationUser,
    UserSpecialization,
    UserSkill
)
from .serializers import (
    UserAvatarSerializer,
    PersonalQualitySerializer,
    PlaceOfWorkUserSerializer,
    EducationUserSerializer,
    UserSpecializationSerializer,
    UserSkillSerializer,
    ProfileSerializer,
    RegistrationProfileSerializer,
    PersonalInfoSerializer,
    FriendProfileSerializer,
    UserExistsSerializer,
)

User = get_user_model()


class FriendSearchView(ListAPIView):
    """
    API для поиска друзей по имени и списку ID.
    """
    permission_classes = [AllowAny]
    serializer_class = FriendProfileSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='ids',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Список ID пользователей, разделенных запятыми.',
                required=True
            ),
            OpenApiParameter(
                name='name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Имя для поиска (first_name, last_name или username).',
                required=True
            )
        ],
        responses=FriendProfileSerializer(many=True)
    )
    def get_queryset(self):
        ids_param = self.request.query_params.get('ids', '')
        name_param = self.request.query_params.get('name', '')

        user_ids = [UUID(id) for id in ids_param.split(',') if self.is_valid_uuid(id)]

        return Profile.objects.filter(
            id__in=user_ids
        ).filter(
            Q(first_name__istartswith=name_param) |
            Q(last_name__istartswith=name_param) |
            Q(username__istartswith=name_param)
        ).order_by('first_name')

    def is_valid_uuid(self, val):
        try:
            UUID(val)
            return True
        except ValueError:
            return False


class FriendProfilesView(ListAPIView):
    """
    API для получения информации о друзьях по списку ID.
    """
    permission_classes = [AllowAny]  # IsAuthenticated
    serializer_class = FriendProfileSerializer

    @extend_schema(
        responses=FriendProfileSerializer(many=True)
    )
    def get_queryset(self):
        ids_param = self.request.query_params.get('ids', '')
        user_ids = [UUID(id) for id in ids_param.split(',') if self.is_valid_uuid(id)]
        return Profile.objects.filter(id__in=user_ids)

    def is_valid_uuid(self, val):
        try:
            UUID(val)
            return True
        except ValueError:
            return False


class CheckUserExistsView(APIView):
    """
    API для проверки существования пользователя по ID.
    """
    permission_classes = [AllowAny]  # IsAuthenticated
    serializer_class = UserExistsSerializer

    def get(self, request, user_id):
        try:
            # Преобразуем строку в UUID
            user_id = UUID(user_id)
            user_exists = Profile.objects.filter(id=user_id).exists()
            return Response({'exists': user_exists}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Invalid UUID format.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateProfileView(APIView):
    permission_classes = [AllowAny]  # IsAuthenticated

    @extend_schema(
        request=RegistrationProfileSerializer,
        responses=RegistrationProfileSerializer
    )
    def post(self, request) -> Response:
        try:
            user_id = request.data.get('id')
            # Преобразуем строку в UUID
            user_id = uuid.UUID(user_id)
            user, created = User.objects.get_or_create(
                pk=user_id,
                defaults={
                    'username': request.data.get('username'),
                    'email': request.data.get('email'),
                    'first_name': request.data.get('first_name')
                }
            )

            if created:
                # Обновляем профиль с дополнительными данными
                user.profile.username = user.username
                user.profile.email = user.email
                user.profile.first_name = user.first_name
                user.profile.save()

            serializer = RegistrationProfileSerializer(user.profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"detail": "Invalid UUID format."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileView(APIView):
    """
    Класс для получения и обновления профиля пользователя по id
    """
    permission_classes = [AllowAny]  # IsAuthenticated
    serializer_class = ProfileSerializer

    @extend_schema(
        responses=ProfileSerializer
    )
    def get(self, request, pk):
        """
        Метод для получения профиля пользователя по id
        """
        user = get_object_or_404(User, pk=pk)
        profile, created = Profile.objects.get_or_create(user=user)

        # Создаем объект UserAvatar, если он не существует
        # if not hasattr(profile, 'avatar'):
        #     UserAvatar.objects.create(user=profile)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    # @extend_schema(
    #     request=ProfileSerializer,
    #     responses=ProfileSerializer
    # )
    # def put(self, request, pk):
    #     """
    #     Метод для обновления профиля пользователя по id
    #     """
    #     if request.user.pk != pk:
    #         return Response({"detail": get_message("forbidden")},
    #                         status=status.HTTP_403_FORBIDDEN)
    #
    #     user = get_object_or_404(User, pk=pk)
    #     profile, created = Profile.objects.get_or_create(user=user)
    #     serializer = ProfileSerializer(profile, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePersonalInfoView(APIView):
    permission_classes = [AllowAny]  # IsAuthenticated

    @extend_schema(
        request=PersonalInfoSerializer,
        responses=PersonalInfoSerializer
    )
    def put(self, request, pk):
        """
        Метод для обновления информации о профиле пользователя
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        serializer = PersonalInfoSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['User Specialization'],
)
class UserSpecializationPostView(APIView):
    """
    Класс для создания специализации пользователя
    """
    permission_classes = [AllowAny]
    serializer_class = UserSpecializationSerializer

    @swagger_auto_schema(
        request_body=UserSpecializationSerializer,
        responses={201: UserSpecializationSerializer},
        manual_parameters=[
            openapi.Parameter(
                name='pk',
                in_=openapi.IN_PATH,
                description='ID пользователя',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def post(self, request, pk):
        """Метод для создания специализации пользователя"""
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)

        if profile.specializations.count() >= 3:
            return Response({"detail": "Пользователь не может иметь более 3 специализаций."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return


@extend_schema(
    tags=['User Specialization'],
)
class UserSpecializationPutDeleteView(APIView):
    """
    Класс для обновления и удаления специализации пользователя
    """
    permission_classes = [AllowAny]
    serializer_class = UserSpecializationSerializer

    @swagger_auto_schema(
        request_body=UserSpecializationSerializer,
        responses={200: UserSpecializationSerializer},
        manual_parameters=[
            openapi.Parameter(
                name='pk',
                in_=openapi.IN_PATH,
                description='ID пользователя',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                name='specialization_id',
                in_=openapi.IN_PATH,
                description='ID специализации',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def put(self, request, pk, specialization_id):
        """Метод для обновления специализации пользователя"""
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        specialization = get_object_or_404(UserSpecialization, pk=specialization_id, user=profile)

        serializer = UserSpecializationSerializer(specialization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'No Content'},
        manual_parameters=[
            openapi.Parameter(
                name='pk',
                in_=openapi.IN_PATH,
                description='ID пользователя',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                name='specialization_id',
                in_=openapi.IN_PATH,
                description='ID специализации',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def delete(self, request, pk, specialization_id):
        """Метод для удаления специализации пользователя"""
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        specialization = get_object_or_404(UserSpecialization, pk=specialization_id, user=profile)

        specialization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['Place of Work'],
)
class PlaceOfWorkPostView(APIView):
    """
    Класс для создания информации о месте работы
    """
    permission_classes = [AllowAny]
    serializer_class = PlaceOfWorkUserSerializer

    @swagger_auto_schema(
        request=PlaceOfWorkUserSerializer,
        responses=PlaceOfWorkUserSerializer,
        parameters=[
            openapi.Parameter(
                name='pk',
                in_=openapi.IN_PATH,
                description='ID пользователя',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def post(self, request, pk):
        """
        Метод для создания информации о месте работы
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        if profile.place_of_work.count() >= 3:
            return Response({"detail": "Пользователь не может иметь более 3 мест работы."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = PlaceOfWorkUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Place of Work'],
)
class PlaceOfWorkPutDeleteView(APIView):
    """
    Класс для обновления и удаления информации о месте работы
    """
    permission_classes = [AllowAny]
    serializer_class = PlaceOfWorkUserSerializer

    @swagger_auto_schema(
        request=PlaceOfWorkUserSerializer,
        responses=PlaceOfWorkUserSerializer,
        parameters=[
            openapi.Parameter(
                name='pk',
                in_=openapi.IN_PATH,
                description='ID пользователя',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                name='place_of_work_id',
                in_=openapi.IN_PATH,
                description='ID места работы',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def put(self, request, pk, place_of_work_id):
        """
        Метод для обновления информации о месте работы
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        place_of_work = get_object_or_404(PlaceOfWorkUser, pk=place_of_work_id, user=profile)
        serializer = PlaceOfWorkUserSerializer(place_of_work, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, place_of_work_id):
        """
        Метод для удаления информации о месте работы
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        place_of_work = get_object_or_404(PlaceOfWorkUser, pk=place_of_work_id, user=profile)
        place_of_work.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['Personal Quality'],
)
class UpdatePersonalQualityView(APIView):
    """
    Класс для обновления информации о личных качествах
    """
    permission_classes = [AllowAny]  # IsAuthenticated
    serializer_class = PersonalQualitySerializer

    @extend_schema(
        request=PersonalQualitySerializer,
        responses=PersonalQualitySerializer
    )
    def put(self, request, pk):
        """
        Метод для обновления информации о личных качествах
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        personal_quality, created = PersonalQuality.objects.get_or_create(
            user=profile,
            defaults={
                'quality': request.data.get('quality', '')
            }
        )
        serializer = PersonalQualitySerializer(personal_quality, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, personal_quality_id):
        """
        Метод для удаления информации о личных качествах
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        personal_quality = get_object_or_404(PersonalQuality, pk=personal_quality_id, user=profile)
        personal_quality.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['User Education'],
)
class EducationPostView(APIView):
    """
    Класс для создания информации об образовании
    """
    permission_classes = [AllowAny]
    serializer_class = EducationUserSerializer

    @swagger_auto_schema(
        request=EducationUserSerializer,
        responses=EducationUserSerializer,
        parameters=[
            openapi.Parameter(
                name='pk',
                in_=openapi.IN_PATH,
                description='ID пользователя',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def post(self, request, pk):
        """
        Метод для создания информации об образовании
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        if profile.education.count() >= 3:
            return Response({"detail": "Пользователь не может иметь более 3 образований."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = EducationUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['User Education'],
)
class EducationPutDeleteView(APIView):
    """
    Класс для обновления и удаления информации об образовании
    """
    permission_classes = [AllowAny]
    serializer_class = EducationUserSerializer

    @swagger_auto_schema(
        request=EducationUserSerializer,
        responses=EducationUserSerializer,
        parameters=[
            openapi.Parameter(
                name='pk',
                in_=openapi.IN_PATH,
                description='ID пользователя',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                name='education_id',
                in_=openapi.IN_PATH,
                description='ID образования',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def put(self, request, pk, education_id):
        """
        Метод для обновления информации об образовании
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        education = get_object_or_404(EducationUser, pk=education_id, user=profile)
        serializer = EducationUserSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, education_id):
        """
        Метод для удаления информации об образовании
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        education = get_object_or_404(EducationUser, pk=education_id, user=profile)
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['User Avatar'])
class UpdateAvatarView(APIView):
    """
    Класс для обновления аватара пользователя
    """
    permission_classes = [AllowAny]  # IsAuthenticated
    serializer_class = UserAvatarSerializer

    @extend_schema(
        request=UserAvatarSerializer,
        responses=UserAvatarSerializer
    )
    def put(self, request, pk):
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        avatar, created = UserAvatar.objects.get_or_create(user=profile)

        try:
            serializer = UserAvatarSerializer(avatar, data=request.data)
            if serializer.is_valid():
                # Удаляем старую аватарку после успешной валидации
                avatar.delete_old_avatar()

                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ClientError as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """
        Метод для удаления аватара пользователя
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        avatar = get_object_or_404(UserAvatar, user=profile)
        avatar.avatar = 'uploads/default.jpg'
        avatar.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['User Skill'],
)
class SkillPostView(APIView):
    """
    Класс для создания навыка пользователя
    """
    permission_classes = [AllowAny]
    serializer_class = UserSkillSerializer

    @swagger_auto_schema(
        request=UserSkillSerializer,
        responses=UserSkillSerializer,
        parameters=[
            openapi.Parameter(
                name='pk',
                in_=openapi.IN_PATH,
                description='ID пользователя',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def post(self, request, pk):
        """
        Метод для создания навыка пользователя
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        serializer = UserSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['User Skill'],
)
class SkillPutDeleteView(APIView):
    """
    Класс для обновления и удаления навыка пользователя
    """
    permission_classes = [AllowAny]
    serializer_class = UserSkillSerializer

    @swagger_auto_schema(
        request=UserSkillSerializer,
        responses=UserSkillSerializer,
        parameters=[
            openapi.Parameter(
                name='pk',
                in_=openapi.IN_PATH,
                description='ID пользователя',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                name='skill_id',
                in_=openapi.IN_PATH,
                description='ID навыка',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def put(self, request, pk, skill_id):
        """
        Метод для обновления навыка пользователя
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        skill = get_object_or_404(UserSkill, pk=skill_id, user=profile)
        serializer = UserSkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, skill_id):
        """
        Метод для удаления навыка пользователя
        """
        # if request.user.pk != pk:
        #     return Response({"detail": get_message("forbidden")},
        #                     status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        skill = get_object_or_404(UserSkill, pk=skill_id, user=profile)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
