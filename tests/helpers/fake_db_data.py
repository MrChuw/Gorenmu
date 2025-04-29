# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from tests.helpers.mock_classes import MockContext
from bot.models import User
from bot.models import Channel
from bot.models import Status


if TYPE_CHECKING:
    from bot.bot import Gorenmu



async def create_fake_db(bot: Gorenmu):
    channel_user = await User.create_or_none(id=123456, name="channelname")
    channel = await Channel.create(user=channel_user)
    ctx = MockContext("username", 12345, "channelname", 123456, bot)
    ctx.bot.channels["channelname"] = channel
    await User.create_or_update(ctx)

    for num in range(50):
        ctx = MockContext(f"some_user_{num+1}", num + 1, "channelname", 123456, bot)  # NOQA
        await User.create_or_update(ctx)

    for num in range(45, 51):
        user = await ctx.bot.memcache.get(key=num, namespace="user")
        channel = await Channel.create(user=user)
        ctx.bot.channels[user.name] = channel

    ctx = MockContext("status_user_50", 12344321, "channelname", 123456, bot)  # NOQA
    ctx.user.get_translation(bot, 'en')
    user = await User.create_or_update(ctx)
    afk = ctx.user.translations.Afk.afks.get("afk")  # NOQA
    ctx.user = user
    await Status.go_afk(ctx=ctx, status=afk, content="")

    ctx = MockContext("status_user_51", 123443210, "channelname", 123456, bot)  # NOQA
    ctx.user.get_translation(bot, 'en')  # NOQA
    user = await User.create_or_update(ctx)
    afk = ctx.user.translations.Afk.afks.get("afk")  # NOQA
    ctx.user = user
    await Status.go_afk(ctx=ctx, status=afk, content="content")

    for num, item in enumerate(ctx.user.translations.Afk.afks):
        ctx = MockContext(f"status_user_{(num + 1) * 64}", (num + 1) * 64, "channelname", 123456, bot)  # NOQA
        ctx.user.get_translation(bot, 'en')  # NOQA
        user = await User.create_or_update(ctx)
        afk = ctx.user.translations.Afk.afks.get(item)  # NOQA
        ctx.user = user
        await Status.go_afk(ctx=ctx, status=afk, content="")

        ctx = MockContext(f"status_user_{(num + 1) * 46}", (num + 1) * 46, "channelname", 123456, bot)  # NOQA
        ctx.user.get_translation(bot, 'en')  # NOQA
        user = await User.create_or_update(ctx)
        ctx.user = user
        await Status.go_afk(ctx=ctx, status=afk, content="content")


    ...













































