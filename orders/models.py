from django.db import models

from users.models import User


class Orders(models.Model):

    """Описывает сущность заказ

    Атрибуты:
        1. first_name - имя получателя
        2. last_name - фамилия получателя
        3. email - адрес электронной почты для связи
        4. address - адрес доставки
        5. created - дата и время оформления заказа. Заполняется автоматически при добавлении записи в БД
        6. user - пользователь, который оформил заказ. Связь Один-со-Многими. Первичная модель - User
        7. status - статус заказа. Перечисление с целочисленными внутренними значениями
        8. buscets - товары, из которых состоит заказ
        9. to_pay - сумма к оплате за заказ

    """

    class Status(models.IntegerChoices):

        """Описывает перечисление с целочисленными внутренними значениями"""

        ACCEPTED = 0, 'Принят'
        PAID = 1, 'Оплачен'
        TRANSIT = 2, 'В пути'
        DELIVERED = 3, 'Доставлен'

    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('E-mail')
    address = models.TextField('Адрес', max_length=500)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='orders',
        related_query_name='order',
        null=True,
        blank=True,
        verbose_name='Оформил'
    )
    status = models.PositiveSmallIntegerField('Статус заказа', choices=Status.choices,
                                              default=Status.ACCEPTED)
    buscets = models.JSONField('Товары', default=dict)
    to_pay = models.PositiveIntegerField('К оплате', default=0)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ #{self.id} | {self.first_name} {self.last_name} | {self.get_status_display()}"
