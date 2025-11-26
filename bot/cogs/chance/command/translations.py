from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Chance(TBase):
        def __init__(self):
            super().__init__()

        def response(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}%")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Returns a random percentage.")
                self.lang_dict.add_with(["pt_br", "pt"], "Retorna uma porcentagem aleatória.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}chance")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}chance")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command generates and returns a random percentage, representing a value between 0% and 100%.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando gera e retorna uma porcentagem aleatória, representando um valor entre 0% e 100%.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], CommandExemples([{"response": "34%"}]))
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Chance: Chance
