from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from yarl import URL

from bot.apis import ApiIvrFi
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class LiveCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.ApiIvrFi = ApiIvrFi(bot, self.SessionsCaches.IvrFi.session)
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="live", aliases=["title"])
    async def live(self, ctx: Context, channel: str = "") -> Response:
        if not channel.isdigit():
            channel = self.StringTools.str2name_or(channel or ctx.channel.name)
            user_tmi = await self.ApiIvrFi.Twitch.User.fetch_user(name=channel)
        else:
            user_tmi = await self.ApiIvrFi.Twitch.User.fetch_user(user_id=int(channel) or ctx.channel.id)
        if not user_tmi:
            return self.translations.Exceptions.user_not_found_name(channel)

        translations = self.translations.Live
        stream = user_tmi.stream or user_tmi.last_broadcast
        humanize = self.translations.SupportTools.TimeTools.Humanize(ctx.user.language)
        title = translations.title(stream.title)
        twitch_url = URL("https://www.twitch.tv/")
        if not hasattr(stream, "id") and not stream.started_at:
            return self.translations.Live.never_streamed(name=channel)
        elif not hasattr(stream, "id"):
            last_stream_natural = humanize.naturaltime(user_tmi.last_broadcast.started_at)
            last_stream_precise = humanize.precisedelta(user_tmi.last_broadcast.started_at)
            broadcast_time = translations.last_stream(last_stream_natural, last_stream_precise)
            if stream2 := await ctx.bot.fetch_videos(user_id=user_tmi.id):
                stream2 = stream2[0]
                vod_url = twitch_url / "videos" / stream2.id
            else:
                vod_url = ""
        else:
            stream_started = user_tmi.stream.created_at
            current_stream_natural = humanize.naturaltime(stream_started)
            current_stream_precise = humanize.precisedelta(stream_started)
            broadcast_time = translations.stream_started(current_stream_natural, current_stream_precise)
            stream2 = (await ctx.bot.fetch_videos(user_id=user_tmi.id))[0]
            now_adjusted = datetime.datetime.now().replace(tzinfo=None) - datetime.timedelta(seconds=90)
            vod_offset = (now_adjusted - stream_started).total_seconds()
            vod_offset = max(0, int(vod_offset))
            vod_url = (twitch_url / "videos" / stream2.id).update_query(t=f"{vod_offset}s")

        channel_link = twitch_url / user_tmi.display_name
        if ctx.invoke_by == "title":
            response = f"{title} || {broadcast_time} {channel_link}"
            return translations.response(response)

        views = translations.views(stream.viewers_count) if hasattr(stream, "viewers_count") else ""
        game = translations.playing(stream.game.display_name) if hasattr(stream, "game") else ""
        response = " || ".join(
            part
            for part in [
                title,
                broadcast_time,
                views,
                game,
                f"{channel_link} {vod_url}",
            ]
            if part
        )
        return translations.response(response)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(LiveCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
