from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TranslationBase
from bot.ext.translations.extras import TBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class AccountAge(TBase):
        def __init__(self):
            super().__init__()

        def accountage(
            self,
            ctx: Context,
            mention: str,
            date: str,
            delta: str,
            success: bool = True,
            handle: str | None = None,
        ):
            response = Response(ctx=ctx, success=success, handle=handle, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{} created the account on {} ({} ago)")
                self.lang_dict.add_with(["pt_br", "pt"], "{} criou a conta em {} (há {})")
            return response.format_response(self._untangle_str(ctx, self._cname), mention, date, delta)

        accountage: Response = accountage

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Check the Twitch account creation date.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Verifica a data de criação de uma conta da Twitch.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Usage: {}accountage (username)")
                self.lang_dict.add_with(["pt_br", "pt"], "Uso: {}accountage (nome_de_usuário)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Returns the creation date of a Twitch account and how long ago it was created. "
                    "If no username is given, it checks your own account.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Retorna a data em que uma conta da Twitch foi criada e há quanto tempo isso aconteceu. "
                    "Se nenhum nome for fornecido, verifica sua própria conta.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "args": "accountage mr_chuw",
                                "response": "@mr_chuw created the account on 20/01/2019 19:34:45 (6 year ago).",
                            },
                            {
                                "args": "accountage",
                                "response": "@your_name created the account on 20/01/2019 19:34:45 (6 year ago).",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "args": "accountage mr_chuw",
                                "response": "@mr_chuw criou a conta em 20/01/2019 19:34:45 (há 6 anos)",
                            },
                            {
                                "args": "accountage",
                                "response": "@seu_nome criou a conta em 20/01/2019 19:34:45 (há 6 anos).",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

    AccountAge: AccountAge
