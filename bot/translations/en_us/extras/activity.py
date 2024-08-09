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
            return f"it's {self._current}"

        @property
        def leave(self) -> str:
            return f"you {self._leave}"

        @property
        def leave_again(self) -> str:
            return f"you continued {self._leave_again}"

        @property
        def returned(self) -> str:
            return f"you {self._returned}"

        @property
        def emoji(self) -> str:
            return self._emoji

        @property
        def name(self) -> str:
            return self._name


    afks = {
        "afk": Status("afk", "🏃⌨", "went afk", "afk", "came back", "afk"),
        "read": Status("read", "📖", "went to read", "reading", "read", "reading"),
        "brb": Status("brb", "🏃⌨", "coming back soon", "away", "came back", "away"),
        "eat": Status("food", "🍽", "went to eat", "eating", "ate", "eating"),
        "food": Status("food", "🍽", "went to eat", "eating", "ate", "eating"),
        "play": Status("game", "🎮", "went to play", "playing", "played", "playing"),
        "game": Status("game", "🎮", "went to play", "playing", "played", "playing"),
        "sleep": Status("gn", "💤", "went to sleep", "sleeping", "woke up", "sleeping"),
        "night": Status("gn", "💤", "went to sleep", "sleeping", "woke up", "sleeping"),
        "study": Status("study", "📚", "went to study", "studying", "studied", "studying"),
        "art": Status("art", "🎨", "went to draw", "drawing", "drew", "drawing"),
        "watch": Status("watch", "📺", "went to watch", "watching", "watched", "watching"),
        "shower": Status("shower", "🚿", "went to shower", "in the shower", "took a shower", "the shower"),
        "assist": Status("watch", "📺", "went to watch", "watching", "watched", "watching"),
        "code": Status("code", "💻", "went to code", "coding", "coded", "coding"),
        "work": Status("work", "💼", "went to work", "working", "worked", "working"),
    }
