from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase, TranslationEntry

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .color import ColorCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: ColorCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: ColorCmd = parent
        self.populate_subclasses(parent=self)

    class Color(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Color"

        def color(self, res1, res2) -> Response:
            text = self.get_text(self._cname, res1=res1, res2=res2)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def no_user_hex(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def user_not_color(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def user_color(
            self, name: str | None = None, hex_value: str | None = None, hex_name: str | None = None
        ) -> str | TranslationEntry:
            if name is None:
                return self.get_entry(self._cname)

            return self.get_text(self._cname, name=name, hex_value=hex_value, hex_name=hex_name)

        def hex_color(self, hex_value: str | None = None, hex_name: str | None = None) -> str | TranslationEntry:
            if not hex_value or not hex_name:
                return self.get_entry(self._cname)
            return self.get_text(self._cname, hex_value=hex_value, hex_name=hex_name)

        def saved_color(self, hex_value: str | None = None, hex_name: str | None = None) -> str | TranslationEntry:
            if not hex_value or not hex_name:
                return self.get_entry(self._cname)
            return self.get_text(self._cname, hex_value=hex_value, hex_name=hex_name)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            name = self._cname
            prefix = prefix
            return self.get_text(name, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {
                        "prefix": self.get_text("cmd_ex1_prefix"),
                        "args": "mr_chuw",
                        "response": self.get_text("cmd_ex1_res"),
                    },
                    {
                        "prefix": self.get_text("cmd_ex2_prefix"),
                        "args": "#FF4500",
                        "response": self.get_text("cmd_ex2_res"),
                    },
                    {
                        "prefix": self.get_text("cmd_ex3_prefix"),
                        "args": "mr_chuw",
                        "response": self.get_text("cmd_ex3_res"),
                    },
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

    Color: Color
