from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from products.views import APIProductCategoryAddView, ApiProductsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ApiProductsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category/add', APIProductCategoryAddView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
