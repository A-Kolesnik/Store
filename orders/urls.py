from django.urls import path

from .views import (OrderCreateView, OrdersListView, OrderView,
                    SuccessOrderCreateView)

app_name = 'app_orders'

urlpatterns = [
    path('/', OrdersListView.as_view(), name='show'),
    path('order/<int:order_id>', OrderView.as_view(), name='order'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('success/', SuccessOrderCreateView.as_view(), name='success'),
]
