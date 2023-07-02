from django.test import TestCase
from django.urls import reverse

from common.mixins.test_mixins import TestViewsMixin


class IndexViewTestCase(TestCase, TestViewsMixin):

    """Описывает тесты контроллера IndexView

    Переопределены методы родительского класса:
        1. setUpTestData()
        2. setUp()
    Методы-тесты:
        1. test_return_code()
        2. test_template_name()

    """

    @classmethod
    def setUpTestData(cls):
        """Выполняет подготовительные операции перед запуском всех тестов

        1. Получает url для запроса
        2. Инициализирует переменную-ключ заголовка в контексте
        3. Инициализирует переменную-наименование заголовка
        """
        cls.url = reverse('index')
        cls.title_key = 'title'
        cls.title_data = 'Store'
        cls.template_name = 'products/index.html'

    def setUp(self):
        """Выполняет GET запрос перед каждым тестом"""
        self.response = self.client.get(self.url)

    def test_response_code(self):
        """Тест кода HTTP-ответа на запрос"""
        super(IndexViewTestCase, self).run_test_response_code()

    def test_template_name(self):
        """Тест наименования шаблона, используемого для рендеринга"""
        super(IndexViewTestCase, self).run_test_template_name()

    def test_title(self):
        """Тест содержимого заголовка"""
        super(IndexViewTestCase, self).run_test_title()
