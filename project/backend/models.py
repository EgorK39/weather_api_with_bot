from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

""" WeatherModel """


def validate_unix_time(value):
    if not value.isdigit():
        raise ValidationError(
            _("%(value)s должна быть цифровым значением"),
            params={"value": value},
        )
    if len(value) < 10:
        raise ValidationError(
            _("%(value)s символов должно быть больше 9"),
            params={"value": value},
        )


class WeatherModel(models.Model):
    isReady = models.BooleanField(default=False, blank=True)
    city = models.ForeignKey("CityModel", on_delete=models.CASCADE)
    temp = models.FloatField(db_column="Температура")
    pressureMM = models.IntegerField(db_column="Давление")
    windSpeed = models.FloatField(db_column="Ветер")
    nowIs = models.DateTimeField(auto_now=True)
    unixTime = models.CharField(max_length=54, validators=[validate_unix_time])

    def clean(self, *args, **kwargs):
        if self.temp >= 80 or self.temp < -80:
            raise ValidationError(
                _("%(value)s: Температура не может быть меньше -80 и более 80"),
                params={"value": self.temp},
            )
        if self.pressureMM >= 850 or self.pressureMM < 650:
            raise ValidationError(
                _("%(value)s: укажите корректные данные показателя давления"),
                params={"value": self.pressureMM},
            )
        if self.windSpeed > 40 or self.windSpeed < 0:
            raise ValidationError(
                _("%(value)s: Скорость ветра не можеть быть меньше 0 и более 40"),
                params={"value": self.windSpeed},
            )
        super(WeatherModel, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.clean()
        super(WeatherModel, self).save(*args, **kwargs)

    def __str__(self):
        return "Температура: %s" % self.temp


""" CityModel """


def validate_num(value):
    if len(value) == 5:
        if not re.fullmatch(r'\d{2}[.]\d{2}', value):
            raise ValidationError(
                _("%(value)s поле должно быть заполнено по образцу: 12.21"),
                params={"value": value},
            )
    elif len(value) == 6:
        if not re.fullmatch(r'\d{3}[.]\d{2}', value):
            raise ValidationError(
                _("%(value)s поле должно быть заполнено по образцу: 131.87"),
                params={"value": value},
            )
    else:
        raise ValidationError(
            _("%(value)s поле должно содержать от 5 до 6 символов по образцу: 78.87"),
            params={"value": value},
        )


def validate_coords(value):
    validate_num(value)


def check_err(value):
    validate_num(value)


class CityModel(models.Model):
    cityName = models.CharField(max_length=64, unique=True)
    latitude = models.CharField(max_length=5, validators=[validate_coords])
    longitude = models.CharField(max_length=6, validators=[validate_coords])

    def clean(self, *args, **kwargs):
        for letter in range(len(self.cityName)):
            if self.cityName[letter].isalpha() and not self.cityName[letter].islower():
                raise ValidationError(
                    _("%(value)s: название города должно быть написано в нижнем регистре. Пример: %(value_two)s"),
                    params={"value": self.cityName, "value_two": self.cityName.lower()},
                )
        check_err(self.latitude)
        check_err(self.longitude)
        super(CityModel, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.clean()
        super(CityModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"Название города: {self.cityName}"
