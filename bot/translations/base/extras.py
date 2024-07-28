from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ext.commands import Context
    from models import User


@dataclass
class Status:
    _name: str = None
    _emoji: str = None
    _leave: str = None
    _current: str = None
    _returned: str = None
    _leave_again: str = None

    @property
    def current(self) -> str:
        return ""

    @property
    def leave(self) -> str:
        return ""

    @property
    def leave_again(self) -> str:
        return ""

    @property
    def returned(self) -> str:
        return ""

    @property
    def emoji(self) -> str:
        return ""


class Response:
    def __init__(self, data: dict):
        self.ctx: Optional[Context] = data.get("ctx", None)
        self.success: Optional[bool] = data.get("success", None)
        self.response: Optional[str] = data.get("response", None)
        self.response_list: Optional[List[str]] = data.get("response_list", None)
        self.object: Optional[object] = data.get("object", None)
        self.handle: Optional[str] = data.get("handle", None)
        self.is_response: bool = data.get("is_response", False)
        self.pipeble: bool = data.get("pipeble", True)
        self.response_string: str = ""

    def format_response(self, ctx: Context, *args: Any, **kwargs: Any) -> Response:
        if self is ctx.translations.Cookies.CookieCount.cookie:
            return ctx.translations.Cookies.CookieCount.format_cookie(self, ctx, *args, **kwargs)
        if self is ctx.translations.Tools.Weather.weather:
            return ctx.translations.Tools.Weather.format_weather(self, ctx, *args, **kwargs)
        self.ctx = ctx
        success = kwargs.pop("success", True)
        response_list = kwargs.pop("response_list", None)
        handle = kwargs.pop("handle", None)

        self.is_response = True

        # Definir valores em response_obj se fornecidos
        self.success = success
        self.response_list = response_list
        self.handle = handle

        if args:
            self.response_string = self.response.format(*args, **kwargs)
        else:
            self.response_string = self.response
        return self


mention_dict = {"en-us": "you", "pt-br": "você"}


class BaseTranslation:
    ctx: Context

    # TODO: adicionar um fallback para o idioma padrão caso não tenha a tradução.

    @staticmethod
    def mention(ctx: Context, user: User, name: str) -> str:
        return (
            mention_dict[user.language] if user.name == ctx.author.name else f"@{name}"
        )  # if user.language is not None:  #     pass  # if user.language == "pt-br":  #     return "você" if user.name == ctx.author.name else f"@{name}"  # if user.language == "en-us":  #     return "you" if user.name == ctx.author.name else f"@{name}"

    @staticmethod
    def remind_mention(ctx: Context, user: User, name: str, invoke_by: str) -> str:
        return (
            mention_dict[user.language]
            if name == ctx.author.name
            else (
                user.nickname or f"@{name}"
                if invoke_by in ["remind", "lembrete", "remember"]
                else mention_dict[user.language]
            )
        )


class Activity:
    afks = {
        "read": Status(),
        "afk": Status(),
        "brb": Status(),
        "food": Status(),
        "game": Status(),
        "gn": Status(),
        "study": Status(),
        "art": Status(),
        "watch": Status(),
        "shower": Status(),
        "code": Status(),
        "work": Status(),
    }


# Games stuff


def fight_option(ctx: Context, name: str) -> list[str]:
    pass


# Pets stuff


class PetInfo:
    def __init__(self, specie, name, price):
        self.specie: str = specie
        self.emoji: str = name
        self.price: int = price


PetsDict = dict[str, PetInfo]

PetFuncCallable = Callable[[List[PetsDict]], List[PetInfo]]


def from_list_to_pet_list(pets_dict: List[PetsDict]) -> List[PetInfo]:
    return [PetInfo(specie=pet["specie"], name=pet["emoji"], price=pet["price"]) for pet in pets_dict]


# Weather Stuff


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
