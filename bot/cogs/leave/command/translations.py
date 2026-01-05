from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses(parent=self)

    class Leave(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)

        def not_on_channel(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "I'm not on your channel.")
                self.lang_dict.add_with(["pt_br", "pt"], "Eu não estou no seu canal.")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        def channel_removed(self, args) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Your channel @{} has been successfully removed.")
                self.lang_dict.add_with(["pt_br", "pt"], "Seu canal @{} foi removido com sucesso.")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), args)

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This command is used to remove the bot from your chat.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando é usado para remover o bot do seu chat.")
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}leave")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}leave")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This command is used to remove the bot from your chat.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando é usado para remover o bot do seu chat.")
            return self._untangle_str(self.ctx_get(), self._cname)

        # endregion

    Leave: Leave
