from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .lastseen import LastSeenCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: LastSeenCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: LastSeenCmd = parent
        self.populate_subclasses(parent=self)

    class LastSeen(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "LastSeen"

        def bot(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def author(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def not_found(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def not_authorized(self, name: str, delta: str) -> Response:
            text = self.get_text(self._cname, name=name, delta=delta)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def last_seen(self, name: str, channel: str, content: str, delta: str) -> Response:
            text = self.get_text(self._cname, name=name, channel=channel, content=content, delta=delta)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.
        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {"args": "", "response": self.get_text("cmd_ex1_res")},
                    {"args": "user_nick", "response": self.get_text("cmd_ex2_res")},
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "info",
                        "position": "top",
                        "title": self.get_text("adm_title"),
                        "message": self.get_text("adm_msg"),
                    }
                ]
            )

        # endregion

    LastSeen: LastSeen
