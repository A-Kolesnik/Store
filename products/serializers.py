from rest_framework import serializers

from .models import Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):

    """Выполняет преобразование набора записей 'товары' к формату json"""

    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'quantity',
        )


class ProductCategorySerializer(serializers.ModelSerializer):

    """Выполняет преобразование набора записей 'категории товаров' к формату json"""

    class Meta:
        model = ProductCategory
        fields = (
            'name',
            'description',
        )
