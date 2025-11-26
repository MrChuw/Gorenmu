from __future__ import annotations

import re
from typing import TYPE_CHECKING

from bot.apis import Color
from bot.ext import Context, Response, commands
from bot.models import User
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ColorCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.color_cache: SessionsCaches.Color = SessionsCaches(bot).Color
        self.StringTools: StringTools = StringTools()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="color", aliases=["colour"])
    async def color(self, ctx: Context, name: str) -> Response:
        translations = self.translations.Color
        color_url = ctx.bot.config.ApisConfig.color_site_url
        tmi_color = None
        user = None
        urls = []
        responses = []
        name = self.StringTools.str2name_or(name)

        async def get_color_info(hex_code: str, response_template: str):
            params = {"hex": hex_code}
            hex_name = await Color.name(params=params, session=self.color_cache.session, log=ctx.bot.log)
            url_preview = color_url.with_path(f"/hex/{hex_code.upper()}").human_repr()
            response = response_template.format(hex_code.upper(), hex_name)
            urls.append(url_preview)
            responses.append(response)

        if "#" not in name and (user := await ctx.bot.fetch_user(login=name)):  # NOQA: SIM102
            if tmi_color := (await ctx.bot.fetch_chatters_color([user.id]))[0].color:  # NOQA: SIM102
                await get_color_info(
                    tmi_color.hex_clean,
                    translations.user_color(ctx).replace("{}", name, 1),
                )

        if color_hex := re.match(r"^#?[0-9a-fA-F]{6}$", name):
            color_hex = color_hex[0].replace("#", "")
            await get_color_info(color_hex, translations.hex_color(ctx))

        if user:
            user_db = await User.get_user(ctx, translations=self.translations, user_id=user.id, is_none=True)
            if user_db and user_db.saved_color:
                await get_color_info(user_db.saved_color, translations.saved_color(ctx))

        if not tmi_color and not color_hex:
            if not user:
                return translations.no_user_hex(ctx)
            return translations.user_not_color(ctx)

        url_previews = list(dict.fromkeys(urls))
        return translations.color(ctx, " || ".join(responses), " || ".join(url_previews))


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ColorCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
