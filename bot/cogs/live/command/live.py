# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from yarl import URL

from bot.apis import ApiIvrFi
from bot.apis.ivrfi.parsers.user import UserElement
from bot.ext import Context, commands
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class LiveCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.ApiIvrFi = ApiIvrFi(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("Live")
    @commands.command(name="live", aliases=["title"])
    async def live(self, ctx: Context, channel: str = "") -> Response:
        if not channel.isdigit():
            channel = ctx.bot.StringTools.str2name_or(channel or ctx.channel.name)
            user_tmi = await self.ApiIvrFi.User.fetch_user(name=channel)
        else:
            user_tmi = await self.ApiIvrFi.User.fetch_user(user_id=int(channel) or ctx.channel.id)
        if not user_tmi:
            return ctx.user.translations.Exceptions.user_not_found_name.format_response(ctx, channel, success=False)
        return await format_response(ctx, user_tmi)


async def format_response(ctx: Context, user_tmi: UserElement) -> Response:
    translations = ctx.user.translations.Live
    stream = user_tmi.stream or user_tmi.last_broadcast
    humanize = ctx.user.translations.SupportTools.TimeTools.Humanize
    title = translations.title.format(stream.title)
    twitch_url = URL("https://www.twitch.tv/")
    if not hasattr(stream, "id"):
        last_stream_natural = humanize.naturaltime(user_tmi.last_broadcast.started_at)
        last_stream_precise = humanize.precisedelta(user_tmi.last_broadcast.started_at)
        broadcast_time = translations.last_stream.format(last_stream_natural, last_stream_precise)
        stream2 = (await ctx.bot.fetch_videos(user_id=user_tmi.id))[0]
        vod_url = twitch_url / "videos" / stream2.id
    else:
        stream_started = user_tmi.stream.created_at
        current_stream_natural = humanize.naturaltime(stream_started)
        current_stream_precise = humanize.precisedelta(stream_started)
        broadcast_time = translations.stream_started.format(current_stream_natural, current_stream_precise)
        stream2 = (await ctx.bot.fetch_videos(user_id=user_tmi.id))[0]
        now_adjusted = datetime.datetime.now(datetime.UTC).replace(tzinfo=None) - datetime.timedelta(seconds=90)
        vod_offset = (now_adjusted - stream_started).total_seconds()
        vod_offset = max(0, int(vod_offset))
        vod_url = (twitch_url / "videos" / stream2.id).update_query(t=f"{vod_offset}s")

    channel_link = twitch_url / user_tmi.display_name
    if ctx.invoke_by == "title":
        response = f"{title} || {broadcast_time} {channel_link}"
        return translations.response.format_response(ctx, response)

    views = translations.views.format(stream.viewers_count) if hasattr(stream, "viewers_count") else ""
    game = translations.playing.format(stream.game.display_name) if hasattr(stream, "game") else ""
    response = " || ".join(part for part in [title, broadcast_time, views, game, f"{channel_link} {vod_url}"] if part)
    return translations.response.format_response(ctx, response)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(LiveCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
