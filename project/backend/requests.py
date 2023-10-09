import requests
import os
import json
from .models import WeatherModel, CityModel


def request_func(city_id):
    if CityModel.objects.filter(pk=city_id).exists():
        latitude = CityModel.objects.get(pk=city_id).latitude
        longitude = CityModel.objects.get(pk=city_id).longitude

        key = os.getenv('X-Yandex-API-Key')
        url = f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}'
        headers = {'X-Yandex-API-Key': key}

        response = requests.get(url, headers=headers)
        data = response.text
        return data


def parseJSON_func(data):
    dataStr = json.loads(data)
    dataDict = {
        'unixTime': dataStr['now'],
        'city_by_res': dataStr['geo_object']['locality']['name'],
        'temp': dataStr['fact']['temp'],
        'pressureMM': dataStr['fact']['pressure_mm'],
        'windSpeed': dataStr['fact']['wind_speed']
    }
    return dataDict
