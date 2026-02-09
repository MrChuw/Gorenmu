from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .imgur import ImgurCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: ImgurCmd) -> None:
        super().__init__(bot)
        self.parent: ImgurCmd = parent
        self.populate_subclasses(parent=self)

    class Imgur(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)

        def time(self, time) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Time: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Tempo: {}")
            return self._untangle_str(self.ctx_get(), self._cname).format(time)

        def all_images(self, embed_url) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "All generated images: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Todas as imagens geradas: {}")
            return self._untangle_str(self.ctx_get(), self._cname).format(embed_url)

        def all_images2(self, embed_url) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "|| All images: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "|| Todas as imagens: {}")
            return self._untangle_str(self.ctx_get(), self._cname).format(embed_url)

        def took_too_long(self, passed) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{}s has passed and I haven't been able to generate the image(s).")
                self.lang_dict.add_with(["pt_br", "pt"], "{}s se passaram e não consegui gerar a(s) imagem(ns)")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), passed)

        def links(self, responses) -> Response:
            return Response(ctx=self.ctx_get(), success=True, handle=None, response_list=responses)

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "Command used to generate random images from Imgur. NSFW command disabled by default."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Comando usado para gerar imagens aleatórias do Imgur. O comando NSFW está desativado por padrão.",
                )
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}imgur(7) (amount)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}imgur(7) (quantidade)")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "Command used to generate random images from Imgur. NSFW command disabled by default."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Comando usado para gerar imagens aleatórias do Imgur. O comando NSFW está desativado por padrão.",
                )
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Disabled by default.",
                                "message": "Because this command can generate NSFW images, it is disabled by default.",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Desativo por padrão.",
                                "message": "Porque esse comando pode gerar imagens NSFW ele é desativado por padrão.",
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(self.ctx_get(), self._cname)

        # endregion

    Imgur: Imgur
