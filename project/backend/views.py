from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from .models import WeatherModel, CityModel
from .serializers import (
    WeatherSuperUserSerializer, CitySerializer,
    WeatherSimpleUserSerializer
)

from .requests import request_func, parseJSON_func
from .tasks import add_task


class WeatherViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = WeatherModel.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return WeatherSuperUserSerializer
        else:
            return WeatherSimpleUserSerializer

    def list(self, request, *args, **kwargs):
        if request.GET.get('city'):
            city = request.GET.get('city').lower()
            if CityModel.objects.filter(cityName=city).exists():
                city_id = CityModel.objects.get(cityName=city).pk

                if WeatherModel.objects.filter(city=city_id).exists():
                    if WeatherModel.objects.get(city=city_id).isReady:
                        print('уже есть такой город')
                        add_task.apply_async(
                            [city_id],
                            countdown=60 * 30
                        )
                    else:
                        data = request_func(city_id)
                        dataPy = parseJSON_func(data)

                        # WeatherModel.objects.filter(city=city_id).update(
                        #     isReady=True,
                        #     city=CityModel.objects.get(pk=city_id),
                        #     temp=dataPy.get("temp"),
                        #     pressureMM=dataPy.get("pressureMM"),
                        #     windSpeed=dataPy.get("windSpeed"),
                        #     unixTime=dataPy.get("unixTime")
                        # ) fixme

                        weather_model = WeatherModel.objects.get(city=city_id)
                        weather_model.isReady = True
                        weather_model.city = CityModel.objects.get(pk=city_id)
                        weather_model.temp = dataPy.get("temp")
                        weather_model.pressureMM = dataPy.get("pressureMM")
                        weather_model.windSpeed = dataPy.get("windSpeed")
                        weather_model.unixTime = dataPy.get("unixTime")
                        weather_model.save()

                        add_task.apply_async(
                            [city_id],
                            countdown=60 * 30
                        )

                else:
                    data = request_func(city_id)
                    dataPy = parseJSON_func(data)
                    WeatherModel.objects.create(
                        isReady=True,
                        city=CityModel.objects.get(pk=city_id),
                        temp=dataPy.get("temp"),
                        pressureMM=dataPy.get("pressureMM"),
                        windSpeed=dataPy.get("windSpeed"),
                        unixTime=dataPy.get("unixTime")
                    )
                    add_task.apply_async(
                        [city_id],
                        countdown=60 * 30
                    )

                queryset = WeatherModel.objects.filter(city=city_id).order_by("-unixTime")
                page = self.paginate_queryset(queryset)

                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response(
                    {'CityError': 'Указанного города нет в списке. Попробуйте еще раз, например, "Калининград"'},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            # return HttpResponse("Произошла ошибка", status=status.HTTP_400_BAD_REQUEST, reason="Incorrect data")
            return Response(
                {'Error': "Неверно указан адрес. Попробуйте: http://127.0.0.1:8000/weather/?city=Калининград"},
                status=status.HTTP_400_BAD_REQUEST)
