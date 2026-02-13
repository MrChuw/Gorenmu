from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase
from bot.utils.timelength import English, Guess, Locale, Portuguese, Spanish

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .time import TimeCmd


@lru_cache(maxsize=12)
def _get_cached_lang_logic(
    cname: str, lang_val: str | bool, guess: bool, translator_instance: TBase, _
) -> type[Locale] | type[Guess]:
    locales = {"English": English, "Portuguese": Portuguese, "Spanish": Spanish}

    if lang_val:
        res = translator_instance.get_text_by_lang(lang_val, cname) or translator_instance.get_text_by_lang("en", cname)
        return locales.get(res, English)

    if guess:
        return Guess

    current_type = translator_instance.get_text(cname)
    return locales.get(current_type, English)


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: TimeCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: TimeCmd = parent
        self.populate_subclasses(parent=self)

    class Time(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Time"

        def only_latin(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def overflow(self) -> Response:
            dev_name = self.parent.bot.dev_user.display_name
            text = self.get_text(self._cname, dev=dev_name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def past(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def present(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def future(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def get_lang(self, lang: str | bool = "", guess: bool = False, lang_hash=None) -> type[Locale] | type[Guess]:
            return _get_cached_lang_logic(self._cname, lang, guess, self, lang_hash)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {"args": "h 100_000_000s", "response": self.get_text("cmd_res_hours")},
                    {"args": "h 100_000_000s", "response": self.get_text("cmd_res_full")},
                    {"args": "time 25/12/2025 at 12:00:00", "response": self.get_text("cmd_res_future")},
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions([])

        # endregion

    Time: Time
