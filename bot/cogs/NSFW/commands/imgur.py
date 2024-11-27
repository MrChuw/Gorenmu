# -*- coding: utf-8 -*-
import asyncio
import random
import time
from string import ascii_letters, digits
from typing import List

from aiohttp_client_cache import CachedSession

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.models import Imgur, ImgurAggregate
from bot.translations import BaseDecorators, Response

timeout_calc = lambda q: 250 + ((q // 500) * 120)  # NOQA


async def generate_links(quantity: int, k: int, session: CachedSession):
    urls = ["https://i.imgur.com/" + "".join(random.choices(ascii_letters + digits, k=k)) + ".jpg" for _ in
            range(quantity + 10)]
    tasks = [asyncio.create_task(session.head(url=url, allow_redirects=False)) for url in urls]
    return await asyncio.gather(*tasks)


async def generate(ctx: Context, quantity: int, k: int) -> List[str]:
    links = []
    urls = await generate_links(quantity=quantity, k=k, session=ctx.bot.SessionsCaches.ImgurCachedSession.session)
    start_time = time.perf_counter()
    timeout = timeout_calc(quantity)
    count = 0

    while len(links) != quantity:
        if (time.perf_counter() - start_time) >= timeout:
            return links or None
        if len(links) >= quantity:
            break
        for url in urls:
            if url.status == 200:
                links.append(f"{url.url} {len(links) + 1}º ")
                count += 1
            elif url.status in [429, 503]:
                return links
        if len(links) >= quantity:
            return links
        if quantity >= 1001:
            await asyncio.sleep(5)
            timeout += 15
            new_quantity = int(quantity * 0.2)
        else:
            await asyncio.sleep(1)
            new_quantity = int(quantity * 0.5)
        urls = await generate_links(quantity=new_quantity, k=k,
                                    session=ctx.bot.SessionsCaches.ImgurCachedSession.session
                                    )


@base_decorator(BaseDecorators.NSFW.Imgur)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='imgur', aliases=['imgur7'])
async def command(ctx: Context, args: str = "") -> Response:
    translations = ctx.translations.NSFW.Imgur
    quantity = int(args) if args.isdigit() else 1
    quantity = quantity if int(ctx.author.id) in ctx.bot.config.BotConfig.imgur_permitidos else min(quantity, 100)
    time_start = time.perf_counter()
    k = 5 if ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower() == "imgur" else 7
    links = await generate(ctx, quantity, k)
    embed = None
    if links is None:
        return translations.timeout.format_response(ctx, success=False)
    finished = ctx.translations.SupportTools.Humanize.precisedelta(time.perf_counter() - time_start,
                                                                            minimum_unit="microseconds"
                                                                            )
    await Imgur.bulk_create(
            [Imgur(user=ctx.user, link=link.split(" ", 1)[0].replace("https://i.imgur.com/", "").replace(".jpg", ""
                                                                                                         )
                   ) for link in links]
    )
    if len(links) > 1:
        embed = await ctx.bot.UploadThings.send_imgur([link.split()[0] for link in links], ctx.bot,
                                                      ctx.bot.SessionsCaches.ImgurCachedSession.session
                                                      )
        await ImgurAggregate.create(link=embed, user=ctx.user)
    responses = []
    if quantity < 10 and embed:
        responses.extend((" ".join(links[:quantity]).replace("i.imgur.com/", "rg.psf.lt/"),
                          translations.all_images_embed.format(embed))
                         )
        return translations.links.format_response(ctx, response_list=responses)
    if quantity >= 10 and embed:
        responses.append(translations.all_images_embed_time.format(finished, embed))
        return translations.links.format_response(ctx, response_list=responses)
    if quantity >= 25:
        responses.append(translations.time_message.format(finished))
    for i in range(0, len(links), 10):
        chunk = links[i:i + 10]
        responses.append(" ".join(chunk).replace("i.imgur.com/", "rg.psf.lt/"))
    return translations.links.format_response(ctx, response_list=responses)


