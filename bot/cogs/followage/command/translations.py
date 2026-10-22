from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .followage import FollowAgeCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: FollowAgeCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.FollowAge: FollowAge = FollowAge(self)


class FollowAge(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "FollowAge"
        super().__init__(parent, __file__)

    def follow(self, mention: str, mention_channel: str, delta: str) -> Response:
        text = self.get_text(self._cname, mention=mention, channel=mention_channel, delta=delta)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def not_followed(self, mention: str, mention_channel: str) -> Response:
        text = self.get_text(self._cname, mention=mention, channel=mention_channel)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def self_follow(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples([])

