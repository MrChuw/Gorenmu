from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from bot.ext.translations.extras import Humanize as ExtrasHumanize

from . import ClassBase, TBase

if TYPE_CHECKING:
    from bot.ext import TranslationBase


@lru_cache(maxsize=8)
def _get_humanize_data(instance: TBase, lang: str | None = None) -> ExtrasHumanize:
    context = instance.ctx_get()
    lang = lang or context.user.language or "en"

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


class OtherTools(ClassBase):
    class SupportTools(ClassBase, TBase):
        def __init__(self, parent: TranslationBase | None = None, file=None):
            super().__init__(parent, file)
            self.populate_subclasses(parent)

        class LanguageContext(ClassBase, TBase):
            def __init__(self, parent: TranslationBase | None = None):
                super().__init__(parent)
                self.prefix = "LanguageContext"
                self.populate_subclasses(parent)

            def mention(self, author_name: str, target_name: str) -> str:
                if target_name.lower() == author_name.lower():
                    return self.get_text(self._cname)
                return f"@{target_name}"

            class Verbs(TBase):
                def __init__(self, parent: TranslationBase | None = None):
                    super().__init__(parent)
                    self.prefix = "LanguageContext_Verbs"

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

            Verbs: Verbs

        LanguageContext: LanguageContext

        class TimeTools(TBase):
            def __init__(self, parent: TranslationBase | None = None):
                super().__init__(parent)
                self.prefix = "TimeTools"

            def strftime(self) -> str:
                return self.get_text("strftime")

            strftime: str

            def Humanize(self, lang: str = None) -> ExtrasHumanize:  # NOQA
                return _get_humanize_data(self, lang)

            Humanize: ExtrasHumanize

        TimeTools: TimeTools

        class Emotes(TBase):
            def __init__(self, parent: TranslationBase | None = None):
                super().__init__(parent)
                self.prefix = "Emotes"

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

        Emotes: Emotes

    SupportTools: SupportTools

    class GenericWait(TBase):
        def __init__(self, parent: TranslationBase | None = None, file=None):
            super().__init__(parent, file)
            self.prefix = "GenericWait"

        def already_in_action(self, action: str, user1: str, user2: str) -> str:
            return self.get_text(self._cname, action=action, user1=user1, user2=user2)

        def accept(self, lang: str | None = None) -> list[str]:
            target_lang = lang or self.ctx_get().user.get_lang() or "en"
            return self.get_list_by_lang(target_lang, self._cname)

        def reject(self, lang: str | None = None) -> list[str]:
            target_lang = lang or self.ctx_get().user.get_lang() or "en"
            return self.get_list_by_lang(target_lang, self._cname)

    GenericWait: GenericWait
