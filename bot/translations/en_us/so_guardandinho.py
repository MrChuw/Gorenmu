import re

# Weather Stuff


weather_codes = {
    0: {"day": {"description": "Sunny", "emoji": "☀️"}, "night": {"description": "Clear", "emoji": "🌙"}},
    1: {"day": {"description": "Mainly Sunny", "emoji": "🌤️"}, "night": {"description": "Mainly Clear", "emoji": "🌙"}},
    2: {
        "day": {"description": "Partly Cloudy", "emoji": "⛅"},
        "night": {"description": "Partly Cloudy", "emoji": "⛅"},
    },
    3: {"day": {"description": "Cloudy", "emoji": "☁️"}, "night": {"description": "Cloudy", "emoji": "☁️"}},
    45: {"day": {"description": "Foggy", "emoji": "🌫️"}, "night": {"description": "Foggy", "emoji": "🌫️"}},
    48: {"day": {"description": "Rime Fog", "emoji": "🌫️"}, "night": {"description": "Rime Fog", "emoji": "🌫️"}},
    51: {
        "day": {"description": "Light Drizzle", "emoji": "🌧️"},
        "night": {"description": "Light Drizzle", "emoji": "🌧️"},
    },
    53: {"day": {"description": "Drizzle", "emoji": "🌧️"}, "night": {"description": "Drizzle", "emoji": "🌧️"}},
    55: {
        "day": {"description": "Heavy Drizzle", "emoji": "🌧️"},
        "night": {"description": "Heavy Drizzle", "emoji": "🌧️"},
    },
    56: {
        "day": {"description": "Light Freezing Drizzle", "emoji": "🌧️"},
        "night": {"description": "Light Freezing Drizzle", "emoji": "🌧️"},
    },
    57: {
        "day": {"description": "Freezing Drizzle", "emoji": "🌧️"},
        "night": {"description": "Freezing Drizzle", "emoji": "🌧️"},
    },
    61: {"day": {"description": "Light Rain", "emoji": "🌧️"}, "night": {"description": "Light Rain", "emoji": "🌧️"}},
    63: {"day": {"description": "Rain", "emoji": "🌧️"}, "night": {"description": "Rain", "emoji": "🌧️"}},
    65: {"day": {"description": "Heavy Rain", "emoji": "🌧️"}, "night": {"description": "Heavy Rain", "emoji": "🌧️"}},
    66: {
        "day": {"description": "Light Freezing Rain", "emoji": "🌧️"},
        "night": {"description": "Light Freezing Rain", "emoji": "🌧️"},
    },
    67: {
        "day": {"description": "Freezing Rain", "emoji": "🌧️"},
        "night": {"description": "Freezing Rain", "emoji": "🌧️"},
    },
    71: {"day": {"description": "Light Snow", "emoji": "🌧️"}, "night": {"description": "Light Snow", "emoji": "🌧️"}},
    73: {"day": {"description": "Snow", "emoji": "🌧️"}, "night": {"description": "Snow", "emoji": "🌧️"}},
    75: {"day": {"description": "Heavy Snow", "emoji": "🌧️"}, "night": {"description": "Heavy Snow", "emoji": "🌧️"}},
    77: {"day": {"description": "Snow Grains", "emoji": "🌧️"}, "night": {"description": "Snow Grains", "emoji": "🌧️"}},
    80: {
        "day": {"description": "Light Showers", "emoji": "🌧️"},
        "night": {"description": "Light Showers", "emoji": "🌧️"},
    },
    81: {"day": {"description": "Showers", "emoji": "🌧️"}, "night": {"description": "Showers", "emoji": "🌧️"}},
    82: {
        "day": {"description": "Heavy Showers", "emoji": "🌧️"},
        "night": {"description": "Heavy Showers", "emoji": "🌧️"},
    },
    85: {
        "day": {"description": "Light Snow Showers", "emoji": "🌧️"},
        "night": {"description": "Light Snow Showers", "emoji": "🌧️"},
    },
    86: {"day": {"description": "Snow Showers", "emoji": "🌧️"}, "night": {"description": "Snow Showers", "emoji": "🌧️"}},
    95: {"day": {"description": "Thunderstorm", "emoji": "⛈️"}, "night": {"description": "Thunderstorm", "emoji": "⛈️"}},
    96: {
        "day": {"description": "Light Thunderstorms With Hail", "emoji": "⛈️"},
        "night": {"description": "Light Thunderstorms With Hail", "emoji": "⛈️"},
    },
    99: {
        "day": {"description": "Thunderstorm With Hail", "emoji": "⛈️"},
        "night": {"description": "Thunderstorm With Hail", "emoji": "⛈️"},
    },
    99999: {"day": {"description": "Unknown", "emoji": "❓"}, "night": {"description": "Unknown", "emoji": "❓"}},
}

