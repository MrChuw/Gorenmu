from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from bot.apis.weather import DailyParameters, HourlyParameters, OpenMeteo
from bot.ext import Context, Response, commands
from bot.models import User
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class WeatherCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.StringTools: StringTools = StringTools()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name='weather', aliases=['wt'])
    async def weather(self, ctx: Context, *, location: str = "") -> Response:
        from_chat = True
        location, from_user = self.StringTools.extract_and_remove_field(location, "user", False)
        user = None
        if from_user:
            user = await User.get_user_or_none(ctx, self.translations, name=from_user)
            if not user:
                return self.translations.Exceptions.user_not_found_name(name=from_user)
            if not user.city:
                return self.translations.Weather.user_has_no_city(from_user)
            from_chat = False
            location = user.city
        if ctx.user.city and not location:
            location = ctx.user.city
            from_chat = False

        is_private = not from_chat and (user or ctx.user).city_hidden
        safe_location_name = self.translations.Weather.hidden() if is_private else location
        if not location:
            return self.translations.Weather.city_not_passed(ctx.prefix)

        meteo = OpenMeteo(self.SessionsCaches.Weather.session)
        try:
            async with meteo as open_meteo:
                geocoding_result = await open_meteo.geocoding(name=location)
            if geocoding_result.results:
                city = geocoding_result.results[0]
            else:
                return self.translations.Weather.city_not_found(safe_location_name)
        except Exception as e:
            ctx.bot.log.error(e)
            return self.translations.Weather.city_not_found(safe_location_name)

        async with meteo as open_meteo:
            weather_obj = await open_meteo.forecast(
                latitude=city.latitude,
                longitude=city.longitude,
                current_weather=True,
                daily=[
                    DailyParameters.SUNRISE,
                    DailyParameters.SUNSET,
                    DailyParameters.PRECIPITATION_HOURS,
                    DailyParameters.TEMPERATURE_2M_MAX,
                ],
                hourly=[
                    HourlyParameters.APPARENT_TEMPERATURE,
                    HourlyParameters.TEMPERATURE_2M,
                    HourlyParameters.RELATIVE_HUMIDITY_2M,
                    HourlyParameters.PRESSURE_MSL,
                    HourlyParameters.WIND_SPEED_10M,
                    HourlyParameters.PRECIPITATION,
                    HourlyParameters.IS_DAY,
                ],
            )
        if not weather_obj.current_weather:
            return self.translations.Weather.no_weather_found(safe_location_name)
        hour = weather_obj.hourly.time
        index = min(range(len(hour)), key=lambda i: abs(hour[i] - datetime.datetime.now()))

        weather_str, emoji = self.translations.Weather.weather_from_codes(
            weather_obj.current_weather.weather_code, weather_obj.hourly.is_day[index]
        )
        wind_direction = self.translations.Weather.weather_wind_direction(
            weather_obj.current_weather.wind_direction, True
        )

        return self.translations.Weather.weather(
            weather_obj=weather_obj,
            index=index,
            city_name=safe_location_name if is_private else city.display,
            weather_str=weather_str,
            emoji=emoji,
            wind_direction=wind_direction,
        )


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(WeatherCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
