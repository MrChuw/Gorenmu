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

    class Live(TBase):
        def __init__(self):
            super().__init__()

        def never_streamed(self, ctx, name: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "User {} has never opened any stream.")
                self.lang_dict.add_with(["pt_br", "pt"], "Usuário {} nunca abriu nenhuma stream.")
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def response(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def title(self, ctx: Context, title) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Title: {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Título: {}.")
            return self._untangle_str(ctx, self._cname).format(title)

        def last_stream(self, ctx: Context, time_natural, time_precise) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Last stream: {} ({}).")
                self.lang_dict.add_with(["pt_br", "pt"], "Última transmissão: {} ({}).")
            return self._untangle_str(ctx, self._cname).format(time_natural, time_precise)

        def stream_started(self, ctx: Context, time_natural, time_precise) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Stream started: {} ({}).")
                self.lang_dict.add_with(["pt_br", "pt"], "Transmissão iniciada: {} ({}).")
            return self._untangle_str(ctx, self._cname).format(time_natural, time_precise)

        def views(self, ctx: Context, views) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Views: {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Visualizações: {}.")
            return self._untangle_str(ctx, self._cname).format(views)

        def playing(self, ctx: Context, game) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Playing: {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Jogando: {}.")
            return self._untangle_str(ctx, self._cname).format(game)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Shows information about a channel's current or last broadcast.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Mostra informações sobre a live atual ou a última de um canal."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}live (channel or id)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}live (canal ou id)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Displays details about the current stream or the last broadcast of the specified Twitch channel. "
                    "Includes title, time since started, viewers, game, and VOD link if available. "
                    "If no channel is specified, uses the current one.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Exibe detalhes sobre a live atual ou a última do canal da Twitch especificado. "
                    "Inclui título, tempo desde o início, visualizações, jogo e link do VOD se disponível. "
                    "Se nenhum canal for especificado, usa o canal atual.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "Live channel:",
                                "args": "xXCoolNickXx",
                                "response": "Title: Cool Stream Title. || "
                                "Stream started: a month ago (1 month, 1 day, 1 hour). || "
                                " Views: 42069. || "
                                "Playing: Coolest Game. || "
                                "https://www.twitch.tv/xXCoolNickXx https://www.twitch.tv/videos/1324",
                            },
                            {
                                "prefix": "Offline channel with recent VOD:",
                                "args": "xXCoolNickXx",
                                "response": "Title: Cool Stream Title. || "
                                "Last stream: a month ago (1 month, 1 day, 1 hour). || "
                                "https://www.twitch.tv/xXCoolNickXx https://www.twitch.tv/videos/1324",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "Canal ao vivo:",
                                "args": "xXCoolNickXx",
                                "response": "Título: Cool Stream Title. || "
                                "Transmissão iniciada: há um mês (1 mês, 1 dia, 1 hora). || "
                                "Visualizações: 42069. || "
                                "Jogando: Coolest Game. || "
                                "https://www.twitch.tv/xXCoolNickXx https://www.twitch.tv/videos/1324",
                            },
                            {
                                "prefix": "Canal offline com VOD recente:",
                                "args": "xXCoolNickXx",
                                "response": "Título: Cool Stream Title. || "
                                "Última transmissão: há um mês (1 mês, 1 dia, 1 hora). || "
                                "https://www.twitch.tv/xXCoolNickXx https://www.twitch.tv/videos/1324",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Live: Live
