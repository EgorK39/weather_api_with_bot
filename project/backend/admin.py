from django.contrib import admin

from .models import WeatherModel, CityModel

admin.site.register(WeatherModel)
admin.site.register(CityModel)
