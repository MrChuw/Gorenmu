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

    class LastSeen(TBase):
        def __init__(self):
            super().__init__()

        def bot(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "I am everywhere, at every moment...")
                self.lang_dict.add_with(["pt_br", "pt"], "eu estou em todos os lugares, a todo momento...")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def author(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you were last seen here ☝️")
                self.lang_dict.add_with(["pt_br", "pt"], "você foi visto pela última vez aqui ☝️")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def not_found(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "@{} has not been registered yet.")
                self.lang_dict.add_with(["pt_br", "pt"], "@{} ainda não foi registrado.")
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def not_authorized(self, ctx: Context, name, delta) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "@{} was last seen {}")
                self.lang_dict.add_with(["pt_br", "pt"], "@{} foi visto ultima vez {}")
            return response.format_response(self._untangle_str(ctx, self._cname), name, delta)

        def last_seen(self, ctx: Context, name, channel, content, delta) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "@{} was last seen in @{}: {} ({})")
                self.lang_dict.add_with(["pt_br", "pt"], "@{} foi visto em @{} pela última vez: {} ({})")
            return response.format_response(self._untangle_str(ctx, self._cname), name, channel, content, delta)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Used to see the last time a user was online.")
                self.lang_dict.add_with(["pt_br", "pt"], "Usado para ver a ultima vez que um usuário esteve online.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Usage: {}lastseen (user)")
                self.lang_dict.add_with(["pt_br", "pt"], "Uso: {}lastseen (usuário)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.
        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Command used to check when a user was last seen in a chat.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Comando utilizado para verificar quando foi a ultima vez que um usuário foi visto em um chat.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "args": "",
                                "response": "@channel_name was last seen in @other_channel: "
                                "Message content (1 day ago)",
                            },
                            {
                                "args": "user_nick",
                                "response": "@user_nick was last seen in @other_channel: "
                                "Message content (2 days ago)",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "args": "",
                                "response": "@nome_do_canal foi visto em @outro_canal pela última vez: "
                                "Conteúdo da mensagem (ha 1 dia)",
                            },
                            {
                                "args": "user_nick",
                                "response": "@user_nick foi visto em @outro_canal pela última vez: "
                                "Conteúdo da mensagem (ha 2 dia)",
                            },
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
                                "admonition_type": "info",
                                "position": "top",
                                "title": "User Mention",
                                "message": "If the user has disabled mentions, the content of the last "
                                "message and exact time will not be shown.",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "info",
                                "position": "top",
                                "title": "User Mention",
                                "message": "Caso o usuário tenha desabilitado a menção o conteúdo da ultima "
                                "mensagem e exato tempo não sera mostrado.",
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    LastSeen: LastSeen
