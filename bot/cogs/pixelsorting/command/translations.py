from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .pixelsorting import PixelSortingCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: PixelSortingCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: PixelSortingCmd = parent
        self.populate_subclasses(parent=self)

    class PixelSorting(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "PixelSorting"

        def no_url(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def invalid_content_type(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def took_too_long(self, time: str | int | float) -> Response:
            text = self.get_text(self._cname, time=str(time))
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def image(self, shortened: str) -> Response:
            text = self.get_text(self._cname, shortened=shortened)
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
                    {
                        "prefix": self.get_text("cmd_no_args_prefix"),
                        "args": self.get_text("cmd_url_arg"),
                        "response": self.get_text("cmd_res"),
                    },
                    {
                        "prefix": self.get_text("cmd_args_prefix"),
                        "args": self.get_text("cmd_full_args"),
                        "response": self.get_text("cmd_res"),
                    },
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "warning",
                        "position": "top",
                        "title": self.get_text("adm_res_title"),
                        "message": self.get_text("adm_res_msg"),
                    },
                    {
                        "admonition_type": "info",
                        "position": "top",
                        "title": self.get_text("adm_modes_title"),
                        "message": self.get_text("adm_modes_msg"),
                    },
                    {
                        "admonition_type": "info",
                        "position": "middle",
                        "title": self.get_text("adm_mask_title"),
                        "message": self.get_text("adm_mask_msg"),
                    },
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm_rand_title"),
                        "message": self.get_text("adm_rand_msg"),
                    },
                ]
            )

        # endregion

    PixelSorting: PixelSorting
