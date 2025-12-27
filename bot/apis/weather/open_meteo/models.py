from __future__ import annotations

from datetime import date, datetime
from enum import Enum, auto
from typing import Any, Dict

ISO3166_LVL_MAP: dict[str, str] = {
    "lvl2": "country",
    "lvl3": "region",
    "lvl4": "state",
    "lvl5": "state_district",
    "lvl6": "province",
    "lvl7": "county",
    "lvl8": "municipality",
    "lvl9": "city_district",
}


class StrEnum(str, Enum):
    """An Enum of strings.

    A backported StrEnum implementation of Python 3.11, providing roughly the
    same implementation for our use case. The `auto()` behavior uses the
    lowercase version of its member name for its value.

        Example:
        class Example(StrEnum):
            UPPER_CASE = auto()
            NOT_AUTO = "beep"

            # We should not use these, but they work
            lower_case = auto()
            MixedCase = auto()

        assert Example.UPPER_CASE == "upper_case"
        assert Example.NOT_AUTO == "beep"

        assert Example.lower_case == "lower_case"
        assert Example.MixedCase == "MixedCase"
    """

    def __new__(cls, value: str, *args: Any, **kwargs: Any) -> StrEnum:
        """Validate StrEnum creation.

        Args:
            value: Value of the member.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            The StrEnum instance.

        Raises:
            TypeError: If the value is not a string.
        """
        if not isinstance(value, (str, auto)):
            raise TypeError(f"Values of StrEnums must be strings: {value!r} is a {type(value)}")
        return super().__new__(cls, value, *args, **kwargs)  # type: ignore

    def __str__(self) -> str:
        """Represent as a string.

        Returns:
            Value of the member as a string.
        """
        return str(self.value)

    @staticmethod
    def _generate_next_value_(  # pylint: disable=arguments-differ
        name: str, _start: Any, _count: Any, _last_values: Any
    ) -> str:
        """Generate the next value when not given.

        Args:
            name: the name of the member
            _start: the initial start value or None
            _count: the number of existing members
            _last_values: the last value assigned or None

        Returns:
            The next value for the member.
        """
        return name.lower()


class TemperatureUnit(StrEnum):
    """Enum to represent the temperature units available."""

    CELSIUS = auto()
    FAHRENHEIT = auto()


class WindSpeedUnit(StrEnum):
    """Enum to represent the wind speed units available."""

    KILOMETERS_PER_HOUR = "kmh"
    KNOTS = "kn"
    METERS_PER_SECOND = "ms"
    MILES_PER_HOUR = "mph"


class PrecipitationUnit(StrEnum):
    """Enum to represent the precipitation units available."""

    MILLIMETERS = "mm"
    INCHES = "in"


class TimeFormat(StrEnum):
    """Enum to represent the time formats available."""

    ISO_8601 = "iso8601"
    UNIXTIME = "unixtime"


