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

    class BotInfo(TBase):
        def __init__(self):
            super().__init__()

        def info(self, ctx: Context, channels, commands, name, url) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "I am connected to {} channels, with {} commands, "
                    "made by @{} in Python (Twitchio). Bot website: {}",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Estou conectado a canais {}, com comandos {}, "
                    "criados por @{} em Python (Twitchio). Site do bot: {}",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), channels, commands, name, url)

        def site(self, ctx: Context, site_url) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), site_url)

        def uptime(self, ctx: Context, time) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "I woke up {} ago.")
                self.lang_dict.add_with(["pt_br", "pt"], "Eu acordei há {}")
            return response.format_response(self._untangle_str(ctx, self._cname), time)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Shows general bot statistics, uptime, and metadata like site and developer.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Exibe estatísticas gerais do bot, tempo de atividade e metadados como site e desenvolvedor.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {0}botinfo | {0}site | {0}uptime")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {0}botinfo | {0}site | {0}uptime")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Displays information about the bot, such as number of channels, "
                    "total commands, developer, uptime, and site.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Mostra informações sobre o bot, como número de canais, "
                    "total de comandos, desenvolvedor, tempo online e site.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "response": "I am connected to 10 channels, with 50 commands, "
                                "made by @DevName in Python (Twitchio). Bot website: https://example.com"
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "response": "Estou conectado a 10 canais, com 50 comandos, "
                                "feito por @DevName em Python (Twitchio). Site do bot: https://exemplo.com"
                            }
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    BotInfo: BotInfo
