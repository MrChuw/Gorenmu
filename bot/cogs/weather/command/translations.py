from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from bot.apis.weather import Forecast
from bot.cogs.weather.extras.code_parser import WeatherCode
from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .weather import WeatherCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: WeatherCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: WeatherCmd = parent
        self.populate_subclasses(parent=self)

    class Weather(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Weather"

        def city_not_passed(self, prefix: str) -> Response:
            text = self.get_text(self._cname, prefix=prefix)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def no_weather_found(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def user_has_no_city(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def city_not_found(self, city: str) -> Response:
            text = self.get_text(self._cname, city=city)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def hidden(self) -> str:
            return self.get_text(self._cname)

        def weather_from_codes(self, code: int, is_day: int) -> tuple[str, str] | str:
            base_path = Path(__file__).parent.parent / "extras"
            lang = self.ctx_get().user.get_lang()
            suffix = "br" if lang in ["pt_br", "pt"] else "en"

            codes_data = json.load((base_path / f"{suffix}_codes.json").open("r"))
            weather_codes = WeatherCode(codes_data)

            weather_info = weather_codes.get(code).get("day" if is_day == 1 else "night")
            if weather_info:
                return weather_info.description, weather_info.emoji
            return "Unknown weather code"

        def weather_wind_direction(self, angle: int, concise: bool) -> str:
            attrs = self.get_attributes_list(self._cname)
            directions = ["n", "ne", "l", "se", "s", "so", "o", "no", "n"]
            idx = int((angle + 22.5) / 45) % 8
            key = directions[idx]
            parts = next((attrs[item] for item in attrs if item == key), "Unknown, Unknown")
            return parts[1] if concise else parts[0]

        def weather(
            self,
            weather_obj: Forecast,
            index: int,
            city_name: str,
            weather_str: str,
            emoji: str,
            wind_direction: str,
        ) -> Response:
            w_curr = weather_obj.current_weather
            w_hour = weather_obj.hourly
            units = weather_obj.hourly_units

            precip_val = w_hour.precipitation[index]
            precip_string = ""
            if precip_val > 0:
                precip_string = self.get_text(
                    "weather_strings", attr="precip", val=precip_val, u_precip=units.precipitation
                )

            text = self.get_text(
                "weather_display",
                city=city_name,
                desc=weather_str.capitalize(),
                emoji=emoji.strip(),
                temp=w_curr.temperature,
                max=weather_obj.daily.temperature_2m_max[0],
                app=w_hour.apparent_temperature[index],
                u_temp=units.apparent_temperature,
                press=w_hour.pressure_msl[index],
                u_press=units.pressure_msl,
                hum=w_hour.relative_humidity_2m[index],
                u_hum=units.relative_humidity_2m,
                wind_spd=w_curr.wind_speed,
                u_wind_spd=units.wind_speed_10m,
                wind_dir=wind_direction,
                precip=precip_string,
            )

            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {
                        "args": self.get_text("cmd_ex1_args"),
                        "response": self.get_text("cmd_ex1_res"),
                    },
                    {
                        "args": self.get_text("cmd_ex2_args"),
                        "response": self.get_text("cmd_ex2_res"),
                    },
                    {
                        "args": self.get_text("cmd_ex3_args"),
                        "response": self.get_text("cmd_ex3_res"),
                    },
                    {
                        "args": self.get_text("cmd_ex4_args"),
                        "response": self.get_text("cmd_ex4_res"),
                    },
                    {
                        "prefix": self.get_text("cmd_ex5_prefix"),
                        "args": self.get_text("cmd_ex5_args"),
                        "response": self.get_text("cmd_ex5_res"),
                    },
                ]
            )

        def deco_admonitions(self, prefix: str = "!", *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "tip",
                        "position": "top",
                        "title": self.get_text("adm_title1"),
                        "message": self.get_text("adm_msg1"),
                    },
                    {
                        "admonition_type": "tip",
                        "position": "top",
                        "title": self.get_text("adm_title2"),
                        "message": self.get_text("adm_msg2", prefix=prefix),
                    },
                ]
            )

        # endregion

    Weather: Weather
