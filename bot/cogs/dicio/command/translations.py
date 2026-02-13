from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .dicio import DicioCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: DicioCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: DicioCmd = parent
        self.populate_subclasses(parent=self)

    class Dicio(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Dicio"

        def response(self, word, exist, similar, origin, url) -> Response:
            text = self.get_text(self._cname, word=word, exist=exist, similar=similar, origin=origin, url=url)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def check_exist(self, exist) -> str:
            text = self.get_text(self._cname, exist=exist)
            return text

        def all_languages(self, languages) -> Response:
            text = self.get_text(self._cname, languages=languages)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def error(self, link, dev) -> Response:
            text = self.get_text(self._cname, link=link, dev=dev)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def url(self, lang, word):
            return self.get_text_by_lang(lang, self._cname, word=word)

        def languages(self, lang) -> str:
            langs = self.get_attributes(self._cname)
            if lang == "languages":
                return ", ".join(self.lang_dict._namespaces["languages"].keys())  # NOQA

            return langs.get(lang, "en/en_US")

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Dicio: Dicio
