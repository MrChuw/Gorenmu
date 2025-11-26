from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Echo(TBase):
        def __init__(self):
            super().__init__()

        def echo(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=True, handle="echo", response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("helper"):
                self.lang_dict.add_with("en", "Repeats the message you send.")
                self.lang_dict.add_with(["pt_br", "pt"], "Repete a mensagem que você enviar.")
            return self._untangle_str(ctx, "helper")

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once("usage"):
                self.lang_dict.add_with("en", "{}echo (message)")
                self.lang_dict.add_with(["pt_br", "pt"], "{}echo (mensagem)")
            return self._untangle_str(ctx, "usage").format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("description"):
                self.lang_dict.add_with("en", "Sends back the same message provided by the user.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Envia de volta a mesma mensagem fornecida pelo usuário.",
                )
            return self._untangle_str(ctx, "description")

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once("admonitions"):
                self.lang_dict.add_with(
                    "en",
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "title": "Punctuations!",
                                "message": (
                                    "If any type of punctuation is placed at the beginning of the message, "
                                    "an invisible character will be inserted to prevent the use of commands."
                                ),
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
                                "title": "Pontuação!",
                                "message": (
                                    "Se algum tipo de pontuação for colocado no início da mensagem, "
                                    "um caractere invisível será inserido para evitar o uso de comandos."
                                ),
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, "admonitions")

    Echo: Echo
