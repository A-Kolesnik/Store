from rest_framework import serializers

from .models import Product


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
