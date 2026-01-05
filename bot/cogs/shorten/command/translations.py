from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses(parent=self)

    class Shorten(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)

        def api_erro(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "The shortener API is currently experiencing issues.")
                self.lang_dict.add_with(["pt_br", "pt"], "A API do encurtador apresentando problemas no momento.")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        def urls(self, urls) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Here are all the URLs: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Aqui estão todos os URLs: {}")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), urls)

        def url(self, url) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Here is the URL: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Aqui está URL: {}")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), url)

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Shorten links using my link shortening service.")
                self.lang_dict.add_with(["pt_br", "pt"], "Encurta links usando o meu serviço de encurtar links.")
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}shorten (links)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}shorten (links)")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Shorten links using my link shortening service.")
                self.lang_dict.add_with(["pt_br", "pt"], "Encurta links usando o meu serviço de encurtar links.")
            return self._untangle_str(self.ctx_get(), self._cname)

    Shorten: Shorten
