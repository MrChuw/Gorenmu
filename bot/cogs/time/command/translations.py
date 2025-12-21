from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase
from bot.utils.timelength import English, Guess, Locale, Portuguese, Spanish

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Time(TBase):
        def __init__(self):
            super().__init__()

        def only_latin(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Please use only Latin characters.")
                self.lang_dict.add_with(["pt_br", "pt"], "Por favor, utilize apenas caracteres Latin.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def overflow(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    f"Number/date too large to convert, if you think this is wrong, please contact: {ctx.bot.dev_name}",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Número/data muito grande para converter. "
                    f"Se você acha que isso está errado, entre em contato com: {ctx.bot.dev_name}",
                )
            return response.format_response(self._untangle_str(ctx, self._cname))

        def past(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{} ago")
                self.lang_dict.add_with(["pt_br", "pt"], "há {}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def present(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{}")
                self.lang_dict.add_with(["pt_br", "pt"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def future(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "in {}")
                self.lang_dict.add_with(["pt_br", "pt"], "em {}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def get_lang(self, ctx: Context, lang: str | bool = "", guess: bool = False) -> type[Locale] | type[Guess]:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", English)
                self.lang_dict.add_with(["pt_br", "pt"], Portuguese)
                self.lang_dict.add_with(["es"], Spanish)
            if lang:
                return self.lang_dict.get_lang_any(lang, self._cname, "en")
            else:
                return Guess if guess else self._untangle_any(ctx, self._cname)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "Converts units of time into other units, for example: Days to Hours, Seconds to Days, etc."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Converte unidades de tempo em outras unidades, exemplo: Dias em Horas, Segundos em Dias, etc.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "To use: {}time (final unit: seconds) (format to be transformed, e.g., 50h)"
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Para usar: {}time (unidade final: segundos) (formato a ser transformado, ex: 50h)"
                )
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Converts units of time into other units, for example: Days to Hours, Seconds to Days, etc. "
                    "Able to convert data and future/past.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Converte unidades de tempo em outras unidades, exemplo: Dias em Horas, Segundos em Dias, etc. "
                    "Podendo Converter datas e futuro/passado.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "h 100_000_000s", "response": "27777.78 hours"},
                            {
                                "args": "h 100_000_000s",
                                "response": "3 years, 2 months, 1 day, 9 hours, 46 minutes and 40 seconds",
                            },
                            {
                                "args": "time 25/12/2025 at 12:00:00",
                                "response": "in 8 days, 17 hours, 21 minutes and 28.9231 seconds",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"args": "h 100_000_000s", "response": "27777.78 horas"},
                            {
                                "args": "h 100_000_000s",
                                "response": "3 anos, 2 meses, 1 dia, 9 horas, 46 minutos e 40 segundos",
                            },
                            {
                                "args": "time 25/12/2025 at 12:00:00",
                                "response": "em 8 dias, 17 horas, 21 minutos e 28,9231 segundos.",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Time: Time
