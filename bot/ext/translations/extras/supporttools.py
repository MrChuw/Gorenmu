from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext.translations.extras import Humanize as ExtrasHumanize

from . import ClassBase, TBase

if TYPE_CHECKING:
    from bot.ext import Context, TranslationBase


class OtherTools(ClassBase):
    class SupportTools(ClassBase, TBase):
        def __init__(self, parent: TranslationBase | None = None):
            super().__init__(parent)
            self.populate_subclasses(parent)

        class LanguageContext(ClassBase, TBase):
            def __init__(self, parent: TranslationBase | None = None):
                super().__init__(parent)
                self.populate_subclasses(parent)

            def mention(self, ctx: Context, author_name: str, target_name: str) -> str:
                with self.lang_dict.once(self._cname):
                    self.lang_dict.add_with("en", "you")
                    self.lang_dict.add_with(["pt_br", "pt"], "você")
                mention = self._untangle_str(ctx, self._cname)
                return mention if target_name == author_name else f"@{target_name}"

            class Verbs(TBase):
                def __init__(self, parent: TranslationBase | None = None):
                    super().__init__(parent)

                def cookies_second_person(self, ctx: Context) -> str:
                    with self.lang_dict.once(self._cname):
                        self.lang_dict.add_with("en", "have")
                        self.lang_dict.add_with(["pt_br", "pt"], "já comeu")
                    return self._untangle_str(ctx, self._cname)

                def cookies_third_person(self, ctx: Context) -> str:
                    with self.lang_dict.once(self._cname):
                        self.lang_dict.add_with("en", "has")
                        self.lang_dict.add_with(["pt_br", "pt"], "já comeu")
                    return self._untangle_str(ctx, self._cname)

                def positive(self, ctx: Context) -> list[str]:
                    with self.lang_dict.once(self._cname):
                        self.lang_dict.add_with("en", ["True"])
                        self.lang_dict.add_with(["pt_br", "pt"], ["Sim"])
                    return self._untangle_any(ctx, self._cname) + self._untangle_any_lang("en", self._cname)

                def negative(self, ctx: Context) -> list[str]:
                    with self.lang_dict.once(self._cname):
                        self.lang_dict.add_with("en", ["False"])
                        self.lang_dict.add_with(["pt_br", "pt"], ["Não"])
                    return self._untangle_any(ctx, self._cname) + self._untangle_any_lang("en", self._cname)

                def nothing(self, ctx: Context) -> list[str]:
                    with self.lang_dict.once(self._cname):
                        self.lang_dict.add_with("en", ["None"])
                        self.lang_dict.add_with(["pt_br", "pt"], ["Nenhum"])
                    return self._untangle_any(ctx, self._cname) + self._untangle_any_lang("en", self._cname)

            Verbs: Verbs

        LanguageContext: LanguageContext

        class TimeTools(TBase):
            def __init__(self, parent: TranslationBase | None = None):
                super().__init__(parent)

            def strftime(self, ctx: Context) -> str:
                with self.lang_dict.once(self._cname):
                    self.lang_dict.add_with("en", "%m/%d/%Y at %I:%M %p")
                    self.lang_dict.add_with(["pt_br", "pt"], "%d/%m/%Y às %H:%M:%S")
                return self._untangle_str(ctx, self._cname)

            strftime: str

            def Humanize(self, ctx: Context) -> ExtrasHumanize:  # NOQA
                cname = self._cname.lower()
                with self.lang_dict.once(cname):
                    en_pattern = ExtrasHumanize(
                        {
                            "years": ["years", "year", "y"],
                            "months": ["months", "month", "mo"],
                            "weeks": ["weeks", "week", "w"],
                            "days": ["days", "day", "d"],
                            "hours": ["hours", "hour", "h"],
                            "minutes": ["minutes", "minute", "min", "m"],
                            "seconds": ["seconds", "second", "secs", "sec", "s"],
                            "milliseconds": ["milliseconds", "millisecond", "millisecs", "millisec", "milli"],
                            "microseconds": ["microseconds", "microsecond", "micro", "us"],
                            "time": ["time", "t"],
                        },
                        "en",
                    )
                    self.lang_dict.add_with("en", en_pattern)
                    self.lang_dict.add_with(
                        ["pt_br", "pt"],
                        ExtrasHumanize(
                            {
                                "years": ["anos", "ano", "a"],
                                "months": ["meses", "mês", "mo"],
                                "weeks": ["semanas", "semana", "w"],
                                "days": ["dias", "dia", "d"],
                                "hours": ["horas", "hora", "h"],
                                "minutes": ["minutos", "minuto", "min", "m"],
                                "seconds": ["segundos", "segundo", "segs", "seg", "s"],
                                "milliseconds": ["milissegundos", "milissegundo", "milisecs", "milisec", "mili"],
                                "microseconds": ["microssegundos", "microssegundo", "micro", "us"],
                                "time": ["tempo", "t"],
                            },
                            "pt_BR",
                            en_pattern.pattern,
                        ),
                    )

                return self._untangle_any(ctx, cname)

            Humanize: ExtrasHumanize

        TimeTools: TimeTools

        class Emotes(TBase):
            def __init__(self, parent: TranslationBase | None = None):
                super().__init__(parent)

            def happy(self, ctx: Context) -> list[str]:
                with self.lang_dict.once(self._cname):
                    self.lang_dict.add_with(["en", "pt_br", "pt"], ["happy"])
                return self._untangle_any(ctx, self._cname)

            def pog(self, ctx: Context) -> list[str]:
                with self.lang_dict.once(self._cname):
                    self.lang_dict.add_with(["en", "pt_br", "pt"], ["pog"])
                return self._untangle_any(ctx, self._cname)

            def sad(self, ctx: Context) -> list[str]:
                with self.lang_dict.once(self._cname):
                    self.lang_dict.add_with(["en", "pt_br", "pt"], ["sad"])
                return self._untangle_any(ctx, self._cname)

        Emotes: Emotes

    SupportTools: SupportTools
