from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .live import LiveCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: LiveCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: LiveCmd = parent
        self.populate_subclasses(parent=self)

    class Live(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Live"

        def never_streamed(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def response(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def title(self, title: str) -> str:
            return self.get_text(self._cname, title=title)

        def last_stream(self, time_natural: str, time_precise: str) -> str:
            return self.get_text(self._cname, time_natural=time_natural, time_precise=time_precise)

        def stream_started(self, time_natural: str, time_precise: str) -> str:
            return self.get_text(self._cname, time_natural=time_natural, time_precise=time_precise)

        def views(self, views: str | int) -> str:
            return self.get_text(self._cname, views=str(views))

        def playing(self, game: str) -> str:
            return self.get_text(self._cname, game=game)

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
                    {
                        "prefix": self.get_text("cmd_live_prefix"),
                        "args": "xXCoolNickXx",
                        "response": self.get_text("cmd_live_res"),
                    },
                    {
                        "prefix": self.get_text("cmd_off_prefix"),
                        "args": "xXCoolNickXx",
                        "response": self.get_text("cmd_off_res"),
                    },
                ]
            )

        # endregion

    Live: Live
