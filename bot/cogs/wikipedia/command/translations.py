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

    class Wikipedia(TBase):
        def __init__(self):
            super().__init__()

        def url(self, lang: str) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "https://wikipedia.org/wiki/Special:Random")
                self.lang_dict.add_with(["pt_br", "pt"], "https://pt.wikipedia.org/wiki/Special:Random")
            return self.lang_dict.get_lang(lang, self._cname, "en")

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Sends a random wikipedia.")
                self.lang_dict.add_with(["pt_br", "pt"], "Envia uma wikipedia aleatória.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}wikihow")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}wikihow")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command uses the random from [Wikipedia](https://wikipedia.com) to generate random links.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando usa o aleatório de [Wikipedia](https://wikipedia.com) para gerar links aleatórios.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", CommandExemples([{"response": "(random wikipedia link)"}]))
                self.lang_dict.add_with(
                    ["pt_br", "pt"], CommandExemples([{"response": "(link aleatório para o wikipedia)"}])
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Wikipedia: Wikipedia
