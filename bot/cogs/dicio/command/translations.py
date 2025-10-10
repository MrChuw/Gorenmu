# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Dicio(TBase):
        def __init__(self):
            super().__init__()

        def response(self, ctx: Context, word, exist, similar, origin, url) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "The word {} {} || Similar: {} || Origin: {} || Url: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "A palavra {} {} || Similares: {}  || Origem: {} || Url: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), word, exist, similar, origin, url)

        def all_languages(self, ctx: Context, languages) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "All available languages are: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Todos os idiomas disponíveis são: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), languages)

        def error(self, ctx: Context, link, dev) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Unexpected error, lang does not exist. Check {} to see available languages and ask @{} to add.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Erro inesperado, idioma não existe. "
                    "Verifique {} para ver os idiomas disponíveis e @{} para adicionar.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), link, dev)

        def exist(self, ctx: Context):
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "exist")
                self.lang_dict.add_with(["pt_br", "pt"], "existe")
            return self._untangle_str(ctx, self._cname)

        def url(self, lang, word):
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "https://en.wiktionary.org/wiki/{}")
                self.lang_dict.add_with(["pt_br", "pt"], "https://dicio.com.br/{}")
            if url := self.lang_dict.get_lang_or_none(lang, self._cname):
                return url.format(word)
            return None

        def not_exist(self, ctx: Context):
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "does not exist")
                self.lang_dict.add_with(["pt_br", "pt"], "não existe")
            return self._untangle_str(ctx, self._cname)

        def languages(self, lang) -> str:
            with self.lang_dict.once(self._cname):
                # English (en)
                self.lang_dict.add_with(["en_us", "en"], "en/en_US")
                self.lang_dict.add_with(["en_gb", "en_uk", "uk"], "en/en_GB")

                # Portuguese (pt)
                self.lang_dict.add_with(["pt_br", "pt"], "pt_BR/pt_BR")
                self.lang_dict.add_with("pt_pt", "pt_PT/pt_PT")

                # Spanish (es)
                self.lang_dict.add_with(["es_es", "es"], "es/es_ES")
                self.lang_dict.add_with("es_mx", "es_MX/es_MX")
                self.lang_dict.add_with("es_ar", "es_AR/es_AR")
                self.lang_dict.add_with("es_us", "es_US/es_US")

                # Others
                self.lang_dict.add_with(["de_de", "de"], "de_DE/de_DE_frami")  # NOQA
                self.lang_dict.add_with(["fr_fr", "fr"], "fr_FR/fr")
                self.lang_dict.add_with(["it_it", "it"], "it_IT/it_IT")
                self.lang_dict.add_with("ko_kr", "ko_KR/ko_KR")
                self.lang_dict.add_with("ru_ru", "ru_RU/ru_RU")
                self.lang_dict.add_with("ar", "ar/ar")
                self.lang_dict.add_with("hi_in", "hi_IN/hi_IN")
                self.lang_dict.add_with("nl_nl", "nl_NL/nl_NL")
                self.lang_dict.add_with("pl_pl", "pl_PL/pl_PL")
                self.lang_dict.add_with(["sv_se", "sv"], "sv_SE/sv_SE")
                self.lang_dict.add_with(["sv_fi", "fi"], "sv_SE/sv_FI")
                self.lang_dict.add_with("tr_tr", "tr_TR/tr_TR")
                self.lang_dict.add_with("th_th", "th_TH/th_TH")
                self.lang_dict.add_with("id_id", "id_ID/id_ID")
                self.lang_dict.add_with("vi_vn", "vi_VN/vi_VN")
                self.lang_dict.add_with("he_il", "he_IL/he_IL")
                self.lang_dict.add_with("el_gr", "el_GR/el_GR")
                self.lang_dict.add_with("uk_ua", "uk_UA/uk_UA")

            if lang == "languages":
                return ", ".join(self.lang_dict._namespaces["languages"].keys())  # NOQA

            return self.lang_dict.get_lang(lang, self._cname, "en")

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "")
                self.lang_dict.add_with(["pt_br", "pt"], "")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{}dicio (word) <lang:en>")
                self.lang_dict.add_with(["pt_br", "pt"], "{}dicio (palavra) <lang:pt_br>")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "")
                self.lang_dict.add_with(["pt_br", "pt"], "")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", CommandExemples([]))
                self.lang_dict.add_with(["pt_br", "pt"], CommandExemples([]))
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Dicio: Dicio
