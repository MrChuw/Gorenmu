from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .dicio import DicioCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: DicioCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.Dicio: Dicio = Dicio(self)


class Dicio(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Dicio"
        super().__init__(parent, __file__)

    def response(self, word, exist, similar, origin, url) -> Response:
        text = self.get_text(self._cname, word=word, exist=exist, similar=similar, origin=origin, url=url)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def check_exist(self, exist) -> str:
        return self.get_text(self._cname, exist=exist)

    def all_languages(self, languages) -> Response:
        text = self.get_text(self._cname, languages=languages)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def error(self, link, dev) -> Response:
        text = self.get_text(self._cname, link=link, dev=dev)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def url(self, lang, word):
        return self.get_text_by_lang(lang, self._cname, word=word)

    # TODO: test new method
    # def languages(self, lang) -> str:
    #     langs = self.get_attributes(self._cname)
    #     if lang == "languages":
    #         return ", ".join(self.lang_dict._namespaces["languages"].keys())  # NOQA
    #     return langs.get(lang, "en/en_US")

    def languages(self, lang) -> str:
        langs = self.get_attributes(self._cname)
        if lang == "languages":
            return ", ".join(self.lang_dict.get_languages())
        return langs.get(lang, "en/en_US")

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)
