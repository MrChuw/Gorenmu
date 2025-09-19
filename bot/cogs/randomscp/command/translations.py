# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class RandomScp(TBase):
        def __init__(self):
            super().__init__()

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Sends a random SCP.")
                self.lang_dict.add_with(["pt_br", "pt"], "Envia um SCP aleatório.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}scp")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}scp")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command uses the random from [SCP](https://scp-wiki.wikidot.com) to "
                    "generate random SCP links.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando usa o aleatório de [SCP](https://scp-wiki.wikidot.com) para "
                    "gerar links aleatórios de SCP.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", CommandExemples([{"response": "(random SCP link)"}]))
                self.lang_dict.add_with(["pt_br", "pt"], CommandExemples([{"response": "(link de um SCP aleatório)"}]))
            return self._untangle_commands(ctx, self._cname)

        # endregion

    RandomScp: RandomScp
