from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import WeatherModel, CityModel


class CityModelCaseTest(TestCase):
    def setUp(self):
        CityModel.objects.create(cityName="калининград", latitude="54.71",
                                 longitude='20.51')

    def test_city_model(self):
        """ Проверяем корректность введенных данных. """
        cityName = CityModel.objects.get(pk=1).cityName
        latitude = CityModel.objects.get(pk=1).latitude
        longitude = CityModel.objects.get(pk=1).longitude
        self.assertEqual(cityName, 'калининград')
        self.assertEqual(latitude, '54.71')
        self.assertEqual(longitude, '20.51')


class ResponseCaseTest(APITestCase):
    def setUp(self):
        CityModel.objects.create(cityName="калининград", latitude="54.71",
                                 longitude='20.51')

    def test_create_account(self):
        response = self.client.get('http://127.0.0.1:8000/weather/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_url(self):
        response = self.client.get('http://127.0.0.1:8000/weather/?city=калининград')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WeatherModel.objects.get(pk=1).city.cityName, "калининград")
