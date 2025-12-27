from typing import Any


class DiurnalTerms:
    def __init__(self, day: str = "day", night: str = "night"):
        self.day = day
        self.night = night

    def get(self, is_day: int):
        return self.night if is_day == 0 else self.day


class WeatherDetails:
    def __init__(self, data: dict[str, Any]):
        self.description: str = data.get("description", "Unknown")
        self.emoji: str = data.get("emoji", "❓")

    def get(self, key: str) -> str | None:
        return getattr(self, key, None)


class WeatherCode:
    def __init__(self, data: dict[str, Any]):
        # Mapping of WMO codes to a dictionary containing WeatherDetails objects
        self.codes: dict[str, dict[str, WeatherDetails]] = {}

        for code, periods in data.items():
            self.codes[code] = {
                "day": WeatherDetails(periods.get("day", {})),
                "night": WeatherDetails(periods.get("night", {})),
            }

    def get(self, code: str | int) -> dict[str, WeatherDetails] | None:
        str_code = str(code)
        # Returns the specific code, or the default 'Unknown' code
        return self.codes.get(str_code, self.codes.get("99999"))