class HourlyParameters(StrEnum):
    """Enum to represent the hourly parameters available."""

    # If is day or night
    IS_DAY = "is_day"

    # Air temperature at 2 meters above ground
    APPARENT_TEMPERATURE = "apparent_temperature"

    # Total cloud cover as an area fraction
    CLOUD_COVER = "cloudcover"

    # High level clouds from 8 km altitude
    CLOUD_COVER_HIGH = "cloudcover_high"

    # Low level clouds and fog up to 3 km altitude
    CLOUD_COVER_LOW = "cloudcover_low"

    # Mid level clouds from 3 to 8 km altitude
    CLOUD_COVER_MID = "cloudcover_mid"

    # Dew point temperature at 2 meters above ground
    DEW_POINT_2M = "dewpoint_2m"

    # Diffuse solar radiation as average of the preceding hour
    DIFFUSE_RADIATION = "diffuse_radiation"

    # Direct solar radiation as average of the preceding hour on the horizontal
    # plane and the normal plane (perpendicular to the sun)
    DIRECT_NORMAL_IRRADIANCE = "direct_normal_irradiance"
    DIRECT_RADIATION = "direct_radiation"

    # Sum of evapotranspration of the preceding hour
    # from lands urface and plants
    EVAPOTRANSPIRATION = "evapotranspiration"

    # Altitude above sea level of the 0°C level
    FREEZING_LEVEL_HEIGHT = "freezinglevel_height"

    # Total precipitation (rain, showers, snow) sum of the preceding hour
    PRECIPITATION = "precipitation"

    # Atmospheric air pressure reduced to sea level (hPa)
    PRESSURE_MSL = "pressure_msl"

    # Relative humidity at 2 meters above ground
    RELATIVE_HUMIDITY_2M = "relativehumidity_2m"

    # Shortwave solar radiation as average of the preceding hour
    SHORTWAVE_RADIATION = "shortwave_radiation"

    # Snow depth on the ground
    SNOW_DEPTH = "snow_depth"

    # Average soil water content as volumetric mixing ratio at 0-1, 1-3, 3-9,
    # 9-27 and 27-81 cm depths.
    SOIL_MOISTURE_0_1CM = "soil_moisture_0_1cm"
    SOIL_MOISTURE_1_3CM = "soil_moisture_1_3cm"
    SOIL_MOISTURE_27_81CM = "soil_moisture_27_81cm"
    SOIL_MOISTURE_3_9CM = "soil_moisture_3_9cm"
    SOIL_MOISTURE_9_27CM = "soil_moisture_9_27cm"

    # Temperature in the soil at 0, 6, 18 and 54 cm depths. 0 cm is the surface
    # temperature on land or water surface temperature on water.
    SOIL_TEMPERATURE_0CM = "soil_temperature_0cm"
    SOIL_TEMPERATURE_18CM = "soil_temperature_18cm"
    SOIL_TEMPERATURE_54CM = "soil_temperature_54cm"
    SOIL_TEMPERATURE_6CM = "soil_temperature_6cm"

    # Air temperature at 2 meters above ground
    TEMPERATURE_2M = "temperature_2m"

    # Vapor Pressure Deificit (VPD) in kilo pascal (kPa). For high VPD (>1.6),
    # water transpiration of plants increases. For low VPD (<0.4),
    # transpiration decreases.
    VAPOR_PRESSURE_DEFICIT = "vapor_pressure_deficit"

    # Weather condition as a WMO numeric weather code.
    WEATHER_CODE = "weather_code"

    # Wind direction at 10, 80, 120 or 180 meters above ground
    WIND_DIRECTION_10M = "winddirection_10m"
    WIND_DIRECTION_120M = "winddirection_120m"
    WIND_DIRECTION_180M = "winddirection_180m"
    WIND_DIRECTION_80M = "winddirection_80m"

    # Gusts at 10 meters above ground as a maximum of the preceding hour
    WIND_GUSTS_10M = "windgusts_10m"

    # Wind speed at 10, 80, 120 or 180 meters above ground.
    # Wind speed on 10 meters is the standard level.
    WIND_SPEED_10M = "windspeed_10m"
    WIND_SPEED_120M = "windspeed_120m"
    WIND_SPEED_180M = "windspeed_180m"
    WIND_SPEED_80M = "windspeed_80m"


