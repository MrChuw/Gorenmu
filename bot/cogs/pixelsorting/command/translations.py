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

    class PixelSorting(TBase):
        def __init__(self):
            super().__init__()

        def no_url(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "No valid URL provided.")
                self.lang_dict.add_with(["pt_br", "pt"], "Nenhuma URL válida fornecida.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def invalid_content_type(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "Only real image files (like .jpg, .png) are accepted, no previews or unsupported links."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Somente arquivos de imagem reais (como .jpg, .png) são aceitos, sem pré-visualizações ou "
                    "links não suportados.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname))

        def took_too_long(self, ctx: Context, time) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "{} seconds have passed and the process has not finished. Try a smaller image or less types."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "{} segundos se passaram e o processo não foi concluído. Tente uma imagem menor ou menos tipos.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), time)

        def image(self, ctx: Context, shortened) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), shortened)

        def placeholder2(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "")
                self.lang_dict.add_with(["pt_br", "pt"], "")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Command used to make basic pixel sorting in images.")
                self.lang_dict.add_with(["pt_br", "pt"], "Comando usado para aplicar pixel sorting básico em imagens.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}pxs (url or shortened direct link) ")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}pxs (url ou link direto encurtado)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command processes an image using pixel sorting algorithms. "
                    "You can specify the color mode, intensity, direction, crop tiles, randomization, "
                    "and masking options.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando processa uma imagem utilizando algoritmos de pixel sorting. "
                    "Você pode especificar o modo de cor, intensidade, direção, recorte por blocos, "
                    "aleatoriedade e opções de máscara.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "An image URL with no default arguments.",
                                "args": "(image url)",
                                "response": "(link for the image.)",
                                "suffix": "",
                            },
                            {
                                "prefix": "An image URL with with arguments.",
                                "args": "type:red crop:100px:100px maskmode:internal dire:horizontal",
                                "response": "(link for the image.)",
                                "suffix": "",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "Uma URL de imagem sem argumentos.",
                                "args": "(url da imagem)",
                                "response": "(link da imagem gerada.)",
                                "suffix": "",
                            },
                            {
                                "prefix": "Uma URL de imagem com argumentos.",
                                "args": "type:red crop:100px:100px maskmode:internal dire:horizontal",
                                "response": "(link da imagem gerada.)",
                                "suffix": "",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    Admonitions(
                        [
                            {
                                "admonition_type": "info",
                                "position": "top",
                                "title": "Multiple Sorting Modes",
                                "message": "You can use modes like red, green, blue, sum, rgb, hue, "
                                "saturation, value, luma, and more.",
                            },
                            {
                                "admonition_type": "info",
                                "position": "middle",
                                "title": "Masking Options",
                                "message": "You can control which pixels are affected using "
                                "[maskmode:internal|external] and [maskthreshold:128].",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "Random Segments",
                                "message": "Set [rand:true] to introduce randomness into which segments are sorted.",
                            },
                            {
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Max Resolution",
                                "message": "Images larger than 1920x1080 will be resized automatically.",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "info",
                                "position": "top",
                                "title": "Múltiplos modos de ordenação",
                                "message": "Você pode usar modos como red, green, blue, sum, rgb, hue, saturation, "
                                "value, luma e outros.",
                            },
                            {
                                "admonition_type": "info",
                                "position": "middle",
                                "title": "Opções de máscara",
                                "message": "Você pode controlar quais pixels serão afetados usando "
                                "[maskmode:internal|external] e [maskthreshold:128].",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "Segmentos aleatórios",
                                "message": "Defina [rand:true] para introduzir aleatoriedade nos "
                                "segmentos que serão ordenados.",
                            },
                            {
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Resolução máxima",
                                "message": "Imagens maiores que 1920x1080 serão redimensionadas automaticamente.",
                            },
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    PixelSorting: PixelSorting
