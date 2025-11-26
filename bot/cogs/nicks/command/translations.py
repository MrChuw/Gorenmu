from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Nicks(TBase):
        def __init__(self):
            super().__init__()

        def not_seen(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    'I have never seen anyone with the nick "{}" in any tracked chat.',
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    'Nunca vi ninguém com o nick "{}" em nenhum chat rastreado.',
                )
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "User nickname history.")
                self.lang_dict.add_with(["pt_br", "pt"], "Histórico de nicks de um usuário.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}nicks (user nick)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}nicks (nick do usuário)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "User nickname history.")
                self.lang_dict.add_with(["pt_br", "pt"], "Histórico de nicks de um usuário.")
            return self._untangle_str(ctx, self._cname)

        # endregion

    Nicks: Nicks
