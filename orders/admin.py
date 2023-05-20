from django.contrib import admin

from .models import Orders


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):

    """Редактор модели Orders

    Описывает параметры представления модели Orders на административном сайте

    """

    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'created',
        'status',
        'user',
        'to_pay',
    )
    list_display_links = ('id',)
    readonly_fields = (
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'created',
        'status',
        'user',
        'to_pay',
        'buscets',
    )
