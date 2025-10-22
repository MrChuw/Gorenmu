# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class FollowAge(TBase):
        def __init__(self):
            super().__init__()

        def follow(self, ctx: Context, mention: str, mention_channel: str, delta: str) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{} follows {} for {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{} segue {} {}")
            return response.format_response(self._untangle_str(ctx, self._cname), mention, mention_channel, delta)

        def not_followed(self, ctx: Context, mention, mention_channel) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{} does not follow {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{} não segue {}")
            return response.format_response(self._untangle_str(ctx, self._cname), mention, mention_channel)

        def self_follow(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Obviously you can't follow yourself.")
                self.lang_dict.add_with(["pt_br", "pt"], "Obviamente vc não pode seguir vc mesmo.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Command used to check how long someone has been following a channel.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Comando utilizado para verificar a quanto tempo alguém segue um canal."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{}followage (user) (channel)")
                self.lang_dict.add_with(["pt_br", "pt"], "{}followage (usuário) (canal)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Command used to check how long someone has been following a channel.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Comando utilizado para verificar a quanto tempo alguém segue um canal."
                )
            return self._untangle_str(ctx, self._cname)

        # endregion

    FollowAge: FollowAge