class DailyParameters(StrEnum):
    """Enum to represent the daily parameters available."""

    # Maximum and minimum daily air temperature at 2 meters above ground.
    APPARENT_TEMPERATURE_MAX = "apparent_temperature_max"
    APPARENT_TEMPERATURE_MIN = "apparent_temperature_min"

    # The number of hours with rain,
    PRECIPITATION_HOURS = "precipitation_hours"

    # Sum of daily precipitation.
    PRECIPITATION_SUM = "precipitation_sum"

    # The sum of solar radiation on a given day in Mega Joules.
    SHORTWAVE_RADIATION_SUM = "shortwave_radiation_sum"

    # Sun rise and set times
    SUNRISE = "sunrise"
    SUNSET = "sunset"

    # Maximum and minimum daily air temperature at 2 meters above ground.
    TEMPERATURE_2M_MAX = "temperature_2m_max"
    TEMPERATURE_2M_MIN = "temperature_2m_min"

    # The most severe weather condition on a given day.
    WEATHER_CODE = "weather_code"

    # Dominant wind direction.
    WIND_DIRECTION_10M_DOMINANT = "winddirection_10m_dominant"

    # Maximum wind speed and gusts on a day
    WIND_GUSTS_10M_MAX = "windgusts_10m_max"
    WIND_SPEED_10M_MAX = "windspeed_10m_max"


class HourlyForecast:
    def __init__(self, data: dict[str, Any]):
        # Time markers
        raw_time = data.get("time")
        self.time: list[datetime] | None = [datetime.fromisoformat(t) for t in raw_time] if raw_time else None

        # General Atmosphere
        self.temperature_2m: list[float] | None = data.get("temperature_2m")
        self.apparent_temperature: list[float] | None = data.get("apparent_temperature")
        self.pressure_msl: list[float] | None = data.get("pressure_msl")
        self.vapor_pressure_deficit: list[float] | None = data.get("vapor_pressure_deficit")
        self.freezing_level_height: list[int] | None = data.get("freezinglevel_height")
        self.weather_code: list[int] | None = data.get("weathercode")
        self.is_day: list[int] | None = data.get("is_day")

        # Humidity and Clouds
        self.relative_humidity_2m: list[int] | None = data.get("relativehumidity_2m")
        self.dew_point_2m: list[float] | None = data.get("dewpoint_2m")
        self.cloud_cover: list[int] | None = data.get("cloudcover")
        self.cloud_cover_low: list[int] | None = data.get("cloudcover_low")
        self.cloud_cover_mid: list[int] | None = data.get("cloudcover_mid")
        self.cloud_cover_high: list[int] | None = data.get("cloudcover_high")

        # Precipitation and Radiation
        self.precipitation: list[float] | None = data.get("precipitation")
        self.snow_depth: list[int] | None = data.get("snow_depth")
        self.evapotranspiration: list[float] | None = data.get("evapotranspiration")
        self.shortwave_radiation: list[float] | None = data.get("shortwave_radiation")
        self.diffuse_radiation: list[float] | None = data.get("diffuse_radiation")
        self.direct_radiation: list[float] | None = data.get("direct_radiation")
        self.direct_normal_irradiance: list[float] | None = data.get("direct_normal_irradiance")

        # Soil Metrics
        self.soil_moisture_0_1cm: list[float] | None = data.get("soil_moisture_0_1cm")
        self.soil_moisture_1_3cm: list[float] | None = data.get("soil_moisture_1_3cm")
        self.soil_moisture_3_9cm: list[float] | None = data.get("soil_moisture_3_9cm")
        self.soil_moisture_9_27cm: list[float] | None = data.get("soil_moisture_9_27cm")
        self.soil_moisture_27_81cm: list[float] | None = data.get("soil_moisture_27_81cm")
        self.soil_temperature_0cm: list[float] | None = data.get("soil_temperature_0cm")
        self.soil_temperature_6cm: list[float] | None = data.get("soil_temperature_6cm")
        self.soil_temperature_18cm: list[float] | None = data.get("soil_temperature_18cm")
        self.soil_temperature_54cm: list[float] | None = data.get("soil_temperature_54cm")

        # Wind Speed
        self.wind_speed_10m: list[float] | None = data.get("windspeed_10m")
        self.wind_speed_80m: list[float] | None = data.get("windspeed_80m")
        self.wind_speed_120m: list[float] | None = data.get("windspeed_120m")
        self.wind_speed_180m: list[float] | None = data.get("windspeed_180m")
        self.wind_gusts_10m: list[float] | None = data.get("windgusts_10m")

        # Wind Direction
        self.wind_direction_10m: list[int] | None = data.get("winddirection_10m")
        self.wind_direction_80m: list[int] | None = data.get("winddirection_80m")
        self.wind_direction_120m: list[int] | None = data.get("winddirection_120m")
        self.wind_direction_180m: list[int] | None = data.get("winddirection_180m")


