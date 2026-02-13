from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .imgur import ImgurCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: ImgurCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: ImgurCmd = parent
        self.populate_subclasses(parent=self)

    class Imgur(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Imgur"

        def time(self, time) -> str:
            return self.get_text(self._cname, time=time)

        def all_images(self, embed_url) -> str:
            return self.get_text(self._cname, embed_url=embed_url)

        def all_images2(self, embed_url) -> str:
            return self.get_text(self._cname, embed_url=embed_url)

        def took_too_long(self, passed) -> Response:
            text = self.get_text(self._cname, passed=passed)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def links(self, responses) -> Response:
            return Response(ctx=self.ctx_get(), success=True, response_list=responses)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [{"prefix": self.get_text("cmd_ex1_prefix"), "args": "5", "response": self.get_text("cmd_ex1_res")}]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "warning",
                        "position": "top",
                        "title": self.get_text("adm_warn_title"),
                        "message": self.get_text("adm_warn_msg"),
                    }
                ]
            )

        # endregion

    Imgur: Imgur
