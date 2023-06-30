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


class DetailMessageSerializer(serializers.Serializer):
    detail = serializers.CharField()

    def update(self, instance, validated_data):
        self.update(instance, validated_data)

    def create(self, validated_data):
        self.create(validated_data)
