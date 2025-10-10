# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from collections import defaultdict
from typing import TYPE_CHECKING

from bot.apis import Color
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools, TimeTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class RandomColorCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.command(name="randomcolor", aliases=["rc"])
    async def randomcolor(self, ctx: Context, tipo: str = None) -> Response:
        translations = self.translations.RandomColor
        session = self.SessionsCaches.Color.session
        url = ctx.bot.config.ApisConfig.color_site_url
        params = defaultdict()
        hex_code = None
        if tipo == "type:hex" or not tipo:
            hex_code = "%06x" % random.randint(0, 0xFFFFFF)
            params["hex"] = str(hex_code)
            url = url.with_path(f"/hex/{hex_code}")
            hex_code = f"#{hex_code.upper()}"
        elif tipo == "type:rgb":
            rgb = tuple(random.randint(0, 255) for _ in range(3))
            params["rgb"] = str(rgb)
            url = url.with_path("/rgb/{},{},{}".format(*rgb))
            hex_code = "#{:02X}{:02X}{:02X}".format(*rgb)
        name = await Color.name(params, session, self.bot.log) or translations.api_down(ctx)
        return translations.response_url(ctx, hex_code, name, url)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(RandomColorCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
