from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from products.views import APIProductCategoryViewSet, ApiProductsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ApiProductsViewSet)
router.register('category', APIProductCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
