"""
URL mappings for the REST APIs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_api import views



router = DefaultRouter()
router.register('streams', views.StreamsViewSet)

app_name = 'rest_api'

urlpatterns = [path('', include(router.urls))]