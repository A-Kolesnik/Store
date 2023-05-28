from django.urls import path

from products.views import (APIProductCategoryAddView, APIProductsByCategoryView,
                            APIProductsListView)

urlpatterns = [
    path('products/', APIProductsListView.as_view()),
    path('products/<int:categoryID>', APIProductsByCategoryView.as_view()),
    path('category/add', APIProductCategoryAddView.as_view()),
]
