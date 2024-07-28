# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from bot.translations import BaseDecorators
from bot.translations.base import Response
from bot.translations.base.responses import BaseTranslations

if TYPE_CHECKING:
    pass


class EnUsDecorators:
    class Activity(BaseDecorators):
        helper = "Command to enter a Status."
        usage = "To use: <prefix>Afk <message>"
        description = "This command sets your status to AFK."


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
        return f"is {self._current}"

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


afks = {"read": Status("read", "📖", "went to read", "reading", "read", "reading"),
        "afk": Status("afk", "🏃⌨", "went afk", "afk", "came back", "afk"),
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


class EnUsTranslations:
    class Activity(BaseTranslations.Activity):
        class Afk(BaseTranslations.Activity.Afk):
            afk: dict[str, Status] = afks
            message_too_long: Response = Response(
                    {"success": False, "response": "This message is too long.", "is_response": False}
            )
            afk_response: Response = Response({"success": True, "response": "{}: {}", "is_response": False}
            )
            afk_content_response: Response = Response(
                    {"success": True, "response": "{}: {} and left a note with: {}", "is_response": False,
                    }
            )

        class IsAfk(BaseTranslations.Activity.IsAfk):
            afk: dict[str, Status] = afks
            bot_nick: Response = Response(
                    {"success": False, "response": "I am always here... watching.", "is_response": False,
                    }
            )
            author_nick: Response = Response(
                    {"success": False, "response": "you are not working... obviously", "is_response": False,
                    }
            )
            never_seen: Response = Response(
                    {"success": False, "response": "I don't remember ever seeing any {}.", "is_response": False,
                    }
            )
            is_afk: Response = Response({"success": False, "response": "@{} {}: {}", "is_response": False}
            )
            is_afk_content: Response = Response(
                    {"success": False, "response": "@{} {} and left a note: {}", "is_response": False}
            )
            is_not_afk: Response = Response({"success": False, "response": "@{} is not AFK.", "is_response": False}
            )

        class RAfk(BaseTranslations.Activity.RAfk):
            time_expired: Response = Response(
                    {"success": False, "response": "The time to return has passed.", "is_response": False,
                    }
            )
            is_afk: Response = Response({"success": False, "response": "{}: {}", "is_response": False}
            )
            is_afk_content: Response = Response(
                    {"success": False, "response": "{} {}: and left a note: {}", "is_response": False}
            )
            is_not_afk: Response = Response({"success": False, "response": "you are not AFK.", "is_response": False}
            )