class DailyForecast:
    def __init__(self, data: dict[str, Any]):
        # Time identifiers (usually a list of ISO8601 strings or date objects)
        raw_time = data.get("time")
        self.time: list[date] | None = [date.fromisoformat(t) for t in raw_time] if raw_time else None

        # Temperature lists
        self.temperature_2m_max: list[float] | None = data.get("temperature_2m_max")
        self.temperature_2m_min: list[float] | None = data.get("temperature_2m_min")
        self.apparent_temperature_max: list[float] | None = data.get("apparent_temperature_max")
        self.apparent_temperature_min: list[float] | None = data.get("apparent_temperature_min")

        # Precipitation and Radiation
        self.precipitation_hours: list[int] | None = data.get("precipitation_hours")
        self.precipitation_sum: list[float] | None = data.get("precipitation_sum")
        self.shortwave_radiation_sum: list[float] | None = data.get("shortwave_radiation_sum")

        # Solar events
        self.sunrise: list[datetime] | None = data.get("sunrise")
        self.sunset: list[datetime] | None = data.get("sunset")

        # Weather and Wind (Mapping Pydantic aliases)
        self.weather_code: list[int] | None = data.get("weathercode")
        self.wind_direction_10m_dominant: list[int] | None = data.get("winddirection_10m_dominant")
        self.wind_gusts_10m_max: list[float] | None = data.get("windgusts_10m_max")
        self.wind_speed_10m_max: list[float] | None = data.get("windspeed_10m_max")


class HourlyForecastUnits:
    def __init__(self, data: dict[str, Any]):
        # General and Atmosphere
        self.time: TimeFormat | None = data.get("time")
        self.temperature_2m: str | None = data.get("temperature_2m")
        self.apparent_temperature: str | None = data.get("apparent_temperature")
        self.pressure_msl: str | None = data.get("pressure_msl")
        self.vapor_pressure_deficit: str | None = data.get("vapor_pressure_deficit")
        self.freezing_level_height: str | None = data.get("freezinglevel_height")
        self.weather_code: str | None = data.get("weathercode")

        # Humidity and Clouds (with Aliases)
        self.relative_humidity_2m: str | None = data.get("relativehumidity_2m")
        self.dew_point_2m: str | None = data.get("dewpoint_2m")
        self.cloud_cover: str | None = data.get("cloudcover")
        self.cloud_cover_low: str | None = data.get("cloudcover_low")
        self.cloud_cover_mid: str | None = data.get("cloudcover_mid")
        self.cloud_cover_high: str | None = data.get("cloudcover_high")

        # Precipitation and Radiation
        self.precipitation: str | None = data.get("precipitation")
        self.snow_depth: str | None = data.get("snow_depth")
        self.evapotranspiration: str | None = data.get("evapotranspiration")
        self.shortwave_radiation: str | None = data.get("shortwave_radiation")
        self.diffuse_radiation: str | None = data.get("diffuse_radiation")
        self.direct_radiation: str | None = data.get("direct_radiation")
        self.direct_normal_irradiance: str | None = data.get("direct_normal_irradiance")

        # Soil Metrics
        self.soil_moisture_0_1cm: str | None = data.get("soil_moisture_0_1cm")
        self.soil_moisture_1_3cm: str | None = data.get("soil_moisture_1_3cm")
        self.soil_moisture_3_9cm: str | None = data.get("soil_moisture_3_9cm")
        self.soil_moisture_9_27cm: str | None = data.get("soil_moisture_9_27cm")
        self.soil_moisture_27_81cm: str | None = data.get("soil_moisture_27_81cm")
        self.soil_temperature_0cm: str | None = data.get("soil_temperature_0cm")
        self.soil_temperature_6cm: str | None = data.get("soil_temperature_6cm")
        self.soil_temperature_18cm: str | None = data.get("soil_temperature_18cm")
        self.soil_temperature_54cm: str | None = data.get("soil_temperature_54cm")

        # Wind Speed (Multiple Heights)
        self.wind_speed_10m: str | None = data.get("windspeed_10m")
        self.wind_speed_80m: str | None = data.get("windspeed_80m")
        self.wind_speed_120m: str | None = data.get("windspeed_120m")
        self.wind_speed_180m: str | None = data.get("windspeed_180m")
        self.wind_gusts_10m: str | None = data.get("windgusts_10m")

        # Wind Direction (Multiple Heights)
        self.wind_direction_10m: str | None = data.get("winddirection_10m")
        self.wind_direction_80m: str | None = data.get("winddirection_80m")
        self.wind_direction_120m: str | None = data.get("winddirection_120m")
        self.wind_direction_180m: str | None = data.get("winddirection_180m")


