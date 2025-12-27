from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from bot.apis.weather import Forecast
from bot.cogs.weather.extras.code_parser import WeatherCode
from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Weather(TBase):
        def __init__(self):
            super().__init__()

        def city_not_passed(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "No city saved or sent, use {}savecity (city) (hide:true to hide the city) to save a city."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Nenhuma cidade salva ou enviada, use {}savecity (cidade) "
                    "(hide:true para esconder a cidade) para salvar uma cidade.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), ctx.prefix)

        def no_weather_found(self, ctx: Context, name: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'Weather not found for "{}".')
                self.lang_dict.add_with(["pt_br", "pt"], 'Não foi encontrado o tempo para "{}".')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def user_has_no_city(self, ctx: Context, name: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "User {} has no saved city.")
                self.lang_dict.add_with(["pt_br", "pt"], "Usuário {} não tem cidade salva.")
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def city_not_found(self, ctx: Context, city) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'city "{}" not found.')
                self.lang_dict.add_with(["pt_br", "pt"], 'cidade "{}" não encontrada.')
            return response.format_response(self._untangle_str(ctx, self._cname), city)

        def hidden(self, ctx: Context) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "(Hidden location)")
                self.lang_dict.add_with(["pt_br", "pt"], "(Localização escondida)")
            return self._untangle_str(ctx, self._cname)

        def weather_from_codes(self, ctx: Context, code: int, is_day: int) -> tuple[str, str] | str:
            with self.lang_dict.once(self._cname):
                base_path = Path(__file__).parent.parent / "extras"
                self.lang_dict.add_with("en", WeatherCode(json.load((base_path / "en_codes.json").open("r"))))
                self.lang_dict.add_with(
                    ["pt_br", "pt"], WeatherCode(json.load((base_path / "br_codes.json").open("r")))
                )

            weather_codes: WeatherCode = self._untangle_any(ctx, self._cname)
            weather_info = weather_codes.get(code).get("day" if is_day == 1 else "night")

            if weather_info:
                return weather_info.description, weather_info.emoji
            else:
                return "Unknown weather code"

        def weather_wind_direction(self, ctx: Context, angle: int, concise: bool) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    {
                        (337, 360): {0: "N", 1: "north"},
                        (0, 23): {0: "N", 1: "north"},
                        (23, 68): {0: "NE", 1: "north-east"},
                        (68, 113): {0: "E", 1: "east"},
                        (113, 158): {0: "SE", 1: "south-east"},
                        (158, 203): {0: "S", 1: "south"},
                        (203, 248): {0: "SW", 1: "south-west"},
                        (248, 293): {0: "W", 1: "west"},
                        (293, 337): {0: "NW", 1: "north-west"},
                    },
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    {
                        (337, 360): {0: "N", 1: "norte"},
                        (0, 23): {0: "N", 1: "norte"},
                        (23, 68): {0: "NE", 1: "nordeste"},
                        (68, 113): {0: "L", 1: "leste"},
                        (113, 158): {0: "SE", 1: "sudeste"},
                        (158, 203): {0: "S", 1: "sul"},
                        (203, 248): {0: "SO", 1: "sudoeste"},
                        (248, 293): {0: "O", 1: "oeste"},
                        (293, 337): {0: "NO", 1: "noroeste"},
                    },
                )
            weather_wind_directions: dict[tuple[int, int], dict[int, str]] = self._untangle_any(ctx, self._cname)

            angle %= 360
            for (start, end), direction in weather_wind_directions.items():
                if start <= angle < end:
                    return direction[1 if concise else 0]
            return "Unknown direction"

        def weather_strings(self, ctx: Context) -> list[str]:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    [
                        "temperature of {} {}, maximum of {} {} and apparent temperature of {} {}, ",
                        ", and precipitation of {} {}",
                    ],
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    ["temperatura de {} {}, máxima de {} {} e aparente de {} {}, ", ", e precipitação de {} {}"],
                )
            return self._untangle_any(ctx, self._cname)

        def weather(
            self,
            ctx: Context,
            weather_obj: Forecast,
            index: int,
            city_name: str,
            weather_str: str,
            emoji: str,
            wind_direction: str,
        ) -> Response:
            weather_strings = self.weather_strings(ctx)
            w_curr = weather_obj.current_weather
            w_hour = weather_obj.hourly
            units = weather_obj.hourly_units
            temp_info = weather_strings[0].format(
                w_curr.temperature,
                units.apparent_temperature,
                weather_obj.daily.temperature_2m_max[0],
                units.apparent_temperature,
                w_hour.apparent_temperature[index],
                units.apparent_temperature,
            )
            precip_val = w_hour.precipitation[index]
            precip_string = ""
            if precip_val > 0:
                precip_string = f" {weather_strings[1].format(precip_val, units.precipitation)}"

            parts = [
                f"{city_name}.",
                f"{weather_str.capitalize()} {emoji.strip()},",
                temp_info,
                f"{w_hour.pressure_msl[index]} {units.pressure_msl},",
                f"{w_hour.relative_humidity_2m[index]}{units.relative_humidity_2m},",
                f"{w_curr.wind_speed}{units.wind_speed_10m} {wind_direction}{precip_string}",
            ]

            return Response(ctx=ctx, success=True, response_string=" ".join(parts))

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Enter the command and a city to get the weather forecast.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Digite o comando e uma cidade para obter a previsão do tempo."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}weather (location)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}weather (localização)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Enter the command and a city to get the weather forecast.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Digite o comando e uma cidade para obter a previsão do tempo."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "args": "wt fortaleza",
                                "response": "Fortaleza, Ceará, Brazil. Cloudy ☁️ , temperature of 26.5 °C, "
                                "maximum of 32.7 °C and apparent temperature of 30.4 °C, 1011.4 hPa, 79%, 7.6km/h east",
                            },
                            {
                                "args": "wt georgia, georgia",
                                "response": "Georgia, Georgia. Cloudy ☁️ , temperature of -3.8 °C, maximum of -2.4 °C "
                                "and apparent temperature of -6.7 °C, 1023.4 hPa, 93%, 2.1km/h north-west",
                            },
                            {
                                "args": "wt 61700-000",
                                "response": "61700-000, Aquiraz, Ceará, Brazil. Cloudy ☁️ , "
                                "temperature of 25.6 °C, maximum of 32.6 °C and apparent temperature of "
                                "30.2 °C, 1011.5 hPa, 83%, 4.6km/h north-east",
                            },
                            {
                                "args": "wt Vicolo di Cecilio Giocondo, 2, 80045 Pompei NA, Itália",
                                "response": "Vicolo di Cecilio Giocondo, Pompei, Campania, Italy. Partly cloudy ⛅ , "
                                "temperature of 13.9 °C, maximum of 15.3 °C and apparent temperature of 12.3 °C, "
                                "1020.1 hPa, 58%, 6.6km/h north-east",
                            },
                            {
                                "args": "wt 40.7521725, 14.4862460",
                                "response": "Casa di Cecilio Giocondo, Pompei, Campania, Italy. Partly cloudy ⛅ , "
                                "temperature of 13.9 °C, maximum of 15.3 °C and apparent temperature of 12.3 °C, "
                                "1020.1 hPa, 58%, 6.6km/h north-east",
                            },
                            {
                                "prefix": "Locations can be hidden.",
                                "args": "wt",
                                "response": "(Hidden location) Clear 🌙 , temperature of 1.5 °C, maximum of 6.9 °C and "
                                "apparent temperature of -3.0 °C, 1017.1 hPa, 45%, 8.4km/h north-west",
                            },
                            {
                                "prefix": "User locations will always be hidden.",
                                "args": "wt user:gorenmu",
                                "response": "(Hidden location) Cloudy ☁️ , temperature of 25.2 °C, maximum of 30.3 °C "
                                "and apparent temperature of 34.9 °C, 1009.0 hPa, 68%, 2.1km/h north-west",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "args": "wt fortaleza",
                                "response": "Fortaleza, Ceará, Brazil. Nublado ☁️ , temperatura de 26.5 °C, "
                                "máxima de 32.7 °C e aparente de 30.4 °C, 1011.4 hPa, 79%, 7.6km/h leste",
                            },
                            {
                                "args": "wt georgia, georgia",
                                "response": "Georgia, Georgia. Nublado ☁️ , temperatura de -3.8 °C, máxima de -2.4 °C "
                                "e aparente de -6.7 °C, 1023.4 hPa, 93%, 2.1km/h noroeste",
                            },
                            {
                                "args": "wt 61700-000",
                                "response": "61700-000, Aquiraz, Ceará, Brazil. Nublado ☁️ , "
                                "temperatura de 25.6 °C, máxima de 32.6 °C e aparente de "
                                "30.2 °C, 1011.5 hPa, 83%, 4.6km/h nordeste",
                            },
                            {
                                "args": "wt Vicolo di Cecilio Giocondo, 2, 80045 Pompei NA, Itália",
                                "response": "Vicolo di Cecilio Giocondo, Pompei, Campania, Italy. "
                                "Parcialmente nublado ⛅ , temperatura de 13.9 °C, máxima de 15.3 °C "
                                "e aparente de 12.3 °C, 1020.1 hPa, 58%, 6.6km/h nordeste",
                            },
                            {
                                "args": "wt 40.7521725, 14.4862460",
                                "response": "Casa di Cecilio Giocondo, Pompei, Campania, Italy. "
                                "Parcialmente nublado ⛅ , temperatura de 13.9 °C, máxima de 15.3 °C "
                                "e aparente de 12.3 °C, 1020.1 hPa, 58%, 6.6km/h nordeste",
                            },
                            {
                                "prefix": "As localizações podem ser ocultadas.",
                                "args": "wt",
                                "response": "(Localização oculta) Limpo 🌙 , temperatura de 1.5 °C, máxima de 6.9 °C e "
                                "aparente de -3.0 °C, 1017.1 hPa, 45%, 8.4km/h noroeste",
                            },
                            {
                                "prefix": "A localização de outros usuários sempre sera escondida.",
                                "args": "wt user:gorenmu",
                                "response": "(Localização oculta) Nublado ☁️ , temperatura de 25.2 °C, "
                                "máxima de 30.3 °C e aparente de 34.9 °C, 1009.0 hPa, 68%, 2.1km/h noroeste",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    Admonitions(
                        [
                            {
                                "admonition_type": "tip",
                                "position": "top",
                                "title": "Set city",
                                "message": "You can use /whisper gorenmu +set city (city name) to save a city "
                                "without needing to send a message in the chat.",
                            },
                            {
                                "admonition_type": "tip",
                                "position": "top",
                                "title": "Hide location.",
                                "message": "By default, the city will be saved as hidden when using "
                                '{prefix}set city (city name) adding "hidden:false" to show in the chat.',
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "tip",
                                "position": "top",
                                "title": "Definir cidade",
                                "message": "Você pode usar /whisper gorenmu +set city (nome da cidade) para salvar "
                                "uma cidade sem precisar enviar uma mensagem no chat.",
                            },
                            {
                                "admonition_type": "tip",
                                "position": "top",
                                "title": "Ocultar localização",
                                "message": "Por padrão, a cidade será salva como oculta ao usar "
                                '{prefix}set city (nome da cidade). Adicione "hidden:false" para exibir no chat.',
                            },
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Weather: Weather
