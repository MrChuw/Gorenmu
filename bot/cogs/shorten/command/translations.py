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

    class Shorten(TBase):
        def __init__(self):
            super().__init__()

        def api_erro(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "The shortener API is currently experiencing issues.")
                self.lang_dict.add_with(["pt_br", "pt"], "A API do encurtador apresentando problemas no momento.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def urls(self, ctx: Context, urls) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Here are all the URLs: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Aqui estão todos os URLs: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), urls)

        def url(self, ctx: Context, url) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Here is the URL: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Aqui está URL: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), url)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Shorten links using my link shortening service.")
                self.lang_dict.add_with(["pt_br", "pt"], "Encurta links usando o meu serviço de encurtar links.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}shorten (links)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}shorten (links)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Shorten links using my link shortening service.")
                self.lang_dict.add_with(["pt_br", "pt"], "Encurta links usando o meu serviço de encurtar links.")
            return self._untangle_str(ctx, self._cname)

    Shorten: Shorten
