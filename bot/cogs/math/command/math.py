from __future__ import annotations

from typing import TYPE_CHECKING

from javascript import require

from bot.ext import Context, Response, commands

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu

mathjs = require("../../../apis/js_apis/math.js")


class MathCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)

    cooldown_rate = 5
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="math", aliases=["mathjs"])
    async def math(self, ctx: Context, *, args: str) -> Response:
        if "math." in args or "mathjs." in args:
            return self.translations.Math.not_supported(ctx)
        try:
            response = mathjs.format(mathjs.evaluate(args))
            if type(response) in [int, float]:
                return self.translations.Exceptions.echo(ctx, response)
            if type(response) in [str]:
                if len(response) >= 500:
                    return self.translations.Exceptions.echo(ctx, response[:450])
                return self.translations.Exceptions.echo(ctx, response)
            elif not response or "function" in response.toString():
                return self.translations.Exceptions.echo(ctx, r"¯\_(ツ)_/¯")
            else:
                if len(response.toString()) >= 500:
                    return self.translations.Exceptions.echo(ctx, response.toString()[:450])
                return self.translations.Exceptions.echo(ctx, response.toString())
        except Exception as e:
            await self.bot.CommandHandler.send_bug(ctx, e, ping=False)
            return self.translations.Math.error(ctx)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(MathCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