class CurrentWeather:
    def __init__(self, data: dict[str, Any]):
        # The 'time' field is expected to be a datetime object, or a string
        # that would be parsed. Here we represent the type hint.
        self.time: datetime | None = datetime.fromisoformat(data["time"]) if data.get("time") else None

        # Temperature and Weather status
        self.temperature: float | None = data.get("temperature")
        self.weather_code: int | None = data.get("weathercode")

        # Wind conditions (Mapping Pydantic aliases)
        self.wind_speed: float | None = data.get("windspeed")
        self.wind_direction: int | None = data.get("winddirection")

        # Day/Night indicator
        self.is_day: int | None = data.get("is_day")


class DailyForecastUnits:
    def __init__(self, data: dict[str, Any]):
        # Temperature and Precipitation units
        self.apparent_temperature_max: str | None = data.get("apparent_temperature_max")
        self.apparent_temperature_min: str | None = data.get("apparent_temperature_min")
        self.precipitation_hours: str | None = data.get("precipitation_hours")
        self.precipitation_sum: str | None = data.get("precipitation_sum")

        # Radiation and Solar events
        self.shortwave_radiation_sum: str | None = data.get("shortwave_radiation_sum")
        self.sunrise: TimeFormat | None = data.get("sunrise")
        self.sunset: TimeFormat | None = data.get("sunset")

        # Core metrics
        self.temperature_2m_max: str | None = data.get("temperature_2m_max")
        self.temperature_2m_min: str | None = data.get("temperature_2m_min")
        self.time: TimeFormat | None = data.get("time")

        # Aliased fields from Open-Meteo API
        self.weather_code: str | None = data.get("weathercode")
        self.wind_direction_10m_dominant: str | None = data.get("winddirection_10m_dominant")
        self.wind_gusts_10m_max: str | None = data.get("windgusts_10m_max")
        self.wind_speed_10m_max: str | None = data.get("windspeed_10m_max")


# --- Classes Principais ---


class Forecast:
    def __init__(self, data: dict[str, Any]):
        self.current_weather: CurrentWeather | None = (
            CurrentWeather(data.get("current_weather")) if data.get("current_weather") else None
        )
        self.daily_units: DailyForecastUnits | None = (
            DailyForecastUnits(data.get("daily_units")) if data.get("daily_units") else None
        )
        self.daily: DailyForecast | None = DailyForecast(data.get("daily")) if data.get("daily") else None
        self.hourly_units: HourlyForecastUnits | None = (
            HourlyForecastUnits(data.get("hourly_units")) if data.get("hourly_units") else None
        )
        self.hourly: HourlyForecast | None = HourlyForecast(data.get("hourly")) if data.get("hourly") else None

        # Geographic Data and Metadata
        self.elevation: float = data.get("elevation")
        self.generation_time_ms: float = data.get("generationtime_ms")
        self.latitude: float = data.get("latitude")
        self.longitude: float = data.get("longitude")
        self.utc_offset_seconds: int = data.get("utc_offset_seconds")


