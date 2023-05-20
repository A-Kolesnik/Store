from django.contrib import admin

from .models import Product, ProductCategory, Supplier, SupplierLinkProducts


@admin.register(SupplierLinkProducts)
class SupplierLinkProductsAdmin(admin.ModelAdmin):

    """Редактор модели SupplierLinkProducts

    Описывает параметры представления модели SupplierLinkProducts на административном сайте

    """

    list_display = [
        'supplier',
        'product',
    ]


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    """Редактор модели Supplier

    Описывает параметры представления модели Supplier на административном сайте

    """

    list_display = [
        'name',
        'city',
        'created',
    ]
    fields = [
        'name',
        ('city', 'created'),
    ]
    readonly_fields = ['created']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    """Редактор модели Product

    Описывает параметры представления модели Product на административном сайте

    """

    list_display = [
        'name',
        'description',
        'price',
        'quantity',
        'image',
        'category',
    ]
    fields = [
        'name',
        'description',
        ('price', 'quantity', 'category',),
        'image',
    ]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):

    """Редактор модели ProductCategory

    Описывает параметры представления модели ProductCategory на административном сайте

    """

    list_display = [
        'name',
        'description',
    ]
