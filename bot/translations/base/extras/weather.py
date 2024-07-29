from __future__ import annotations

from typing import Any, Dict, Union


class WeatherTools:
    weather_codes: dict[int | Any, dict[str, dict[str, str]]]
    weather_wind_directions: dict[tuple[int, int], dict[int, str]]

    @staticmethod
    def weather_from_codes(
        code: int, is_day: int, weather_codes: dict[int | Any, dict[str, dict[str, str]]]
    ) -> Union[Dict[str, str], str]:
        time_of_day = "day" if is_day is 1 else "night"
        weather_info = weather_codes.get(code, 99999).get(time_of_day, None)
        if weather_info:
            return {"description": weather_info.get("description"), "emoji": weather_info.get("emoji")}
        else:
            return "Unknown weather code"

    @staticmethod
    def weather_wind_direction(
        angle: int, concise: bool, weather_wind_directions: dict[tuple[int, int], dict[int, str]]
    ) -> str:
        angle = angle % 360
        for (start, end), direction in weather_wind_directions.items():
            if start <= angle < end or (start > end and (angle >= start or angle < end)):
                return direction[concise]
        return "Unknown direction"
