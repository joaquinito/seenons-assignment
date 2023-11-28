"""
URL mappings for the REST APIs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StreamsViewSet, AssetsViewSet, LogisticServiceProvidersViewSet, LSPProductsViewSet, LSPTimeslotsViewSet, ProductsViewSet



router = DefaultRouter()
router.register('streams', StreamsViewSet)
router.register('assets', AssetsViewSet)
router.register('logistic_service_providers', LogisticServiceProvidersViewSet)
router.register('lsp_products', LSPProductsViewSet)
router.register('lsp_timeslots', LSPTimeslotsViewSet)

app_name = 'rest_api'

urlpatterns = [path('', include(router.urls)),
               path('products/', ProductsViewSet.as_view(), name='products')]