from __future__ import annotations

from typing import TYPE_CHECKING

import yarl

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .help import HelpCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: HelpCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: HelpCmd = parent
        self.populate_subclasses(parent=self)

    class Help(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Help"

        def help(self, prefix, name, helper, cooldown, url: yarl.URL, alias) -> Response:
            text = self.get_text(
                self._cname,
                prefix=prefix,
                name=name,
                helper=helper,
                cooldown=cooldown,
                url=url.human_repr(),
                alias=alias,
            )
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def command_site(self, url: yarl.URL) -> Response:
            text = self.get_text(self._cname, url=url.human_repr())
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def suggested_command(self, content, suggested) -> Response:
            text = self.get_text(self._cname, content=content, suggested=suggested)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

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
                        "prefix": self.get_text("cmd_ex1_prefix"),
                        "args": "ping",
                        "response": self.get_text("cmd_ex1_res"),
                    },
                    {
                        "prefix": self.get_text("cmd_ex2_prefix"),
                        "args": "pign",
                        "response": self.get_text("cmd_ex2_res"),
                    },
                    {"prefix": self.get_text("cmd_ex3_prefix"), "args": "", "response": self.get_text("cmd_ex3_res")},
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm_suggestions_title"),
                        "message": self.get_text("adm_suggestions_msg"),
                    },
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm_meta_title"),
                        "message": self.get_text("adm_meta_msg"),
                    },
                ]
            )

        # endregion

    Help: Help
