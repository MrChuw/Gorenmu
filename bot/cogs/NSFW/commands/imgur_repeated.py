# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import AsyncIterator

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.models import Imgur
from bot.translations import BaseDecorators, Response


@base_decorator(BaseDecorators.NSFW.ImgurRepeated)
@cooldown(rate=3, per=10, bucket=Bucket.mod)
@check([])
@command(name='imgur_repeated', aliases=[])
async def command(ctx: Context) -> Response:
    translations = ctx.translations.NSFW.ImgurRepeated
    urls: dict[str, int] = {}
    async for links in get_links():
        urls = defaultdict(int)
        for link in links:
            urls[link.link] += 1
    sorted_urls = {k: v for k, v in sorted(urls.items(), key=lambda x: x[1], reverse=True) if v > 1}
    if not sorted_urls:
        return translations.no_repeated.format_response(ctx)
    duplicates = [f"https://i.imgur.com/{link}.jpg" for link in sorted_urls]
    embed = await ctx.bot.UploadThings.send_imgur(duplicates, ctx.bot, ctx.bot.SessionsCaches.ImgurCachedSession.session
                                                  )
    return translations.links_repeated.format_response(ctx, len(duplicates), embed)


async def get_links() -> AsyncIterator[list[Imgur]]:
    offset = 0
    batch_size = 100
    while True:
        items = await Imgur.all().offset(offset).limit(batch_size)

        if not items:
            break

        yield items
        offset += batch_size

