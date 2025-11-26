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

    class RandomLine(TBase):
        def __init__(self):
            super().__init__()

        def no_user_message(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Couldn't find any message from user @{}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Não encontrei nenhuma mensagem de @{}.")
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def no_channel_message(self, ctx: Context, channel_name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Couldn't find any message from channel @{}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Não encontrei nenhuma mensagem do canal @{}.")
            return response.format_response(self._untangle_str(ctx, self._cname), channel_name)

        def no_user_on_channel(self, ctx: Context, name, channel_name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Couldn't find any message from @{} in @{}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Não encontrei nenhuma mensagem de @{} in @{}.")
            return response.format_response(self._untangle_str(ctx, self._cname), name, channel_name)

        def search_timeout(self, ctx: Context, name, channel_name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "30s has passed and I has unable to find a message from user @{} on channel @{}",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "30s se passaram e não consegui encontrar uma mensagem do usuário @{} no canal @{}",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), name, channel_name)

        def random_line(self, ctx: Context, content, time, nick) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{} (sent {} ago by @{} )")
                self.lang_dict.add_with(["pt_br", "pt"], "{} (enviado há {} por @{} )")
            return response.format_response(self._untangle_str(ctx, self._cname), content, time, nick)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Fetches a random message from the channel or from a user in the channel.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Pega uma mensagem aleatória do canal ou de um usuário em um canal.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "to use: `{0}rl channel:(channel_name)` or `{0}rl user:(user_name)` or "
                    "`{0}rl` or `{0}rl channel:(channel_name) user:(user_name)`",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Para usar: `{0}rl channel:<nome do canal>` or `{0}rl user:<nome do usuário>` or "
                    '`{0}rl` or`{0}rl channel:<nome do canal> user:<nome do usuário> "',
                )
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command selects a random message depending on the options provided.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando seleciona uma mensagem aleatória dependendo das opções fornecidas.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"response": "(it will send a random message from the current channel)"},
                            {
                                "args": "user:(user_name)",
                                "response": "(it will send a random message from the user on the current channel)",
                            },
                            {
                                "args": "channel:(channel_name)",
                                "response": "(it will send a random message from a specific channel)",
                            },
                            {
                                "args": "channel:(channel_name) user:(user_name)",
                                "response": "(it will send a random message from a user in a specific channel)",
                            },
                            {
                                "args": "channel:global user:(user_name)",
                                "response": "(it will send a random message from a user in all channels)",
                            },
                            {
                                "args": "channel:global",
                                "response": "(it will send a random message from in a all channel)",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"response": "(irá enviar uma mensagem aleatória do canal atual)"},
                            {
                                "args": "user:(nome_do_usuário)",
                                "response": "(irá enviar uma mensagem aleatória do usuário no canal atual)",
                            },
                            {
                                "args": "channel:(nome_do_canal)",
                                "response": "(irá enviar uma mensagem aleatória de um canal específico)",
                            },
                            {
                                "args": "channel:(nome_do_canal) user:(nome_do_usuário)",
                                "response": "(irá enviar uma mensagem aleatória de um usuário em um canal específico)",
                            },
                            {
                                "args": "channel:global user:(nome_do_usuário)",
                                "response": "(irá enviar uma mensagem aleatória de um usuário em todos os canais)",
                            },
                            {
                                "args": "channel:global",
                                "response": "(irá enviar uma mensagem aleatória de todos os canais)",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    RandomLine: RandomLine
