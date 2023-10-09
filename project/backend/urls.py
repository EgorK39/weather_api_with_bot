from django.urls import path, include
from rest_framework import routers

from .views import WeatherViewSet

router = routers.SimpleRouter()
router.register(r'weather', WeatherViewSet, basename='weathermodel')

urlpatterns = [
    path('', include(router.urls)),
]
