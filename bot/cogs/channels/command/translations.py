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

    class Channels(TBase):
        def __init__(self):
            super().__init__()

        def quantity(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "I'm logged in {} channels.")
                self.lang_dict.add_with(["pt_br", "pt"], "Estou logado em {} canais.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def names(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("helper"):
                self.lang_dict.add_with("en", "Shows the list of channels where the bot is present.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Mostra a lista de canais em que o bot está presente.",
                )
            return self._untangle_str(ctx, "helper")

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once("usage"):
                self.lang_dict.add_with("en", "To use: {}channels [quantity|ping]")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}channels [quantity|ping]")
            return self._untangle_str(ctx, "usage").format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("description"):
                self.lang_dict.add_with(
                    "en",
                    "Displays the channels where the bot is connected or their quantity.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Exibe os canais em que o bot está conectado ou a quantidade deles.",
                )
            return self._untangle_str(ctx, "description")

    Channels: Channels