weather_wind_directions = (
    {
        (337, 360): {0: "N", 1: "north"},
        (0, 23): {0: "NE", 1: "north-east"},
        (23, 68): {0: "E", 1: "east"},
        (68, 113): {0: "SE", 1: "south-east"},
        (113, 158): {0: "S", 1: "south"},
        (158, 203): {0: "SW", 1: "south-west"},
        (203, 248): {0: "W", 1: "west"},
        (248, 293): {0: "NW", 1: "north-west"},
    },
)

wmo_codes = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "light freezing drizzle",
    57: "dense freezing drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "dense freezing rain",
    71: "slight snow fall",
    73: "moderate snow fall",
    75: "heavy snow fall",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow shower",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
    99999: "unknown",
}

PATTERN_TIME = re.compile(
    r"""
    (\b(?P<years>\d+)\s?(?:anos|ano|a|years|year|y)\b\s?)?
    (\b(?P<months>\d+)\s?(?:meses|mês|mes|months|month|mo)\b\s?)?
    (\b(?P<weeks>\d+)\s?(?:semanas|semana|weeks|week|w)\b\s?)?
    (\b(?P<days>\d+)\s?(?:dias|dia|d|days|day)\b\s?)?
    (\b(?P<hours>\d+)\s?(?:horas|hora|h|hours|hour)\b\s?)?
    (\b(?P<minutes>\d+)\s?(?:minutos|minuto|min|m|minutes|minute)\b\s?)?
    (\b(?P<seconds>\d+)\s?(?:segundos|segundo|seg|s|seconds|second|secs|sec)\b\s?)?
    (\b(?P<milliseconds>\d+)\s?(?:milliseconds|millisecond|millisecs|millisec|milli|milissegundos|milissegundo|miliseconds|milisecond|milisecs|milisec|milis|ms)\b\s?)?
    (\b(?P<microseconds>\d+)\s?(?:microssegundos|microssegundo|microseconds|microsecond|microsecs|microsec|micro|us)\b\s?)?
    """,
    re.VERBOSE,
)

unidades_anos = ["months", "days", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
unidades_meses = ["years", "days", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
unidades_semanas = ["years", "months", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
unidades_dias = ["years", "months", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
unidades_horas = ["years", "months", "days", "minutes", "seconds", "milliseconds", "microseconds"]
unidades_minutos = ["years", "months", "days", "hours", "seconds", "milliseconds", "microseconds"]
unidades_segundos = ["years", "months", "days", "hours", "minutes", "milliseconds", "microseconds"]
unidades_milesegundos = ["years", "months", "days", "hours", "minutes", "seconds", "microseconds"]
unidades_microsegundos = ["years", "months", "days", "hours", "minutes", "seconds", "milliseconds"]

opcoes_para_unidades = {
    "years": unidades_anos,
    "year": unidades_anos,
    "anos": unidades_anos,
    "ano": unidades_anos,
    "a": unidades_anos,
    "y": unidades_anos,
    "months": unidades_meses,
    "month": unidades_meses,
    "meses": unidades_meses,
    "mês": unidades_meses,
    "mes": unidades_meses,
    "mo": unidades_meses,
    "semanas": unidades_semanas,
    "semana": unidades_semanas,
    "weeks": unidades_semanas,
    "week": unidades_semanas,
    "w": unidades_semanas,
    "days": unidades_dias,
    "dias": unidades_dias,
    "dia": unidades_dias,
    "day": unidades_dias,
    "d": unidades_dias,
    "hours": unidades_horas,
    "horas": unidades_horas,
    "hora": unidades_horas,
    "hour": unidades_horas,
    "h": unidades_horas,
    "minutos": unidades_minutos,
    "minutes": unidades_minutos,
    "minute": unidades_minutos,
    "minuto": unidades_minutos,
    "min": unidades_minutos,
    "m": unidades_minutos,
    "segundos": unidades_segundos,
    "segundo": unidades_segundos,
    "secs": unidades_segundos,
    "sec": unidades_segundos,
    "seg": unidades_segundos,
    "s": unidades_segundos,
    "milisegundos": unidades_milesegundos,
    "milliseconds": unidades_milesegundos,
    "milisegundo": unidades_milesegundos,
    "miliseconds": unidades_milesegundos,
    "millisecond": unidades_milesegundos,
    "milisecond": unidades_milesegundos,
    "millisecs": unidades_milesegundos,
    "milisecs": unidades_milesegundos,
    "millisec": unidades_milesegundos,
    "milisec": unidades_milesegundos,
    "milli": unidades_milesegundos,
    "milis": unidades_milesegundos,
    "ms": unidades_milesegundos,
    "microsegundos": unidades_microsegundos,
    "microsegundo": unidades_microsegundos,
    "microseconds": unidades_microsegundos,
    "microsecond": unidades_microsegundos,
    "microsecs": unidades_microsegundos,
    "microsec": unidades_microsegundos,
    "micro": unidades_microsegundos,
    "us": unidades_microsegundos,
    "tempo": (),
    "time": (),
    "t": (),
}
