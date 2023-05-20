from django.db import models

from users.models import User


class ProductCategory(models.Model):

    """Описывает сущность категория товаров.

    Атрибуты:
        1. name - наименование категории
        2. description - описание

    """

    name = models.CharField('Название', max_length=50)
    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):

    """Описывает сущность товар.

    Атрибуты:
        1. name - наименование товара
        2. description - описание товара
        3. price - цена товара
        4. quantity - количество товаров в наличии
        5. image -  изображение товара
        6. category - категория товара. Связь Один-со-Многими. Первичная модель - ProductCategory.

    """
    name = models.CharField('Наименование', max_length=128)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество')
    image = models.ImageField('Изображение', upload_to='products/images/')
    category = models.ForeignKey(
        to=ProductCategory,
        on_delete=models.PROTECT,
        to_field='id',
        related_name='categories',
        related_query_name='category'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name}/{self.category}'


class BuscetQuerySet(models.QuerySet):

    """Применяется в качестве набора записей модели Buscet. Унаследован от класса QuerySet.

    Расширяет возможности QuerySet следующими реализованными методами:
        1. calc_total_price()
        2. calc_total_products()
        3. serialize_json()

    """

    def calc_total_price(self):
        """Вычисляет стоимость корзины товаров и возвращает результат"""
        return sum(buscet['product__price']*buscet['total'] for buscet in self)

    def calc_total_products(self):
        """Вычисляет количество товаров в корзине и возвращает результат"""
        return sum(buscet['total'] for buscet in self)

    def serialize_json(self):
        """Выполняет преобразование объекта BuscetQuerySet к объекту dict и возвращает полученный объект dict.

        Преобразование необходимо для заполнения поля buscets типа JsonField модели Orders.
        Метод применяется к объектам BuscetQuerySet с заранее извлеченными связанными записями первичной
        модели Product.

        """
        buscets = self.values(
            'total',
            'price',
            'product__price',
            'product__name'
        )
        buscets = [dict(buscet) for buscet in buscets]
        for buscet in buscets:
            buscet['price'] = float(buscet['price'])
            buscet['product__price'] = float(buscet['product__price'])

        return buscets


class Buscet(models.Model):

    """Описывает сущность корзина.

    Корзина товаров пользователя представлена в виде нескольких корзин,
    содержащих отдельные товары.
    Атрибуты:
        1. user - пользователь, которому принадлежит корзина. Связь Один-со-Многими. Первичная модель - User.
        2. product - товар. Связь Один-со-Многими. Первичная модель - Product.
        3. total - количество товаров в корзине
        4. created_datetime - дата создания корзины. Заполняется автоматически при добавлении записи в БД.
        5. price - цена корзины, т.е. суммарная стоимость товаров в корзине.
        6. objects - менеджер записей. В качестве типа набора записей применяется класс BuscetQuerySet

    """

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        to_field='id',
        related_name='customers',
        related_query_name='customer'
    )

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        to_field='id',
        related_name='products',
        related_query_name='product'
    )

    total = models.PositiveSmallIntegerField('Остаток', default=0)
    created_datetime = models.DateTimeField('Дата создания', auto_now_add=True)
    price = models.DecimalField('Стоимость корзины', max_digits=8, decimal_places=2)

    objects = BuscetQuerySet.as_manager()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"{self.user.username}/{self.product.name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Заполняет поле price, вызывает метод save() суперкласса."""
        self.price = self.calc_price()
        super(Buscet, self).save()

    def calc_price(self):
        """Вычисляет суммарную стоимость товаров в корзине и возвращает результат"""
        return self.product.price * self.total


class Supplier(models.Model):

    """Описывет сущность поставщик товара.

    Атрибуты:
        1. name - наименование компании-поставщика
        2. city - город, в котором расположен центральный офис компании
        3. created - дата регистрации поставщика на сайте
        4. products - продукты, которые может предоставить поставщик.
           Связь Многие-мо-Многими. Ведомая модель - Product. Связующая модель - SupplierLinkProducts.
           Поле ведущей модели, по которому устанавливается связь - supplier.
           Поле ведомой модели, по которому устанавливается связь - product.

    """

    name = models.CharField('Поставщик', max_length=100)
    city = models.CharField('Город', max_length=50)
    created = models.DateTimeField('Профиль создан', auto_now_add=True)
    products = models.ManyToManyField(
        to=Product,
        related_name='goods',
        through='SupplierLinkProducts',
        through_fields=('supplier', 'product',)
    )

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class SupplierLinkProducts(models.Model):

    """Описывает связь между поставщиком товара и товаром.

       Атрибуты:
           1. supplier - поставщик. Связь Один-со-Многими. Первичная модель - Supplier.
           2. product - продукт. Связь Один-со-Многими. Первичная модель - Product.

    """
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE, related_name='link_suppliers')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='link_products')

    class Meta:
        verbose_name = 'Поставщик/Товар'
        verbose_name_plural = 'Поставщики/Товары'

    def __str__(self):
        return f"{self.supplier.name} | {self.product.name}"
