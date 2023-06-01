from django.test import TestCase
from products.models import Product, ProductCategory
from common.mixins.test_mixins import TestVerboseNameMixin


class ProductTests(TestCase, TestVerboseNameMixin):

    """Описывает тесты модели Product

    Переопределены методы родительского класса:
        1. setUpTestData()
    Методы-тесты:
        1. test_verbose_name()
    """

    @classmethod
    def setUpTestData(cls):
        """Выполняет подготовительные операции перед запуском всех тестов"""
        product_category = ProductCategory.objects.create(
            name='Головные уборы'
        )
        cls.product = Product.objects.create(
            name='Кепка',
            description='Материал: хлопок, Цвет: черный',
            price=1580,
            quantity=10,
            category=product_category
        )
        cls.fields_verbose_name = {
            'name': 'Наименование',
            'description': 'Описание',
            'price': 'Цена',
            'quantity': 'Количество',
            'image': 'Изображение',
        }

    def test_verbose_name(self):
        """Тест параметра verbose_name полей модели"""
        super(ProductTests, self).run_test_verbose_name(self.product, self.fields_verbose_name)
