from django.contrib import admin
from .models import (
    Profile,
    UserAvatar,
    UserSpecialization,
    PersonalQuality,
    PlaceOfWorkUser,
    EducationUser,
    UserSkill
)
from django.contrib.auth import get_user_model

User = get_user_model()


# Определение inline классов для моделей, связанных с профилем
class UserAvatarInline(admin.StackedInline):
    model = UserAvatar
    can_delete = False
    extra = 1


class UserSpecializationInline(admin.TabularInline):
    model = UserSpecialization
    extra = 1


class PersonalQualityInline(admin.StackedInline):
    model = PersonalQuality
    can_delete = False
    extra = 1


class PlaceOfWorkUserInline(admin.StackedInline):
    model = PlaceOfWorkUser
    can_delete = False
    extra = 1


class EducationUserInline(admin.StackedInline):
    model = EducationUser
    can_delete = False
    extra = 1


class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1


# Определение админ-класса для профиля
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    inlines = (
        UserAvatarInline,
        UserSpecializationInline,
        PersonalQualityInline,
        PlaceOfWorkUserInline,
        EducationUserInline,
        UserSkillInline,
    )
    list_display = ('user', 'first_name', 'last_name', 'email')
    search_fields = ('user__username', 'first_name', 'last_name', 'email')


# Определение inline класса для профиля, связанного с пользователем
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    inlines = (
        UserAvatarInline,
        UserSpecializationInline,
        PersonalQualityInline,
        PlaceOfWorkUserInline,
        EducationUserInline,
        UserSkillInline,
    )


# Определение админ-класса для пользователя
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    inlines = (ProfileInline,)


# Регистрация админ-классов
admin.site.register(Profile, ProfileAdmin)
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
