from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from quickjs import Context as JSContext

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu

mathjs_path = Path(__file__).parent / "../../../apis/js_apis/math.js"
with open(mathjs_path, encoding="utf-8") as f:
    MATHJS_SOURCE = f.read()

js_context = JSContext()
js_context.eval(MATHJS_SOURCE)


class MathCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.UploadThings: UploadThings = UploadThings(bot)

    cooldown_rate = 5
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    @commands.command(name="math", aliases=["mathjs"])
    async def math(self, ctx: Context, *, args: str) -> Response:
        if "math." in args or "mathjs." in args:
            return self.translations.Math.not_supported(ctx)

        try:
            code = f"math.format(math.evaluate({args!r}))"
            response = js_context.eval(code)
            res_str = str(response)
            if not res_str or "function" in res_str:
                return self.translations.Exceptions.echo(ctx, r"¯\_(ツ)_/¯")
            if len(res_str) >= 500:
                link = await self.UploadThings.pastebin_upload(res_str, self.SessionsCaches.Math.session)
                response = f"{res_str[:450]} {link}" if link else res_str[:450]
                return self.translations.Exceptions.echo(ctx, response)

            return self.translations.Exceptions.echo(ctx, res_str)

        except Exception as e:
            await self.bot.CommandHandler.send_bug(ctx, e, ping=False)
            return self.translations.Exceptions.error(ctx)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(MathCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
