from django.urls import path

from products.views import APIProductsListView, APIProductsByCategory

urlpatterns = [
    path('products/', APIProductsListView.as_view()),
    path('products/<int:categoryID>', APIProductsByCategory.as_view()),
]
