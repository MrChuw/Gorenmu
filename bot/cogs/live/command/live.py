from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from yarl import URL

from bot.apis import ApiIvrFi
from bot.apis.ivrfi.parsers.user import LastBroadcast, Stream
from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Live, Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class LiveCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.ApiIvrFi = ApiIvrFi(bot, self.SessionsCaches.IvrFi.session)
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()

    @commands.command(name="live", aliases=["title"])
    async def live(self, ctx: Context, channel: str = "") -> Response:
        if not channel.isdigit():
            channel = self.StringTools.str2name_or(channel or ctx.channel_name)
            user_tmi = await self.ApiIvrFi.Twitch.User.fetch_user(name=channel)
        else:
            user_tmi = await self.ApiIvrFi.Twitch.User.fetch_user(user_id=int(channel or ctx.channel.id))

        if not user_tmi:
            return self.translations.Exceptions.user_not_found_name(channel)

        translations = self.translations.Live
        stream = user_tmi.stream or user_tmi.last_broadcast

        if not stream:
            return translations.never_streamed(name=channel)
        if isinstance(stream, Stream) and stream.id is None:
            return translations.never_streamed(name=channel)
        if isinstance(stream, LastBroadcast) and stream.started_at is None:
            return translations.never_streamed(name=channel)

        humanize = self.translations.SupportTools.TimeTools.Humanize()
        title = translations.title(stream.title) if stream.title else ""
        twitch_url = URL("https://www.twitch.tv/")

        game, views = "", ""
        is_offline = isinstance(stream, LastBroadcast)
        handler = self._handle_last_broadcast if is_offline else self._handle_live_stream
        broadcast_time, vod_url = await handler(ctx, str(user_tmi.id), stream, humanize, translations, twitch_url)

        if not is_offline:
            if getattr(stream, "viewers_count", None):
                views = translations.views(stream.viewers_count)

            game_name = stream.game.display_name if getattr(stream, "game", None) else ""
            if game_name:
                game = translations.playing(game_name)

        channel_link = twitch_url / (user_tmi.display_name or user_tmi.login or "")

        if ctx.invoke_by == "title":
            response = f"{title} || {broadcast_time} {channel_link}"
            return translations.response(response)

        response = " || ".join(
            part
            for part in [
                title,
                broadcast_time,
                views,
                game,
                f"{channel_link} {vod_url}".strip(),
            ]
            if part
        )
        return translations.response(response)

    @staticmethod
    async def _handle_last_broadcast(
        ctx: Context, user_id: str, stream, humanize, translations: Live, twitch_url
    ) -> tuple[str, str]:
        last_stream_natural = humanize.naturaltime(stream.started_at)
        last_stream_precise = humanize.precisedelta(stream.started_at)
        broadcast_time = translations.last_stream(last_stream_natural, last_stream_precise)

        vod_url = ""
        if stream2 := await ctx.bot.fetch_videos(user_id=user_id):
            vod_url = twitch_url / "videos" / stream2[0].id

        return broadcast_time, vod_url

    @staticmethod
    async def _handle_live_stream(
        ctx: Context, user_id: str, stream, humanize, translations: Live, twitch_url
    ) -> tuple[str, str]:
        stream_started = stream.created_at
        current_stream_natural = humanize.naturaltime(stream_started)
        current_stream_precise = humanize.precisedelta(stream_started)
        broadcast_time = translations.stream_started(current_stream_natural, current_stream_precise)

        vod_url = ""
        if stream2 := await ctx.bot.fetch_videos(user_id=user_id):
            now_adjusted = datetime.datetime.now().replace(tzinfo=None) - datetime.timedelta(seconds=90)
            vod_offset = max(0, int((now_adjusted - stream_started).total_seconds()))
            vod_url = (twitch_url / "videos" / stream2[0].id).update_query(t=f"{vod_offset}s")

        return broadcast_time, vod_url


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(LiveCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
