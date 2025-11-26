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

    class Bug(TBase):
        def __init__(self):
            super().__init__()

        def bug(self, ctx: Context, bug_id) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "your bug has been reported 🐛 (ID {})")
                self.lang_dict.add_with(["pt_br", "pt"], "seu bug foi reportado 🐛 (ID {})")
            return response.format_response(self._untangle_str(ctx, self._cname), bug_id)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "report a bug that occurred in the Bot.")
                self.lang_dict.add_with(["pt_br", "pt"], "reporte um bug que ocorreu no Bot.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}bug (description)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}bug (descrição)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "report a bug that occurred in the Bot.")
                self.lang_dict.add_with(["pt_br", "pt"], "reporte um bug que ocorreu no Bot.")
            return self._untangle_str(ctx, self._cname)

        # endregion

    Bug: Bug
