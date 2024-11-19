from rest_framework import serializers
from .validators import ProfileValidator
from drf_spectacular.utils import extend_schema_field
from .models import (
    Profile, UserAvatar, UserSpecialization, PersonalQuality,
    PlaceOfWorkUser, EducationUser, UserSkill
)


class FriendProfilesRequestSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Список UUID пользователей для получения информации о друзьях."
    )


class UserExistsSerializer(serializers.Serializer):
    exists = serializers.BooleanField()


class FriendProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    specializations = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'specializations']

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_avatar(self, obj):
        # Возвращаем URL аватара, если он существует
        if hasattr(obj, 'avatar') and obj.avatar.avatar:
            return obj.avatar.avatar.url
        return None

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_specializations(self, obj):
        # Возвращаем список специализаций (до 3 штук)
        return list(obj.specializations.values_list('specialization', flat=True)[:3])


class PersonalInfoSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.CharField(validators=[ProfileValidator.validate_date_format])

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'tg_nick',
            'email',
            'date_of_birth',
            'gender',
            'location',
            'phone'
        ]


class RegistrationProfileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'email', 'token']


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = ['avatar']

    def validate_size(self, value):
        if value > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError("Размер файла не должен превышать 5MB.")
        return value


class UserSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSpecialization
        fields = ['id', 'specialization']


class PersonalQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalQuality
        fields = ['quality', 'link']

    def validate_quality(self, text):
        if len(text) > 150:
            raise serializers.ValidationError("Длинна текста не более 150 символов.")
        return text


class PlaceOfWorkUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOfWorkUser
        fields = ['id', 'company', 'position', 'work_period']


class EducationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationUser
        fields = ['id', 'college', 'speciality', 'year_of_study', 'link']


class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = ['id', 'skill_name', 'skill_type']


class ProfileSerializer(serializers.ModelSerializer):
    avatar = UserAvatarSerializer()
    specializations = UserSpecializationSerializer(many=True)
    personal_quality = PersonalQualitySerializer()
    place_of_work = PlaceOfWorkUserSerializer(many=True, required=False)
    education = EducationUserSerializer(many=True, required=False)
    skills = UserSkillSerializer(many=True, required=False)

    personal_info = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'personal_info',
            'avatar',
            'specializations',
            'personal_quality',
            'place_of_work',
            'education',
            'skills'
        ]

    @extend_schema_field(serializers.DictField(child=serializers.CharField()))
    def get_personal_info(self, obj):
        return {
            'username': obj.username,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'tg_nick': obj.tg_nick,
            'email': obj.email,
            'date_of_birth': obj.date_of_birth,
            'gender': obj.gender,
            'location': obj.location,
            'phone': obj.phone,
        }
