from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .ping import PingCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: PingCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: PingCmd = parent
        self.populate_subclasses(parent=self)

    class Ping(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Ping"

        def ping(self, ping: str, tmi: str, mem: str, started: str) -> Response:
            text = self.get_text(self._cname, ping=ping, tmi=tmi, mem=mem, started=started)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix1=prefix, prefix2=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples([{"args": "", "response": self.get_text("cmd_res")}])

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm_tmi_title"),
                        "message": self.get_text("adm_tmi_msg"),
                    },
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm_ram_title"),
                        "message": self.get_text("adm_ram_msg"),
                    },
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm_up_title"),
                        "message": self.get_text("adm_up_msg"),
                    },
                ]
            )

        # endregion

    Ping: Ping
