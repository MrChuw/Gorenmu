from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import aiohttp

from bot.apis.discord_webhook.discord_webhook import DiscordEmbed, DiscordWebhook

if TYPE_CHECKING:
    from aiohttp_client_cache import CachedSession

    from bot.ext import Context


class DiscordWebHook:
    @staticmethod
    async def send_discord_webhook(
        session: CachedSession,
        url: str,
        ctx: Context,
        content: str,
        title: str,
        author_url: str,
        embeds: list[DiscordEmbed] | None = None,
        title2: str | None = None,
        ping: bool = True,
    ) -> aiohttp.ClientResponse:
        to_mark = ctx.bot.config.Discord.to_mark
        avatar_webhook = ctx.bot.config.Discord.webhook_avatar
        user = await ctx.author.user()
        display_name = ctx.author.display_name
        profile_image = user.profile_image.url
        webhook = DiscordWebhook(
            url=url,
            username=ctx.bot.bot_user.display_name.title(),
            session=session,
            avatar_url=avatar_webhook,
        )
        url_params = f"{ctx.channel.name}/{datetime.now(UTC).year}/{datetime.now(UTC).month}/{datetime.now(UTC).day}"
        log_url1 = f"https://logs.mrchuw.com.br/channel/{url_params}"
        log_url2 = f"https://logxx.dev/channel/{url_params}"
        log_url3 = (
            f"https://tv.supa.sh/logs?c={ctx.channel.name}&d={datetime.now(UTC).strftime('%Y-%m-%d')}#{ctx.message.id}"
        )
        embed = DiscordEmbed()
        embed.set_author(name=display_name, url=author_url, icon_url=profile_image)
        embed.set_title(title2 or title)
        embed.set_description(f"{content}\n\n{log_url1}\n{log_url2}\n{log_url3}")
        embed.set_timestamp(ctx.message.timestamp)
        embed.set_color(ctx.author.color.hex if hasattr(ctx.author, "color") else "03b2f8")
        if to_mark and ping:
            webhook.set_content(" ".join([f"<@{mark}>" for mark in to_mark]) + f" {title}")
        webhook.add_embed(embed)
        if embeds:
            for extra_embed in embeds:
                webhook.add_embed(extra_embed)

        return await webhook.execute()