class Entrance:
    def __init__(self, data: dict[str, Any]):
        self.osm_id: int | None = data.get("osm_id")
        self.type: str | None = data.get("type")
        self.latitude: float | None = float(data["lat"]) if data.get("lat") else None
        self.longitude: float | None = float(data["lon"]) if data.get("lon") else None
        self.extratags: dict[str, Any] = data.get("extratags") or {}
        self.raw: dict[str, Any] = data


class ExtraTags:
    def __init__(self, data: dict[str, Any]):
        # General and OSM specific
        self.wikidata: str | None = data.get("wikidata")
        self.wikipedia: str | None = data.get("wikipedia")
        self.website: str | None = data.get("website")
        self.phone: str | None = data.get("phone")
        self.email: str | None = data.get("email")
        self.sqkm: str | None = data.get("sqkm")

        # Classification & Stats
        self.place: str | None = data.get("place")
        self.linked_place: str | None = data.get("linked_place")
        self.population: str | None = data.get("population")
        self.population_date: str | None = data.get("population:date")
        self.ibge_code: str | None = data.get("IBGE:GEOCODIGO")

        self.capacity: str | None = data.get("capacity")
        self.network: str | None = data.get("network")
        self.operator_type: str | None = data.get("operator:type")
        self.description: str | None = data.get("description")

        # Physical and Operational
        self.building: str | None = data.get("building")
        self.operator: str | None = data.get("operator")
        self.access: str | None = data.get("access")
        self.surface: str | None = data.get("surface")
        self.tracktype: str | None = data.get("tracktype")
        self.opening_hours: str | None = data.get("opening_hours")
        self.opendata_type: str | None = data.get("opendata:type")

        self.raw: dict[str, Any] = data


class NameDetails:
    def __init__(self, data: dict[str, Any]):
        self.name: str | None = data.get("name")
        self.loc_name: str | None = data.get("loc_name")
        self.official_name: str | None = data.get("official_name")
        self.ref: str | None = data.get("ref")
        self.brand: str | None = data.get("brand")
        self.old_name: str | None = data.get("old_name")

        self.names_by_language: dict[str, str] = {
            key.split(":", 1)[1]: value for key, value in data.items() if key.startswith("name:")
        }

        # Mantém o dicionário original
        self.raw: dict[str, Any] = data


class Address:
    def __init__(self, data: dict[str, Any]):
        # Hierarchical display
        self.display: str | None = (
            data.get("city")
            or data.get("town")
            or data.get("village")
            or data.get("municipality")
            or data.get("city_district")
            or data.get("hamlet")
            or data.get("suburb")
            or data.get("city_block")
            or data.get("continent")
        )

        # Street / place
        self.road: str | None = data.get("road")
        self.house_number: str | None = data.get("house_number")
        self.neighbourhood: str | None = data.get("neighbourhood")
        self.suburb: str | None = data.get("suburb")
        self.city_district: str | None = data.get("city_district")
        self.city_block: str | None = data.get("city_block")
        self.quarter: str | None = data.get("quarter")

        # Settlement
        self.city: str | None = data.get("city")
        self.town: str | None = data.get("town")
        self.village: str | None = data.get("village")
        self.municipality: str | None = data.get("municipality")
        self.hamlet: str | None = data.get("hamlet")

        # Administrative
        self.county: str | None = data.get("county")
        self.state_district: str | None = data.get("state_district")
        self.state: str | None = data.get("state")
        self.region: str | None = data.get("region")
        self.postcode: str | None = data.get("postcode")
        self.country: str | None = data.get("country")
        self.country_code: str | None = data.get("country_code")
        self.continent: str | None = data.get("continent")

        # POI
        self.shop: str | None = data.get("shop")
        self.military: str | None = data.get("military")
        self.tourism: str | None = data.get("tourism")
        self.amenity: str | None = data.get("amenity")
        self.office: str | None = data.get("office")
        self.highway: str | None = data.get("highway")
        self.association: str | None = data.get("association")

        # ISO 3166-2 raw (ex: {"lvl4": "BR-CE"})
        self.iso3166_2_raw: dict[str, str] = {
            key.replace("ISO3166-2-", ""): value for key, value in data.items() if key.startswith("ISO3166-2-")
        }

        # ISO 3166-2 normalized (ex: {"state": "BR-CE"})
        self.iso3166_2_normalized: dict[str, str] = {
            ISO3166_LVL_MAP.get(level, level): code for level, code in self.iso3166_2_raw.items()
        }

        self.raw: dict[str, Any] = data

    def get_iso(self, level: str) -> str | None:
        return self.iso3166_2_normalized.get(level) or self.iso3166_2_raw.get(level)

    def __str__(self) -> str:
        """Returns a clean 'Display Location, State, Country' format."""
        parts = [self.display, self.state, self.country]
        return ", ".join(p for p in parts if p)


