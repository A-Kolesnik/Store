from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from products.views import (APIProductCategoryAddView, APIProductsByCategoryView,
                            APIProductsListView)

urlpatterns = [
    path('products/', APIProductsListView.as_view()),
    path('products/<int:categoryID>', APIProductsByCategoryView.as_view()),
    path('category/add', APIProductCategoryAddView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
