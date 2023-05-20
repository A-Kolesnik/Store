from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import CommonMixin

from .forms import LoginForm, RegistrationForm, UserCreationForm
from .models import User, UserConfirmation


class UsersLoginView(LoginView):

    """Выполняет операцию входа на сайт.

    Атрибуты:
        1. template_name - путь к файлу шаблона, создающего страницу с формой
        2. authentication_form - ссылка на класс формы входа

    """

    template_name = 'users/login.html'
    authentication_form = LoginForm


class UserRegisterView(SuccessMessageMixin, CreateView):

    """Отображает форму регистрации, выполняет ее валидацию, добавляет новую запись модели.

    Атрибуты:
        1. template_name - путь к файлу шаблона, создающего страницу с формой
        2. form_class - ссылка на класс формы
        3. success_url - адрес для перенаправления, если форма прошла валидацию
        4. success_message - сообщение пользователю, если регистрация прошла успешно.
        Атрибут предоставляется миксином SuccessMessageMixin

    """

    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('app_users:login')
    success_message = 'Регистрация прошла успешно'


class UsersUpdateView(CommonMixin, UpdateView):

    """Выполняет изменение данных пользователя.

    Переопределен метод суперкласса get_succcess_url()
    Атрибуты:
        1. form_class - ссылка на класс формы
        2. model - модель, используемая для выполнения запросов
        3. template_name - путь к файлу шаблона, создающего страницу с формой
        4. title - заголовок страницы. Атрибут предоставляется миксином CommonMixin

    """

    form_class = UserCreationForm
    model = User
    template_name = 'users/profile.html'
    title = 'Store - Профиль'

    def get_success_url(self):
        """Возвращает адрес страницы профиля определенного пользователя"""
        return reverse_lazy('users:profile', args=(self.object.id,))


class UsersConfirmationView(CommonMixin, TemplateView):

    """Выполняет рендеринг шаблона.

    Переопределен метод суперкласса get()
    Атрибуты:
        1. title - заголовок страницы. Атрибут предоставляется миксином CommonMixin
        2. template_name - путь к файлу шаблона, создающего страницу с формой

    """

    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        """Извлекает информацию о коде подтверждения, выполняет проверку его валидности.

        Если ссылка не валидна, выполняется перенаправление на главную страницу.
        Если ссылка валидна, полю is_verified присваивается значение True и вызывается метод get() суперкласса.
        """
        try:
            user_confirm = UserConfirmation.objects.get(code=kwargs['code'])

            if now() > user_confirm.expiration:
                raise Exception("Ссылка не валидна")

            user_confirm.user.is_verified = True
            user_confirm.user.save()
        except Exception as ex:
            print(ex)
            return redirect(to=reverse('index'))

        return super().get(request, *args, **kwargs)
