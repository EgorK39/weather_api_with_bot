from rest_framework import serializers
from .models import WeatherModel, CityModel


class WeatherSimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherModel
        fields = ['city',
                  'temp',
                  'pressureMM',
                  'windSpeed'
                  ]
        depth = 1


class WeatherSuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherModel
        fields = '__all__'
        depth = 1


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = '__all__'
