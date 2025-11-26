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

    class Preview(TBase):
        def __init__(self):
            super().__init__()

        def not_live(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Channel {} is not live at the moment.")
                self.lang_dict.add_with(["pt_br", "pt"], "O canal {} não esta em live no momento.")
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def preview(self, ctx: Context, preview, vod) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "Preview: {} || VOD: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), preview, vod)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command will send a print and timestamp of the requested live stream.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando enviara um print e timestamp da live pedida.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{}preview (channel_name)")
                self.lang_dict.add_with(["pt_br", "pt"], "{}preview (nome_do_canal)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command uses a service that isn't always reliable to create a live clip/preview. "
                    "If the command fails, try again in a few seconds.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando usa um serviço que nem sempre é estável para criar um clip/preview da live. "
                    "Caso o comando der erro, tente novamente em alguns segundos.",
                )
            return self._untangle_str(ctx, self._cname)

        # endregion

    Preview: Preview
