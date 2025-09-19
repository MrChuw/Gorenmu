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

    class Count(TBase):
        def __init__(self):
            super().__init__()

        def character_count(self, ctx: Context, length, punc, upper, special) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "There is a total of {} characters. Of these, {} are punctuation marks, "
                    "{} are uppercase letters, and {} are special characters.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Há um total de caracteres {}. Destes, {} são sinais de pontuação, "
                    "{} são letras maiúsculas, e {} são caracteres especiais.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), length, punc, upper, special)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Counts the number of symbols in a text or a URL.")
                self.lang_dict.add_with(["pt_br", "pt"], "Conta o número de símbolos em um texto ou uma URL.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}count (text) or type:url (URL URL URL URL)")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Para usar: {}count <texto> ou type:url <quantas URLs você quiser>"
                )
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command can count the number of characters, uppercase letters, "
                    "punctuation marks, and special characters in a text or the content of a URL. "
                    "If you provide a link and the tag `type:url`, the command fetches the page's "
                    "content and performs the count based on what it finds. And it will cache the page "
                    "content for 30 minutes (thirty minutes).",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando pode contar o número de caracteres, letras maiúsculas, sinais de "
                    "pontuação e caracteres especiais em um texto ou no conteúdo de uma URL. "
                    "Se você fornecer um link e a tag `type:url`, o comando buscará o conteúdo da página "
                    "e realizará a contagem com base no que encontrar. E ele armazenará em cache o conteúdo "
                    "da página por 30 minutos (trinta minutos).",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "args": "some nice text! with some 😄 caracteres, spacial!",
                                "response": "There is a total of 48 characters. Of these, 3 are punctuation "
                                "marks, 0 are uppercase letters, and 1 are special characters.",
                            },
                            {
                                "args": "https://example.org/",
                                "response": "There is a total of 20 characters. Of these, 5 are punctuation "
                                "marks, 0 are uppercase letters, and 0 are special characters.",
                            },
                            {
                                "args": " type:url https://example.com/",
                                "response": "There is a total of 1257 characters. Of these, 188 are "
                                "punctuation marks, 21 are uppercase letters, and 0 are special characters.",
                            },
                            {
                                "args": "type:url https://example.com/ https://example.org/",
                                "response": "User, There is a total of 2514 characters. Of these, 376 are "
                                "punctuation marks, 42 are uppercase letters, and 0 are special characters.",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "response": "Há um total de 62 caracteres. Destes, 3 são marcas de pontuação, "
                                "0 são letras maiúsculas, e 1 são caracteres especiais.",
                                "args": "uma boa mensagem! com alguns 😄 caracteres caracteres, spacial!",
                            },
                            {
                                "args": "https://example.org/",
                                "response": "Há um total de 20 caracteres. Destes, 5 são sinais de pontuação, "
                                "0 são letras maiúsculas, e 0 são caracteres especiais.",
                            },
                            {
                                "args": " type:url https://example.com/",
                                "response": "Há um total de 1257 caracteres. Destes, 188 são sinais de pontuação, "
                                "21 são letras maiúsculas, e 0 são caracteres especiais.",
                            },
                            {
                                "args": "type:url https://example.com/ https://example.org/",
                                "response": "Usuário, Há um total de 2514 caracteres. Destes, 376 são sinais de "
                                "pontuação, 42 são letras maiúsculas, e 0 são caracteres especiais.",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Count: Count
