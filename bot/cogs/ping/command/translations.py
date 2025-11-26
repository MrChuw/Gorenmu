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

    class Ping(TBase):
        def __init__(self):
            super().__init__()

        def ping(self, ctx: Context, ping, tmi, mem, started) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{} || TMI: {} || RAM: {} || {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{} || TMI: {} || RAM: {} || {}")
            return response.format_response(self._untangle_str(ctx, self._cname), ping, tmi, mem, started)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Command to check if the bot is alive.")
                self.lang_dict.add_with(["pt_br", "pt"], "Comando para verificar se o bot esta vivo.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}ping or {}pong")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}ping ou {}pong")
            return self._untangle_str(ctx, self._cname).format(prefix, prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command measures the bot's response time, shows memory usage, "
                    "and how long the bot has been online.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando mede o tempo de resposta do bot, mostra o uso de "
                    "memória e há quanto tempo o bot está online.",
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
                                "response": "pong 🏓 || TMI: 123 ms || RAM: 123 MB || up for 1 hour",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "args": "",
                                "response": "pong 🏓 || TMI: 123 ms || RAM: 123 MB || ligado há 1 hora",
                            }
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
                                "position": "bottom",
                                "title": "TMI",
                                "message": "TMI stands for Internal Message Time — "
                                "the time between the message being sent and the bot replying.",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "RAM",
                                "message": "Shows how much RAM memory the current bot process is using.",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "Uptime",
                                "message": "Shows how long the bot has been online since the last boot.",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "TMI",
                                "message": "TMI representa o tempo de mensagem interna — "
                                "o tempo entre o envio da sua mensagem e a execução do comando.",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "RAM",
                                "message": "Mostra quanta memória RAM o processo atual do bot está utilizando.",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "Tempo de atividade",
                                "message": "Mostra há quanto tempo o bot está online desde o último boot.",
                            },
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Ping: Ping
