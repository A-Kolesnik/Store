import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.timezone import now

from .models import User, UserConfirmation


class LoginForm(AuthenticationForm):

    """Описывает форму входа.

    Атрибуты:
        1. username - логин пользователя
        2. password - пароль

    """

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль'}
    ))

    class Meta:
        model = User
        fields = ('username', 'password')


class RegistrationForm(UserCreationForm):

    """Описывает форму регистрации пользователя на сайте.

    Переопределен метод save() суперкласса.
    Атрибуты:
        1. first_name - имя пользователя
        2. last_name - фамилия пользователя
        3. username -логин пользователя
        4. password1 - пароль пользователя
        5. password2 - повтор пароля пользователя
        6. email - адрес электронной почты пользователя

    """

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите фамилию',
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя',

    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Подтвердите пароль',
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите адрес эл. почты',
    }))

    def save(self, commit=True):
        """Выполняет метод save() суперкласса и отправляет ссылку на подтверждение адреса э/почты."""
        user = super(RegistrationForm, self).save(commit=commit)

        user_confirmation = UserConfirmation.objects.create(
            code=uuid.uuid4(),
            user=user,
            expiration=now() + timedelta(minutes=10)
        )
        user_confirmation.send_verification_email()
        return user

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
            'email',
        )


class UserCreationForm(forms.ModelForm):

    """Описывет форму изменения данных пользователя.

    Атрибуты:
        1. first_name - имя пользователя
        2. last_name - фамилия пользователя
        3. image - изображение пользователя
        4. username - логин пользователя
        5. email - адрес электронной почты пользователя

    """

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-label'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'image',
                  'username',
                  'email',
                  )
