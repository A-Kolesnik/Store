from django.urls import path

from .views import ProductListView, add_product, remove_product

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='prod_page'),
    path('category/<int:categoryID>/', ProductListView.as_view(), name='category'),
    path('buscet/add/<int:product_id>/', add_product, name='add_product'),
    path('buscet/remove/<int:buscet_id>/', remove_product, name='remove_product'),
]
