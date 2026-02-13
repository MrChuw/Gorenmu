from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .random_line import RandomLineCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: RandomLineCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: RandomLineCmd = parent
        self.populate_subclasses(parent=self)

    class RandomLine(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "RandomLine"

        def no_user_message(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def no_channel_message(self, channel_name: str) -> Response:
            text = self.get_text(self._cname, channel_name=channel_name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def no_user_on_channel(self, name: str, channel_name: str) -> Response:
            text = self.get_text(self._cname, name=name, channel_name=channel_name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def search_timeout(self, name: str, channel_name: str) -> Response:
            text = self.get_text(self._cname, name=name, channel_name=channel_name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def random_line(self, content: str, time: str, nick: str) -> Response:
            text = self.get_text(self._cname, content=content, time=time, nick=nick)
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
                    {"response": self.get_text("cmd_res_curr_chan")},
                    {
                        "args": "user:(user_name)",
                        "response": self.get_text("cmd_res_user_curr"),
                    },
                    {
                        "args": "channel:(channel_name)",
                        "response": self.get_text("cmd_res_spec_chan"),
                    },
                    {
                        "args": "channel:(channel_name) user:(user_name)",
                        "response": self.get_text("cmd_res_user_spec"),
                    },
                    {
                        "args": "channel:global user:(user_name)",
                        "response": self.get_text("cmd_res_user_glob"),
                    },
                    {
                        "args": "channel:global",
                        "response": self.get_text("cmd_res_glob"),
                    },
                ]
            )

        # endregion

    RandomLine: RandomLine
