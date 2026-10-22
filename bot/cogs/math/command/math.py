import re
from typing import TYPE_CHECKING

from bot.apis import FormatOptions, Mathjs
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class MathCmd(commands.CustomComponent):
    def __init__(self, bot: 'Gorenmu') -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.UploadThings: UploadThings = UploadThings(bot)
        self.StringTools: StringTools = StringTools()
        self.Mathjs: Mathjs = Mathjs()

    @commands.command(name="math", aliases=["mathjs"])
    async def math(self, ctx: Context, *, args: str) -> Response:
        if "math." in args or "mathjs." in args:
            return self.translations.Math.not_supported()
        text, local = self.StringTools.extract_and_remove_bool_field(args, "local", self.translations)

        try:
            if local or self.bot.mock:
                result = self.Mathjs.evaluate(text)
                return await self._format_math_result(result)
            else:
                request = await self.SessionsCaches.Math.session.get(
                        "https://api.mathjs.org/v4/",
                        params={
                                "expr": text
                        }
                )
                result = parse_math_result(await request.text())

            return await self._format_math_result(result)
        except Exception as e:
            return await self._handle_math_error(ctx=ctx, exception=e)

    async def _format_math_result(self, result):
        res_str = self.Mathjs.format(result, FormatOptions(truncate_matrix=True))

        if len(res_str) >= 500 and not self.bot.mock:
            link = await self.UploadThings.pastebin_upload(
                self.Mathjs.format(result, FormatOptions(truncate_matrix=False, pretty=True)),
                self.SessionsCaches.Math.session,
            )
            response = f"{res_str[:450]} {link}" if link else res_str[:450]
            return self.translations.Exceptions.echo(response)

        return self.translations.Exceptions.echo(res_str)

    async def _handle_math_error(self, ctx: Context, exception: Exception) -> Response:
        if isinstance(exception, NameError):
            return self.translations.Math.undefined_symbol(exception.args[1])

        if isinstance(exception, TimeoutError):  # ERR_TIMEOUT
            return self.translations.Math.evaluation_timeout(exception.args[1])

        if isinstance(exception, RecursionError):  # ERR_RECURSION
            return self.translations.Math.expression_too_complex(exception.args[1])

        if isinstance(exception, OverflowError):  # ERR_OVERFLOW
            return self.translations.Math.result_too_large(exception.args[0])

        if isinstance(exception, NotImplementedError):  # ERR_NOT_IMPLEMENTED
            return self.translations.Math.operation_not_supported(exception.args[0])

        if isinstance(exception, ValueError) and len(exception.args) >= 2:
            code = exception.args[-1]
            if isinstance(code, str) and code.startswith("ERR_"):
                method_map = {
                    "ERR_VALUE": "invalid_value",
                    "ERR_MATRIX": "matrix_error",
                    "ERR_DIMENSION": "incompatible_units",
                    "ERR_UNIT": "unknown_unit",
                    "ERR_POLY": "polynomial_error",
                    "ERR_INDEX": "index_out_of_range",
                }

                if method_name := method_map.get(code):
                    handler = getattr(self.translations.Math, method_name)
                    msg = exception.args[0]

                    return handler(msg)

            return self.translations.Math.value_error(str(exception))  # Fallback for any other ValueError

        if isinstance(exception, MemoryError):  # Memory limit exceeded
            return self.translations.Math.memory_limit_exceeded()

        await self.bot.CommandHandler.send_bug(ctx, exception, ping=False)
        return self.translations.Exceptions.error()


async def setup(bot: 'Gorenmu') -> None:
    await bot.add_component(MathCmd(bot))


async def teardown(bot: 'Gorenmu') -> None:  # noqa
    pass


def parse_math_result(val: str):
    if re.search(r'[eEi]', val):
        return val

    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val
