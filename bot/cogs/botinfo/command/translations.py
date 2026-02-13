from __future__ import annotations

from typing import TYPE_CHECKING

import yarl

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .botinfo import BotInfoCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: BotInfoCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: BotInfoCmd = parent
        self.populate_subclasses(parent=self)

    class BotInfo(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "BotInfo"

        def info(self, channels: int | str, commands: int | str, name: str, url: yarl.URL) -> Response:
            text = self.get_text(self._cname, channels=channels, commands=commands, name=name, url=url.human_repr())
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def site(self, site_url: yarl.URL) -> Response:
            text = self.get_text(self._cname, site_url=str(site_url))
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def uptime(self, time: str) -> Response:
            text = self.get_text(self._cname, time=time)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples([{"response": self.get_text("cmd_ex1_res")}])

    BotInfo: BotInfo
