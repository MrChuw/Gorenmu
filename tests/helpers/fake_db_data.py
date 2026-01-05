from __future__ import annotations

import datetime
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

    for num in range(51):
        ctx = MockContext(f"some_user_{num + 1}", num + 1, "channelname", 123456, bot)  # NOQA
        await User.create_or_update(ctx)

    for num in range(45, 51):
        user = await ctx.bot.memcache.User.get(user_id=num)
        channel = await channel.create(user=user)
        ctx.bot.channels[user.name] = channel

    ctx = MockContext("no_mention_user", 1234512341234, "channelname", 123456, bot)
    ctx.bot.channels["channelname"] = channel
    user = await User.create_or_update(ctx)
    user.saved_color = "FF4500"
    user.mention = False
    await user.save()

    ctx = MockContext("status_user_50", 12344321, "channelname", 123456, bot)  # NOQA
    await User.create_or_update(ctx)


async def create_cookie_db(bot: Gorenmu):
    channel_user = await User.create_or_none(user_id=123456, name="channelname")
    channel = await Channel.create(user=channel_user)
    ctx = MockContext("username", 12345, "channelname", 123456, bot)

    for num in range(40, 46):
        user = await ctx.bot.memcache.User.get(user_id=num)
        cookie = await Cookies.create(user=user)
        cookie.received = 54 * num
        cookie.consumed = 73 * num
        cookie.donated = 56 * num
        cookie.stocked = 93 * num
        await cookie.save()
        await cookie.new_cooldown()

    ctx = MockContext("no_mention_user", 1234512341234, "channelname", 123456, bot)
    ctx.bot.channels["channelname"] = channel
    user = await User.create_or_update(ctx)
    user.saved_color = "FF4500"
    user.mention = False
    await user.save()

    for num in range(40, 46):
        user = await ctx.bot.memcache.User.get(user_id=num)
        cookie = await Cookies.create(user=user)
        cookie.received = 54 * num
        cookie.consumed = 73 * num
        cookie.donated = 56 * num
        cookie.stocked = 93 * num
        await cookie.save()
        await cookie.new_cooldown()


async def create_afk_data(bot: Gorenmu):
    ctx = MockContext("status_user_50", 12344321, "channelname", 123456, bot)  # NOQA
    user1 = await User.create_or_update(ctx)
    ctx.user = user1

    translations = Translations(None)  # NOQA
    translations.AFK.afks(None)
    afks = translations.AFK._get_afks()  # NOQA
    await Status.go_afk(ctx=ctx, status=afks.get("afk"), content="")

    ctx = MockContext("status_user_51", 123443210, "channelname", 123456, bot)  # NOQA
    user2 = await User.create_or_update(ctx)
    ctx.user = user2
    await Status.go_afk(ctx=ctx, status=afks.get("afk"), content="content")

    afk_user1 = await Status.get_afk(ctx, user=user1)
    afk_user2 = await Status.get_afk(ctx, user=user2)

    afk_user1.updated_at = datetime.datetime(2025, 8, 7, 17, 5, 55, tzinfo=datetime.UTC)
    afk_user2.updated_at = datetime.datetime(2025, 8, 7, 17, 5, 55, tzinfo=datetime.UTC)

    await afk_user1.save()
    await afk_user2.save()

    # for num, item in enumerate(afks):
    #     ctx = MockContext(f"status_user_{(num + 1) * 64}", (num + 1) * 64, "channelname", 123456, bot)  # NOQA
    #     user = await User.create_or_update(ctx)
    #     afk = afks.get(item)
    #     ctx.user = user
    #     await Status.go_afk(ctx=ctx, status=afk, content="")
    #
    #     ctx = MockContext(f"status_user_{(num + 1) * 46}", (num + 1) * 46, "channelname", 123456, bot)  # NOQA
    #     user = await User.create_or_update(ctx)
    #     ctx.user = user
    #     await Status.go_afk(ctx=ctx, status=afk, content="content")
    # yield
