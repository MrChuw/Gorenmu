# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Safebooru(TBase):
        def __init__(self):
            super().__init__()

        def original(self, ctx: Context) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "Original")
            return self._untangle_str(ctx, self._cname)

        def preview(self, ctx: Context) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "Preview")
            return self._untangle_str(ctx, self._cname)

        def too_much_tags(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Number of tags exceeded the allowed limit of {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Quantidade de tags ultrapassou o limite permitido de {}.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def success(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Command used to generate random images from Safebooru.")
                self.lang_dict.add_with(["pt_br", "pt"], "Comando usado para gerar imagens aleatórias de Safebooru.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}safebooru (tags)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}safebooru (tags)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command is used to generate random images from Safebooru and shorten them for convenience.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando é usado para gerar imagens aleatórias de Safebooru e encurtá-las para conveniência.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"response": "Original: (URL) || Preview: (URL)"},
                            {"args": "some_tag", "response": "Original: (URL) || Preview: (URL)"},
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"response": "Original: (URL) || Preview: (URL)"},
                            {"args": "some_tag", "response": "Original: (URL) || Preview: (URL)"},
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "title": "Tags!",
                                "message": 'For tags containing spaces, the space must be replaced with "_".',
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "title": "Tags!",
                                "message": 'Para tags contendo espaços, o espaço deve ser substituído por "_".',
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Safebooru: Safebooru
