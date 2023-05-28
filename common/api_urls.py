from django.urls import path

from products.views import (APIProductCategoryAddView, APIProductsByCategory,
                            APIProductsListView)

urlpatterns = [
    path('products/', APIProductsListView.as_view()),
    path('products/<int:categoryID>', APIProductsByCategory.as_view()),
    path('category/add', APIProductCategoryAddView.as_view()),
]
