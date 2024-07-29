# -*- coding: utf-8 -*-
from dataclasses import dataclass


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






