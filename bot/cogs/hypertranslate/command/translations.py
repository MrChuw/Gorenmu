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

    class HyperTranslate(TBase):
        def __init__(self):
            super().__init__()

        def base_lang(self, ctx: Context) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "en")
                self.lang_dict.add_with(["pt_br", "pt"], "pt")
            return self._untangle_str(ctx, self._cname)

        def starter_string(self, ctx: Context) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Translating the text…")
                self.lang_dict.add_with(["pt_br", "pt"], "Traduzindo o texto…")
            return self._untangle_str(ctx, self._cname)

        def unexpected_error(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "The text could not be translated.")
                self.lang_dict.add_with(["pt_br", "pt"], "O texto não pôde ser traduzido.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def translation(self, ctx: Context, text) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{}")
                self.lang_dict.add_with(["pt_br", "pt"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), text)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Translates a text into random languages depending on how many times the user requests.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Traduzir um texto em idiomas aleatórios dependendo de quantas vezes o usuário solicita.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}hypertranslate (number of times) text")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Para usar: {}hypertranslate (número de vezes) texto",
                )
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Command based on [ravbug](https://www.ravbug.com/hypertranslate/) that translates a text "
                    "into random languages depending on how many times the user requests.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Comando baseado em [ravbug](https://www.ravbug.com/hypertranslate/) que traduz um texto "
                    "em idiomas aleatórios dependendo de quantas vezes o usuário solicita.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples([{"args": "10 test", "response": "<some random text.>"}]),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples([{"args": "10 teste", "response": "<algum texto aleatório.>"}]),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    HyperTranslate: HyperTranslate
