# -*- coding: utf-8 -*-
from .response import BaseFunctions


class WeatherTools(BaseFunctions):
    def __init__(self, obj):
        super().__init__(obj, None)
        self.weather_codes = self._generate_weather_codes(BaseFunctions(self.get_base("Weather Codes"), None))
        self.cardinais = self._generate_wind_direction(BaseFunctions(self.get_base("Cardinals"), None))
        self.wmo_codes = self._generate_codes(BaseFunctions(self.get_base("WMO Codes"), None))
        del self.fallback, self.obj

    @staticmethod
    def _generate_weather_codes(codes: BaseFunctions):
        return {int(code): codes.get_object(code) for code in codes}

    @staticmethod
    def _generate_wind_direction(names: BaseFunctions) -> dict:
        cardinals = {}
        for cardinal in names:
            cardinal = names.get_object(cardinal)
            angle = tuple(int(ang) for ang in cardinal["angles"])
            short = cardinal["short"]
            long = cardinal["long"]
            cardinals[angle] = {0: short, 1: long}
        return cardinals

    @staticmethod
    def _generate_codes(codes: BaseFunctions):
        return {int(code): codes.get_object(code) for code in codes}
