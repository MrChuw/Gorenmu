from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from typing import Any

from asyncio import timeout, timeout_at
from aiohttp.client import ClientError, ClientResponseError
from aiohttp_client_cache import CachedSession
from yarl import URL

from .exceptions import OpenMeteoConnectionError, OpenMeteoError
from .models import (
    DailyParameters,
    Forecast,
    Geocoding,
    HourlyParameters,
    PrecipitationUnit,
    TemperatureUnit,
    TimeFormat,
    WindSpeedUnit,
)


@dataclass
class OpenMeteo:
    """Main class for the Open-Meteo API."""

    def __init__(self, session: CachedSession):
        self.session = session

    # Request timeout in seconds.
    request_timeout: float = 10.0

    _close_session: bool = False

    async def _request(self, url: URL) -> dict[str, Any]:
        """Handle a request to the Open-Meteo API.

        A generic method for sending/handling HTTP requests done against
        the public Open-Meteo API.

        Args:
            url: URL to call.

        Returns:
            A Python dictionary (JSON decoded) with the response from
            the API.

        Raises:
            OpenMeteoConnectionError: An error occurred while communicating with
                the Open-Meteo API.
            OpenMeteoError: Received an unexpected response from the Open-Meteo
                API.
        """

        try:
            async with timeout(self.request_timeout):
                response = await self.session.get(url)
        except asyncio.TimeoutError as exception:
            raise OpenMeteoConnectionError("Timeout occurred while connecting to the Open-Meteo API") from exception
        except (ClientError, ClientResponseError, socket.gaierror) as exception:
            raise OpenMeteoConnectionError("Error occurred while communicating with Open-Meteo API") from exception
        content_type = response.headers.get("Content-Type", "")
        if (response.status // 100) in [4, 5]:
            if "application/json" in content_type:
                data = await response.json()
                response.close()
                if data.get("error") is True and (reason := data.get("reason")):
                    raise OpenMeteoError(reason)
                raise OpenMeteoError(response.status, data)
            contents = await response.read()
            response.close()
            raise OpenMeteoError(response.status, {"message": contents.decode("utf8")})

        if "application/json" not in content_type:
            text = await response.text()
            raise OpenMeteoError(
                "Unexpected response from the Open-Meteo API", {"Content-Type": content_type, "response": text}
            )

        return await response.json()

    async def forecast(
        self,
        *,
        latitude: float,
        longitude: float,
        timezone: str = "auto",
        current_weather: bool = False,
        daily: list[DailyParameters] | None = None,
        hourly: list[HourlyParameters] | None = None,
        past_days: int = 0,
        precipitation_unit: PrecipitationUnit = PrecipitationUnit.MILLIMETERS,
        temperature_unit: TemperatureUnit = TemperatureUnit.CELSIUS,
        timeformat: TimeFormat = TimeFormat.ISO_8601,
        wind_speed_unit: WindSpeedUnit = WindSpeedUnit.KILOMETERS_PER_HOUR,
    ) -> Forecast:
        url = URL("https://api.open-meteo.com/v1/forecast").with_query(
            current_weather="true" if current_weather else "false",
            daily=",".join(daily) if daily is not None else [],
            hourly=",".join(hourly) if hourly is not None else [],
            latitude=latitude,
            longitude=longitude,
            past_days=past_days,
            precipitation_unit=precipitation_unit,
            temperature_unit=temperature_unit,
            timeformat=timeformat,
            windspeed_unit=wind_speed_unit,
            timezone=timezone,
        )
        data = await self._request(url=url)
        return Forecast.model_validate(data)

    async def geocoding(self, *, name: str, language: str = "en") -> Geocoding:
        url = URL("https://nominatim.openstreetmap.org/search.php").with_query(
            q=name,  # name=name,
            # count=count,
            language=language,
            format="jsonv2",
        )
        data = await self._request(url=url)
        return Geocoding.model_validate({"results": data})

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> OpenMeteo:
        """Async enter.

        Returns:
            The OpenMeteo object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
