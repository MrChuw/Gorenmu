# -*- coding: utf-8 -*-
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

    class RandomColor(TBase):
        def __init__(self):
            super().__init__()

        def api_down(self, ctx: Context) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "thecolorapi.com is inaccessible")
                self.lang_dict.add_with(["pt_br", "pt"], "thecolorapi.com esta inacessível")
            return self._untangle_str(ctx, self._cname)

        def response_url(self, ctx: Context, hex_code, name, url) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{} is {}. {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{} é {}. {}")
            return response.format_response(self._untangle_str(ctx, self._cname), hex_code, name, url)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Sends a random color.")
                self.lang_dict.add_with(["pt_br", "pt"], "Envia uma cor aleatória.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}random_color or add type:hex / type:rgb to specify the type.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Para usar: {}random_color ou adicione type:hex / type:rgb para especificar o tipo.",
                )
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command responds with the HEX code of a random color and a link to an image of the color.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando responde com o código HEX de uma cor aleatória e um link para uma imagem da cor.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", CommandExemples([{"response": "#<HEX> <Color Name> <Link to the color image>"}])
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], CommandExemples([{"response": "#<HEX> <Nome da cor> <Link para a imagem da cor>"}])
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    RandomColor: RandomColor
