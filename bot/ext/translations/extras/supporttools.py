from __future__ import annotations

import inspect
import types
from functools import lru_cache
from typing import TYPE_CHECKING

from bot.ext.translations.extras import Humanize as ExtrasHumanize

from . import TBase

if TYPE_CHECKING:
    from bot.ext import TranslationBase


@lru_cache(maxsize=8)
def _get_humanize_data(instance: TBase, lang: str | None = None) -> ExtrasHumanize:
    units_keys = [
        "years",
        "months",
        "weeks",
        "days",
        "hours",
        "minutes",
        "seconds",
        "milliseconds",
        "microseconds",
        "time",
    ]

    patterns = {unit: instance.get_list(f"unit_{unit}") for unit in units_keys}

    if lang != "en":
        en_patterns = {unit: instance.get_list_by_lang("en", f"unit_{unit}", include_en=False) for unit in units_keys}
        return ExtrasHumanize(patterns, lang, en_patterns)

    return ExtrasHumanize(patterns, "en")


class SupportTools(TBase):
    def __init__(self, parent: TranslationBase, file=None):
        super().__init__(parent, file, is_base=True)
        self.LanguageContext = self._LanguageContext(parent)
        self.TimeTools = self._TimeTools(parent)
        self.Emotes = self._Emotes(parent)

    @staticmethod
    def fake_stacktrace(message: str) -> Exception:
        exc = Exception(message)
        current_frame = inspect.currentframe()
        parent_frame = current_frame.f_back if current_frame else None
        if parent_frame is not None:
            tb = types.TracebackType(
                tb_next=None,
                tb_frame=parent_frame,
                tb_lasti=0,
                tb_lineno=1,
            )
            exc.__traceback__ = tb
        return exc

    class _LanguageContext(TBase):
        def __init__(self, parent: TranslationBase):
            self.prefix = "LanguageContext"
            super().__init__(parent)
            self.Verbs = self._Verbs(parent)
            self.parent.register_locale(self.prefix, is_base=True)

        def mention(self, author_name: str, target_name: str) -> str:
            if target_name.lower() == author_name.lower():
                return self.get_text(self._cname)
            return f"@{target_name}"

        def multi_mention(self, target_name: list[str]) -> str:
            div = self.get_text(self._cname)
            string_ = ""
            string_ += f"@{target_name.pop(0)} "
            for name in target_name:
                string_ += f"{div} @{name} "
            return string_

        class _Verbs(TBase):
            def __init__(self, parent: TranslationBase):
                self.prefix = "LanguageContext_Verbs"
                super().__init__(parent, is_base=True)
                self.parent.register_locale(self.prefix, is_base=True)

            def cookies_second_person(self) -> str:
                return self.get_text(self._cname)

            def cookies_third_person(self) -> str:
                return self.get_text(self._cname)

            def positive(self, lang: str | None = None, include_en=True) -> list[str]:
                return self.get_list_by_lang(
                    lang or self.ctx_get().user.get_lang() or "en", self._cname, include_en=include_en
                )

            def negative(self, lang: str | None = None, include_en=True) -> list[str]:
                return self.get_list_by_lang(
                    lang or self.ctx_get().user.get_lang() or "en", self._cname, include_en=include_en
                )

            def nothing(self, lang: str | None = None, include_en=True) -> list[str]:
                return self.get_list_by_lang(
                    lang or self.ctx_get().user.get_lang() or "en", self._cname, include_en=include_en
                )

            def separators(self, lang: str | None = None, include_en=True) -> list[str]:
                return self.get_list_by_lang(
                    lang or self.ctx_get().user.get_lang() or "en", self._cname, include_en=include_en
                )

            def all(self, lang: str | None = None, include_en=True) -> list[str]:
                return self.get_list_by_lang(
                    lang or self.ctx_get().user.get_lang() or "en", self._cname, include_en=include_en
                )

    class _TimeTools(TBase):
        def __init__(self, parent: TranslationBase):
            self.prefix = "TimeTools"
            super().__init__(parent, is_base=True)
            self.parent.register_locale(self.prefix, is_base=True)

        def strftime(self) -> str:
            return self.get_text("strftime")

        def Humanize(self, lang: str | None = None) -> ExtrasHumanize:  # noqa: N802
            context = self.ctx_get()
            lang = lang or context.user.language or "en"
            return _get_humanize_data(self, lang)

    class _Emotes(TBase):
        def __init__(self, parent: TranslationBase):
            self.prefix = "Emotes"
            super().__init__(parent, is_base=True)
            self.parent.register_locale(self.prefix, is_base=True)

        def happy(self, lang: str | None = None) -> list[str]:
            return self.get_list_by_lang(lang or self.ctx_get().user.get_lang() or "en", self._cname)

        def pog(self, lang: str | None = None) -> list[str]:
            return self.get_list_by_lang(lang or self.ctx_get().user.get_lang() or "en", self._cname)

        def sad(self, lang: str | None = None) -> list[str]:
            return self.get_list_by_lang(lang or self.ctx_get().user.get_lang() or "en", self._cname)

        def love(self, lang: str | None = None) -> list[str]:
            return self.get_list_by_lang(lang or self.ctx_get().user.get_lang() or "en", self._cname)

        def hug(self, lang: str | None = None) -> list[str]:
            return self.get_list_by_lang(lang or self.ctx_get().user.get_lang() or "en", self._cname)

        def pat(self, lang: str | None = None) -> list[str]:
            return self.get_list_by_lang(lang or self.ctx_get().user.get_lang() or "en", self._cname)

        def hit(self, lang: str | None = None) -> list[str]:
            return self.get_list_by_lang(lang or self.ctx_get().user.get_lang() or "en", self._cname)

        def okay(self, lang: str | None = None) -> list[str]:
            return self.get_list_by_lang(lang or self.ctx_get().user.get_lang() or "en", self._cname)

        def bed(self, lang: str | None = None) -> list[str]:
            return self.get_list_by_lang(lang or self.ctx_get().user.get_lang() or "en", self._cname)


class GenericWait(TBase):
    def __init__(self, parent: TranslationBase, file=None):
        self.prefix = "GenericWait"
        super().__init__(parent, file)
        self.parent.register_locale(self.prefix, is_base=True)

    def already_in_action(self, action: str, user1: str, user2: str) -> str:
        return self.get_text(self._cname, action=action, user1=user1, user2=user2)

    def accept(self, lang: str | None = None) -> list[str]:
        target_lang = lang or self.ctx_get().user.get_lang() or "en"
        return self.get_list_by_lang(target_lang, self._cname)

    def reject(self, lang: str | None = None) -> list[str]:
        target_lang = lang or self.ctx_get().user.get_lang() or "en"
        return self.get_list_by_lang(target_lang, self._cname)