class GeocodingResult:
    def __init__(self, data: dict[str, Any]):
        # Identifiers
        self.place_id: int | None = data.get("place_id")
        self.licence: str | None = data.get("licence")
        self.osm_type: str | None = data.get("osm_type")
        self.osm_id: int | None = data.get("osm_id")

        # Coordinates
        self.latitude: float | None = float(data["lat"]) if data.get("lat") else None
        self.longitude: float | None = float(data["lon"]) if data.get("lon") else None

        # Classification
        self.category: str | None = data.get("category")
        self.type: str | None = data.get("type")
        self.place_rank: int | None = data.get("place_rank")
        self.importance: float | None = data.get("importance")
        self.address_type: str | None = data.get("addresstype")
        self.admin_level: int | None = data.get("admin_level")

        # Display Information
        self.name: str | None = data.get("name")
        self.display_name: str | None = data.get("display_name")

        # Sub-Objects
        addr_data = data.get("address")
        self.address: Address | None = Address(addr_data) if addr_data else None

        tags_data = data.get("extratags")
        self.extra_tags: ExtraTags | None = ExtraTags(tags_data) if tags_data else None

        names_data = data.get("namedetails")
        self.name_details: NameDetails | None = NameDetails(names_data) if names_data else None

        # Geometry
        raw_bbox = data.get("boundingbox")
        self.bounding_box: list[float] | None = [float(val) for val in raw_bbox] if raw_bbox else None

        # Entrances
        entrances_data = data.get("entrances")
        if entrances_data:
            self.entrances: list[Entrance] = [Entrance(item) for item in entrances_data]
        else:
            self.entrances = []

        self.icon: str | None = data.get("icon")

        self.raw: dict[str, Any] = data

    @property
    def display(self) -> str:
        if not self.display_name:
            return ""

        name = self.name
        city = self.address.display
        parts: list[str] = []
        if name and name != city:
            parts.append(name)

        if city:
            parts.append(city)

        # if (state := self.address.state) and state != city:
        if state := self.address.state:
            parts.append(state)

        if country := self.address.country:
            parts.append(country)

        return ", ".join(parts)


    @property
    def short_display(self) -> str:
        """Helper to get a clean location string."""
        if self.address:
            addr_str = str(self.address)
            # If it's a specific place (like a shop), include its name
            if self.name and self.name not in addr_str:
                return f"{self.name}, {addr_str}"
            return addr_str
        return self.name or ""


class Geocoding:
    def __init__(self, data: Dict[str, Any]):
        results_data = data.get("results", [])
        self.results: list[GeocodingResult] = [GeocodingResult(item) for item in results_data]
