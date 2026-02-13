from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .afk import AFKCmd
    from .isafk import IsAfkCmd
    from .rafk import RAfkCmd


@lru_cache(maxsize=32)
def _get_cached_activity_data(lang: str, translator_instance: TBase) -> dict[str, Activity.Status]:
    prop_raw = translator_instance.get_list_by_lang(lang, "prop_list", include_en=False)

    properties = {
        "current": prop_raw[0],
        "leave": prop_raw[1],
        "leave_again": prop_raw[2],
        "returned": prop_raw[3],
    }

    keys = ["afk", "read", "brb", "eat", "play", "sleep", "study", "art", "watch", "shower", "code", "work"]
    afks_data = {key: translator_instance.get_list_by_lang(lang, f"{key}_list", include_en=False) for key in keys}

    data = {"property": properties, "afks": afks_data}
    return Activity(data).afks


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: AFKCmd | RAfkCmd | IsAfkCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: AFKCmd | RAfkCmd | IsAfkCmd = parent
        self.populate_subclasses(parent=self)

    class AFK(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "AFK"

        def _cached_activity_processing(self, lang: str) -> dict[str, Activity.Status]:
            return _get_cached_activity_data(lang, self)

        def afk(self, status: str, emoji: str) -> Response:
            text = self.get_text(self._cname, status=status, emoji=emoji)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def content(self, status: str, emoji: str, content: str) -> Response:
            text = self.get_text(self._cname, status=status, emoji=emoji, content=content)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {"response": self.get_text("cmd_ex1_res")},
                    {"args": self.get_text("cmd_ex2_args"), "response": self.get_text("cmd_ex2_res")},
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "warning",
                        "title": self.get_text("adm_title"),
                        "message": self.get_text("adm_msg"),
                    }
                ]
            )

        def afks(self, lang: str | None = None) -> dict[str, Activity.Status]:
            target_lang = lang or self.ctx_get().user.get_lang()
            return self._cached_activity_processing(target_lang)

        def _get_afks(self):
            return self.afks()

    AFK: AFK

    class IsAFK(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "IsAFK"

        def bot(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def author(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def is_afk(self, name: str, status: str, emoji: str, time: str) -> Response:
            text = self.get_text(self._cname, name=name, status=status, emoji=emoji, time=time)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def is_afk_content(self, name: str, status: str, emoji: str, message: str, time: str) -> Response:
            text = self.get_text(self._cname, name=name, status=status, emoji=emoji, message=message, time=time)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def is_not_afk(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {"args": self.get_text("cmd_ex1_args"), "response": self.get_text("cmd_ex1_res")},
                    {"args": self.get_text("cmd_ex2_args"), "response": self.get_text("cmd_ex2_res")},
                ]
            )

    IsAFK: IsAFK

    class RAFK(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "RAFK"

        def return_expired(self) -> str:
            return self.get_text(self._cname)

        def afk(self, status: str, emoji: str) -> Response:
            text = self.get_text(self._cname, status=status, emoji=emoji)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def content(self, status: str, emoji: str, content: str) -> Response:
            text = self.get_text(self._cname, status=status, emoji=emoji, content=content)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {"response": self.get_text("cmd_ex1_res")},
                    {"args": self.get_text("cmd_ex2_args"), "response": self.get_text("cmd_ex2_res")},
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "warning",
                        "title": self.get_text("adm_title"),
                        "message": self.get_text("adm_msg"),
                    }
                ]
            )

    RAFK: RAFK

    class AFKReturn(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "AFKReturn"

        def afk(self, status: str, emoji: str, a_time: str, clock: str) -> Response:
            text = self.get_text(self._cname, status=status, emoji=emoji, a_time=a_time, clock=clock)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def content(self, status: str, emoji: str, message: str, a_time: str, clock: str) -> Response:
            text = self.get_text(self._cname, status=status, emoji=emoji, message=message, a_time=a_time, clock=clock)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

    AFKReturn: AFKReturn


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
