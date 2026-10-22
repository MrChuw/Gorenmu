from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .userid import UserIdCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: UserIdCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.UserId: UserId = UserId(self)


class UserId(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "UserId"
        super().__init__(parent, __file__)

    def id_or_name(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def unknown_name(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def unknown_id(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)
