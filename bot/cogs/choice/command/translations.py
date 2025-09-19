# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Choice(TBase):
        def __init__(self):
            super().__init__()

        def response(self, ctx: Context, choice) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), choice)

        def pattern(self, ctx: Context) -> re.Pattern[str]:
            with self.lang_dict.once(self._cname):
                base_separators = [",", r"\s+"]

                def make_regex(keywords: list[str], base: list[str]) -> str:
                    return f'(?:{"|".join(keywords + base)})'

                regex_string_en = make_regex(["or"], base_separators)
                regex_string_pt = make_regex(["ou"], base_separators)

                self.lang_dict.add_with("en", re.compile(regex_string_en))
                self.lang_dict.add_with(["pt_br", "pt"], re.compile(regex_string_pt))

            return self._untangle_any(ctx, self._cname)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Chooses an option from the options provided by the user.")
                self.lang_dict.add_with(["pt_br", "pt"], "Escolhe uma opção das opções fornecidas pelo usuário.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}choice (option1) or (option2)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}choice (opção1) ou (opção2)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Chooses an option from the options provided by the user.")
                self.lang_dict.add_with(["pt_br", "pt"], "Escolhe uma opção das opções fornecidas pelo usuário.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "dice or house or coin", "response": "house"},
                            {"args": "dice house coin", "response": "dice"},
                            {"args": "dice, house, coin", "response": "coin"},
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"args": "dados ou casa ou moeda", "response": "casa"},
                            {"args": "dice casa moeda", "response": "dados"},
                            {"args": "dados, casa, moeda", "response": "moeda"},
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Choice: Choice
