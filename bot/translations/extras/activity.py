# -*- coding: utf-8 -*-
from dataclasses import dataclass


class Activity:
    @dataclass
    class Status:
        _name: str
        _emoji: str
        _leave: str
        _current: str
        _returned: str
        _leave_again: str
        _property: dict

        @property
        def current(self) -> str:
            return f"{self._property['current']} {self._current}"

        @property
        def leave(self) -> str:
            return f"{self._property['leave']} {self._leave}"

        @property
        def leave_again(self) -> str:
            return f"{self._property['leave_again']} {self._leave_again}"

        @property
        def returned(self) -> str:
            return f"{self._property['returned']} {self._returned}"

        @property
        def emoji(self) -> str:
            return self._emoji

        @property
        def name(self) -> str:
            return self._name

    def __init__(self, data: dict[str, dict]):
        self.property: dict = data.get("property")
        self.afks = {}
        for key, value in data.get("afks").items():
            self.afks[key] = Activity.Status(*value, _property=self.property)
