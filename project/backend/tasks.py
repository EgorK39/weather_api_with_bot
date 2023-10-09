from celery import shared_task
from .models import WeatherModel, CityModel


@shared_task
def add_task(city_id):
    order = WeatherModel.objects.get(city=city_id)
    order.isReady = False
    order.save()
