from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .channels import ChannelsCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: ChannelsCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.Channels: Channels = Channels(self)


class Channels(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Channels"
        super().__init__(parent, __file__)

    def quantity(self, count: int | str) -> Response:
        text = self.get_text(self._cname, count=count)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def names(self, list_str: str) -> Response:
        text = self.get_text(self._cname, list=list_str)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)
