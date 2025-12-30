from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class UserId(TBase):
        def __init__(self):
            super().__init__()

        def id_or_name(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def unknown_name(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Invalid username: @{}")
                self.lang_dict.add_with(["pt_br", "pt"], "Nome de usuário inválido: @{}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def unknown_id(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Invalid id: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "ID inválido: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Transform user ID into username and vice versa.")
                self.lang_dict.add_with(["pt_br", "pt"], "Transformar o id do usuário em nome de usuário e vice-versa.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}userid (username/id)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}userid (username/id)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Transform user ID into username and vice versa.")
                self.lang_dict.add_with(["pt_br", "pt"], "Transformar o id do usuário em nome de usuário e vice-versa.")
            return self._untangle_str(ctx, self._cname)

        # endregion

    UserId: UserId
