"""
URL mappings for the REST APIs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomersViewSet, StreamsViewSet, AssetsViewSet, \
    LogisticServiceProvidersViewSet, LSPProductsViewSet, LSPTimeslotsViewSet, ProductsViewSet


router = DefaultRouter()
router.register('customers', CustomersViewSet)
router.register('streams', StreamsViewSet)
router.register('assets', AssetsViewSet)
router.register('logistic_service_providers', LogisticServiceProvidersViewSet)
router.register('lsp_products', LSPProductsViewSet)
router.register('lsp_timeslots', LSPTimeslotsViewSet)
router.register('products', ProductsViewSet, basename='products')

app_name = 'rest_api'

urlpatterns = [path('', include(router.urls))]
