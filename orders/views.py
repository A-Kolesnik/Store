from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from common.views import CommonMixin
from products.models import Buscet

from .forms import OrdersForm
from .models import Orders


class OrderCreateView(CommonMixin, CreateView):

    """Выводит форму создания заказа, выполняет ее валидацию и добавляет запись в БД.

    Класс-контроллер унаследован от класса-контроллера CreateView.
    Выполнено переопределение метода form_valid() суперкласса с целью
    добавления в запись значений полей, отсутствующих в форме.
    Атрибуты:
        1. title - заголовок страницы. Атрибут предоставляется миксином CommonMixin
        2. template_name - путь к файлу шаблона, сощдающего страницу с формой
        3. form_class - ссылка на класс используемой формы
        4. success_url - адрес для перенаправления в случае успешной валидации формы

    """

    title = 'Store - Оформление заказа'
    template_name = 'orders/order-create.html'
    form_class = OrdersForm
    success_url = reverse_lazy('orders:success')

    def form_valid(self, form):
        """Вычисляет значения отсутствующих в форме полей, выполняет валидацию формы, удаляет корзину.

        1. Вычисляет значения полей user, buscets, to_pay перед операцией валидации формы
        2. Выполняет метод form_valid() суперкласса
        3. В случае успешной валидации, удаляет корзину пользователя

        """
        form.instance.user = self.request.user
        buscets = Buscet.objects.select_related('product').filter(
            user=self.request.user
        )

        Buscet.objects.select_related(None)

        form.instance.buscets = buscets.serialize_json()

        form.instance.to_pay = buscets.values(
            'total',
            'product__price',
        ).calc_total_price()

        response = super(OrderCreateView, self).form_valid(form)
        buscets.delete()

        return response


class SuccessOrderCreateView(CommonMixin, TemplateView):

    """Выполняет рендеринг шаблона"""

    title = 'Store - Спасибо за заказ!'
    template_name = 'orders/order-success.html'


class OrdersListView(CommonMixin, ListView):

    """Отображает список заказов пользователя

    Заказы отсортированы по дате создания.
    Результат запроса помещается в переменную контекста шаблона 'orders'.
    Переопределен метод суперкласса get_queryset()
    Атрибуты:
        1. model - модель, используемая для выполнения запросов
        2. template_name - путь к файлу шаблона, создающего страницу с формой
        3. context_object_name - переменная контекста, содержащая результат запроса
        4. ordering - поле, по которому будет выполнена сортировка
        5. title - заголовок страницы. Атрибут предоставляется миксином CommonMixin

    """

    model = Orders
    template_name = 'orders/orders.html'
    context_object_name = 'orders'
    ordering = ('-created',)
    title = 'Store - Заказы'

    def get_queryset(self):
        """Возвращает список заказов, принадлежащих определенному пользователю"""
        return super(
            OrdersListView,
            self
        ).get_queryset().filter(
            user=self.request.user
        )


class OrderView(DetailView):

    """Отображает детали определенного товара.

    Атрибуты:
        1. model - модель, используемая для выполнения запросов
        2. pk_url_kwarg - наименование URL-параметра для извлечения ключа записи
        3. template_name - путь к файлу шаблона, сощдающего страницу с формой
        4. context_object_name - переменная контекста, содержащая результат запроса

    """

    model = Orders
    pk_url_kwarg = 'order_id'
    template_name = 'orders/order.html'
    context_object_name = 'order'
