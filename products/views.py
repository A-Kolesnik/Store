from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from rest_framework.generics import CreateAPIView, ListAPIView

from common.views import CommonMixin

from .models import Buscet, Product, ProductCategory
from .serializers import ProductCategorySerializer, ProductSerializer


class IndexView(CommonMixin, TemplateView):

    """Выполняет рендеринг шаблона"""

    template_name = 'products/index.html'
    title = 'Store'


class ProductListView(CommonMixin, ListView):
    """Отображает список товаров в каталоге.

    Товары отсортированы по наименованию.
    Результат запроса помещается в переменную контекста шаблона 'products'.
    Переопределены следующие методы суперкласса:
        1. get_queryset()
        2. get_context_data()
    Атрибуты:
        1. model - модель, используемая для выполнения запросов
        2. template_name - путь к файлу шаблона, создающего страницу с формой
        3. context_object_name - переменная контекста, содержащая результат запроса
        4. ordering - поле, по которому будет выполнена сортировка
        5. title - заголовок страницы. Атрибут предоставляется миксином CommonMixin
        6. paginate_by - число товаров в одной части пагинатора

    """
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    ordering = ('name',)
    title = 'Store - Каталог'
    paginate_by = 2

    def get_queryset(self):
        """Возвращает список товаров.

        Если в URL присутствует параметр, указывающий на определенную категорию товаров,
        то набор записей будет состоять только из товаров указанной категории.
        Если категория не указана, то набор записей будет содержать товары всех категорий.
        Если указана категория, которая не существует или не имеющая товаров, будет возвращена 404

        """
        category_id = self.kwargs.get('categoryID')
        queryset = get_list_or_404(
            klass=self.model,
            category_id=category_id
        ) if category_id else self.model.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет в контекст переменную, содержащую список категорий товаров"""
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context


class APIProductsListView(ListAPIView):

    """Возвращает ресурс-перечень товаров

    Переопределены атрибуты:
        1. queryset - набор записей
        2. serializer_class - ссылка на класс-сериализатор

    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class APIProductsByCategory(ListAPIView):

    """Возвращает ресурс-перечень товаров запрашиваемой по id категории

     Переопределены атрибуты:
         1. serializer_class - ссылка на класс-сериализатор
     Переопределены методы:
         1. get_queryset()
     """

    serializer_class = ProductSerializer
    lookup_category_id = 'categoryID'

    def get_queryset(self):
        """Извлекает и возвращает товары запрашиваемой категории

        Категория передается в URL-параметре 'categoryID' в виде ее primary_key 'id'

        """
        queryset = Product.objects.select_related(
            'category'
        ).filter(
            category__id=self.kwargs[self.lookup_category_id]
        ).values(
            'name',
            'description',
            'price',
            'quantity',
        )
        Product.objects.select_related(None)

        return queryset


class APIProductCategoryAddView(CreateAPIView):

    """Создает ресурс-категория товара

    Переопределены атрибуты:
        1. serializer_class - ссылка на класс сериализатора

    """

    serializer_class = ProductCategorySerializer


@login_required
def add_product(request: HttpRequest, product_id: int):
    """Добавляет товар в корзину пользователя и возвращает текущую страницу

    Если для указанного товара, не найдена корзина, создается новая запись .
    Если корзина для товара уже существует, уведичивается поле total/

    """
    product = get_object_or_404(klass=Product, id=product_id)
    try:
        buscet = Buscet.objects.get(user=request.user, product=product)
        buscet.total += 1
        buscet.save()
    except ObjectDoesNotExist:
        Buscet.objects.create(user=request.user, product=product, total=1)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def remove_product(request: HttpRequest, buscet_id: int):
    """Удаляет корзину товара и возвращает текущую страницу"""
    Buscet.objects.filter(id=buscet_id).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
