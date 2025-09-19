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

    class Reverse(TBase):
        def __init__(self):
            super().__init__()

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Reverses a text.")
                self.lang_dict.add_with(["pt_br", "pt"], "Inverte um texto.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}reverse (text)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}reverse <texto>")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This command reverses the sent text.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando reverte o texto enviado.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", CommandExemples([{"args": "the text sent.", "response": ".tnes txet eht"}])
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], CommandExemples([{"args": "o texto enviado.", "response": ".odaivne otxet o"}])
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Reverse: Reverse
