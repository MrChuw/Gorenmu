from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .join import JoinCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: JoinCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: JoinCmd = parent
        self.populate_subclasses(parent=self)

    class Join(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Join"

        def website(self, scopes: list[str], explanation: str = "") -> Response:
            ctx = self.ctx_get()
            url = ctx.bot.config.ApisConfig.join_url.with_path("oauth")
            url = url.with_query(scopes=" ".join(scopes), force_verify="true")

            text = self.get_text(self._cname, url=str(url), explanation=explanation)
            return Response(ctx=ctx, success=True, response_string=text)

        def already_in_chat(self, prefix: str) -> Response:
            text = self.get_text(self._cname, prefix=prefix)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "position": "top",
                        "admonition_type": "warning",
                        "title": self.get_text("adm_title"),
                        "message": self.get_text("adm_msg"),
                    }
                ]
            )

        # endregion

    Join: Join
