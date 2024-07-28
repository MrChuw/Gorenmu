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

        @property
        def current(self) -> str:
            return f"está {self._current}"

        @property
        def leave(self) -> str:
            return f"você {self._leave}"

        @property
        def leave_again(self) -> str:
            return f"você continuou {self._leave_again}"

        @property
        def returned(self) -> str:
            return f"você {self._returned}"

        @property
        def emoji(self) -> str:
            return self._emoji

        @property
        def name(self) -> str:
            return self._name


    afks = {
        "read": Status("read", "📖", "foi ler", "lendo", "leu", "lendo"),
        "afk": Status("afk", "🏃⌨", "ficou afk", "afk", "voltou", "afk"),
        "brb": Status("brb", "🏃⌨", "volta já", "fora", "voltou", "fora"),
        "food": Status("food", "🍽", "foi comer", "comendo", "comeu", "comendo"),
        "game": Status("game", "🎮", "foi jogar", "jogando", "jogou", "jogando"),
        "gn": Status("gn", "💤", "foi dormir", "dormindo", "acordou", "dormindo"),
        "study": Status("study", "📚", "foi estudar", "estudando", "estudou", "estudando"),
        "art": Status("art", "🎨", "foi desenhar", "desenhando", "desenhou", "desenhando"),
        "watch": Status("watch", "📺", "foi assistir", "assistindo", "assistiu", "assistindo"),
        "shower": Status("shower", "🚿", "foi pro banho", "no banho", "tomou banho", "o banho"),
        "code": Status("code", "💻", "foi programar", "programando", "programou", "programando"),
        "work": Status("work", "💼", "foi trabalhar", "trabalhando", "trabalhou", "trabalhando"),
    }
