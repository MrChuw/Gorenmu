# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Wikihow(TBase):
        def __init__(self):
            super().__init__()

        def url(self, lang: str) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "https://www.wikihow.com/Special:Randomizer")
                self.lang_dict.add_with(["pt_br", "pt"], "https://pt.wikihow.com/Especial:Randomizer")
            return self.lang_dict.get_lang(lang, self._cname, "en")

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Sends a random wikihow.")
                self.lang_dict.add_with(["pt_br", "pt"], "Envia um wikihow aleatório.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}wikihow (amount)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}wikihow <quantidade>")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "This command uses the random from [Wikihow](https://wikihow.com) to generate random links."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando usa o aleatório de [Wikihow](https://wikihow.com) para gerar links aleatórios.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", CommandExemples([{"response": "(random wikihow link)"}]))
                self.lang_dict.add_with(
                    ["pt_br", "pt"], CommandExemples([{"response": "(link aleatório para o wikihow)"}])
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Wikihow: Wikihow
