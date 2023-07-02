from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from common.permissions import ApiUserPermission
from common.views import CommonMixin

from .models import Buscet, Product, ProductCategory
from .serializers import (DetailMessageSerializer, ProductCategorySerializer,
                          ProductSerializer)


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
        queryset = self.model.objects.filter(category_id=category_id) if category_id else self.model.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет в контекст переменную, содержащую список категорий товаров"""
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context


@extend_schema(tags=['Products'])
@extend_schema_view(
    list=extend_schema(
        operation_id='api_products_list',
        summary='Получить список товаров',
        description=' ',
        responses={
            (status.HTTP_200_OK, 'application/json'): ProductSerializer,
            (status.HTTP_401_UNAUTHORIZED, 'application/json'): DetailMessageSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='category',
                location=OpenApiParameter.QUERY,
                required=False,
                description='id категории',
                type=int
            ),
        ]
    ),
    retrieve=extend_schema(
        operation_id='api_products_by_category_list',
        summary='Получить товар по id',
        description=' ',
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                required=True,
                description='id товара'
            )
        ],
        responses={
            (status.HTTP_200_OK, 'application/json'): ProductSerializer,
            (status.HTTP_401_UNAUTHORIZED, 'application/json'): DetailMessageSerializer,
            (status.HTTP_404_NOT_FOUND, 'application/json'): DetailMessageSerializer,
        }
    ),
    create=extend_schema(
        operation_id='api_products_create',
        summary='Добавить товар',
        description=' ',
        responses={
            (status.HTTP_201_CREATED, 'application/json'): ProductSerializer,
            (status.HTTP_401_UNAUTHORIZED, 'application/json'): DetailMessageSerializer,
            (status.HTTP_403_FORBIDDEN, 'application/json'): DetailMessageSerializer
        }
    ),
    destroy=extend_schema(
        operation_id='api_products_destroy',
        summary='Удалить товар',
        description=' ',
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                required=True,
                description='id товара, который необходимо удалить'
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            (status.HTTP_401_UNAUTHORIZED, 'application/json'): DetailMessageSerializer,
            (status.HTTP_403_FORBIDDEN, 'application/json'): DetailMessageSerializer
        }
    )

)
class ApiProductsViewSet(ModelViewSet):

    """Возвращает ресурс-перечень товаров или ресурс-перечень товаров отдельной категории

    Переопределены атрибуты:
        1. queryset - набор записей
        2. serializer_class - ссылка на класс-сериализатор

    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (ApiUserPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',)
    http_method_names = ['get', 'post', 'delete']


@extend_schema(tags=['Product Categories'])
@extend_schema_view(
    list=extend_schema(
        operation_id='api_products_category_list',
        summary='Получить список категорий',
        description=' ',
        responses={
            (status.HTTP_200_OK, 'application/json'): ProductCategorySerializer,
            (status.HTTP_401_UNAUTHORIZED, 'application/json'): DetailMessageSerializer,
        },
    ),
    retrieve=extend_schema(
        operation_id='api_catgory_by_id',
        summary='Получить категорию по id',
        description=' ',
        parameters=[
          OpenApiParameter(
              name='id',
              type=int,
              location=OpenApiParameter.PATH,
              required=True,
              description='id категории товара'
          )
        ],
        responses={
            (status.HTTP_200_OK, 'application/json'): ProductCategorySerializer,
            (status.HTTP_401_UNAUTHORIZED, 'application/json'): DetailMessageSerializer,
            (status.HTTP_404_NOT_FOUND, 'application/json'): DetailMessageSerializer,
        }
    ),
    create=extend_schema(
        operation_id='api_category_create',
        summary='Добавить категорию товара',
        description=' ',
        responses={
            (status.HTTP_201_CREATED, 'application/json'): ProductCategorySerializer,
            (status.HTTP_401_UNAUTHORIZED, 'application/json'): DetailMessageSerializer,
            (status.HTTP_403_FORBIDDEN, 'application/json'): DetailMessageSerializer
        }
    ),
    destroy=extend_schema(
        operation_id='api_category_destroy',
        summary='Удалить категорию товара',
        description=' ',
        parameters=[
          OpenApiParameter(
              name='id',
              type=int,
              location=OpenApiParameter.PATH,
              required=True,
              description='id категории товара, которую необходимо удалить'
          )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            (status.HTTP_401_UNAUTHORIZED, 'application/json'): DetailMessageSerializer,
            (status.HTTP_403_FORBIDDEN, 'application/json'): DetailMessageSerializer
        }
    )

)
class APIProductCategoryViewSet(ModelViewSet):

    """Создает ресурс-категория товара

    Переопределены атрибуты:
        1. serializer_class - ссылка на класс сериализатора

    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (ApiUserPermission,)
    http_method_names = ['get', 'post', 'delete']


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
