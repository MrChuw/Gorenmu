# -*- coding: utf-8 -*-
from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

from bot.cogs.afk.commands.translations import Translations
from bot.models import Channel, Cookies, Status, User
from tests.helpers.mock_classes import MockContext

if TYPE_CHECKING:
    from bot.bot import Gorenmu


async def create_fake_db(bot: Gorenmu):
    channel_user = await User.create_or_none(user_id=123456, name="channelname")
    channel = await Channel.create(user=channel_user)
    ctx = MockContext("username", 12345, "channelname", 123456, bot)
    ctx.bot.channels["channelname"] = channel
    user = await User.create_or_update(ctx)
    user.saved_color = "FF4500"
    await user.save()

    for num in range(50):
        ctx = MockContext(f"some_user_{num+1}", num + 1, "channelname", 123456, bot)  # NOQA
        await User.create_or_update(ctx)

    for num in range(45, 51):
        user = await ctx.bot.memcache.User.get(user_id=num)
        channel = await Channel.create(user=user)
        ctx.bot.channels[user.name] = channel

    ctx = MockContext("status_user_50", 12344321, "channelname", 123456, bot)  # NOQA
    # ctx.user.get_translation(bot, "en")
    user = await User.create_or_update(ctx)
    translations = Translations(None)  # NOQA
    with contextlib.suppress():
        translations.AFK.afks(None)
    afks = translations.AFK._get_afks()  # NOQA
    ctx.user = user
    await Status.go_afk(ctx=ctx, status=afks.get("afk"), content="")

    ctx = MockContext("status_user_51", 123443210, "channelname", 123456, bot)  # NOQA
    user = await User.create_or_update(ctx)
    ctx.user = user
    await Status.go_afk(ctx=ctx, status=afks.get("afk"), content="content")

    for num, item in enumerate(afks):
        ctx = MockContext(f"status_user_{(num + 1) * 64}", (num + 1) * 64, "channelname", 123456, bot)  # NOQA
        user = await User.create_or_update(ctx)
        afk = afks.get(item)
        ctx.user = user
        await Status.go_afk(ctx=ctx, status=afk, content="")

        ctx = MockContext(f"status_user_{(num + 1) * 46}", (num + 1) * 46, "channelname", 123456, bot)  # NOQA
        user = await User.create_or_update(ctx)
        ctx.user = user
        await Status.go_afk(ctx=ctx, status=afk, content="content")

    for num in range(40, 46):
        user = await ctx.bot.memcache.User.get(user_id=num)
        cookie = await Cookies.create(user=user)
        cookie.received = 54 * num
        cookie.consumed = 73 * num
        cookie.donated = 56 * num
        cookie.stocked = 93 * num
        await cookie.save()
        await cookie.new_cooldown()
    ...
