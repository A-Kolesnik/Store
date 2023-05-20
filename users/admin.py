from django.contrib import admin

from .models import User, UserConfirmation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    """Редактор модели User

    Описывает параметры представления модели User на административном сайте

    """

    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        'is_verified',
    ]
    fields = [
        'username',
        ('first_name', 'last_name',),
        'email',
        'is_verified',
    ]
    readonly_fields = [
        'is_verified',
        'email',
    ]


@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):

    """Редактор модели UserConfirmation

    Описывает параметры представления модели UserConfirmation на административном сайте

    """

    list_display = [
        'code',
        'user',
        'created',
        'expiration',
    ]
    readonly_fields = [
        'code',
        'user',
        'created',
        'expiration',
    ]
