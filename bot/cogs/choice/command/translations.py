from __future__ import annotations

import re
from functools import lru_cache
from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .choice import ChoiceCmd


@lru_cache(maxsize=8)
def _get_cached_choice_pattern(parent_instance: TranslationBase, lang: str | None = None) -> re.Pattern[str]:
    separator = parent_instance.SupportTools.LanguageContext.Verbs.separators(lang)
    regex_string = f'(?:{"|".join([*separator, ",", r"\s+"])})'
    return re.compile(regex_string)


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: ChoiceCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: ChoiceCmd = parent
        self.populate_subclasses(parent=self)

    class Choice(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Choice"

        def response(self, choice: str) -> Response:
            text = self.get_text(self._cname, choice=choice)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def pattern(self, lang: str | None = None) -> re.Pattern[str]:
            return _get_cached_choice_pattern(self.parent, lang)

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
                    {"args": self.get_text("cmd_ex3_args"), "response": self.get_text("cmd_ex3_res")},
                ]
            )

    Choice: Choice
