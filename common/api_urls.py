from django.urls import path

from products.views import APIProductsListView

urlpatterns = [
    path('products/', APIProductsListView.as_view()),
]
