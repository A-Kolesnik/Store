from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


class User(AbstractUser):

    """Описывает сущность пользователь.

    Переопределяет метод save() суперкласса.
    Наследует все атрибуты модели AbstractUser
    Расширяет модель AbstractUser следующими атрибутами:
        1. image - изображение пользователя
        2. is_verified - адрес электронной почты подтвержден/не подтвержден

    """

    image = models.ImageField('Изображение', upload_to='users/images', null=True, blank=True)
    is_verified = models.BooleanField('Подтвержден', default=False)

    def save(self, *args, **kwargs):
        """Удаляет фото пользователя и вызывает метод save() суперкласса"""
        last_user_info = User.objects.get(pk=self.pk)
        last_user_info.image.delete(save=False)
        super(User, self).save()


class UserConfirmation(models.Model):

    """Описывает сущность код потверждения адреса э/почты.

    Реализованы методы:
        1. send_verification_email()
    Атрибуты:
        1. code - код подтверждения
        2. user - пользователь, к которому привязан код
        3. created - дата/время создания
        4. expiration - до какого времени валиден

    """

    code = models.UUIDField(
        'Код для подтверждения',
        primary_key=True,
        editable=False
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='users',
        related_query_name='user'
    )
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    expiration = models.DateTimeField('Валиден до')

    def send_verification_email(self):
        """Формирует и отправляет пользователю сообщение с ссылкой-подтверждением адреса э/почты"""
        send_mail(
            subject='Verification',
            message=f"Welcome, {self.user.username}!\n"
                    f"Thanks for signing up with Store market!\n"
                    f"You must follow this link to activate your account:\n"
                    f"{settings.DOMAIN_NAME}users/confirm-email/{self.code}\n",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
        )

    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'
