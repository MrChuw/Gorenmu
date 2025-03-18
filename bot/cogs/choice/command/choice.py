# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING
import random
import re

from bot.ext import commands, Context
from bot.translations import BaseDecorators, Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu

__all__ = (
        'ChoiceCmd'
)


class ChoiceCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None:
        ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:
        return True

    @commands.base_decorator(BaseDecorators.Choice)
    @commands.command(name='choice', aliases=['pick'])
    async def choice(self, ctx: Context, *, content: str) -> Response:
        pattern = '|'.join(map(re.escape, ctx.user.translations.Choice.choice_separators))
        choice = random.choice([arg for arg in re.split(pattern, content) if arg])
        return ctx.user.translations.Choice.chosen_option.format_response(ctx, choice)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ChoiceCmd(bot))


async def teardown(bot: Gorenmu) -> None:
    ...
