from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses(parent=self)

    class Join(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)

        def website(self, scopes: list[str], explanation: str = "") -> Response:
            ctx = self.ctx_get()
            url = ctx.bot.config.ApisConfig.join_url.with_path("oauth")
            url = url.with_query(scopes=" ".join(scopes), force_verify="true")
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", f"{url} {explanation}")
                self.lang_dict.add_with(["pt_br", "pt"], f"{url} {explanation}")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def already_in_chat(self, prefix: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "I'm already in your chat. I reactivated myself to make things easier. Prefix: {}"
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Eu já estou no seu chat. Eu me reativei para facilitar as coisas. Prefixo: {}"
                )
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), prefix)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This command sends the link to allow the bot to join your chat.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Este comando envia o link que permite ao bot entrar no seu chat."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}userid (username/id)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}userid (username/id)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This command sends the link to allow the bot to join your chat.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Este comando envia o link que permite ao bot entrar no seu chat."
                )
            return self._untangle_str(ctx, self._cname)

        # def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
        #     with self.lang_dict.once(self._cname):
        #         self.lang_dict.add_with("en", CommandExemples([]))
        #         self.lang_dict.add_with(["pt_br", "pt"], CommandExemples([]))
        #     return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    Admonitions(
                        [
                            {
                                "position": "top",
                                "admonition_type": "warning",
                                "title": "Tags!",
                                "message": "Due to possible future changes on Twitch, "
                                "I'm also changing how the bot joins the channel.",
                            }
                        ]
                    ),
                )

                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "position": "top",
                                "admonition_type": "warning",
                                "title": "Tags!",
                                "message": "Devido possíveis mudanças futuras na Twitch, "
                                "também estou alterando a forma como o bot entra no canal.",
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Join: Join
