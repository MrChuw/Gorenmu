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
from bot.translations import EnDecorators, Response

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
            elif url.status == 429 or url.status == 503:
                return links
        if len(links) < quantity:
            if quantity >= 1001:
                await asyncio.sleep(5)
                timeout += 15
                new_quantity = int(quantity * 0.2)
                urls = await generate_links(quantity=new_quantity, k=k,
                                            session=ctx.bot.SessionsCaches.ImgurCachedSession.session
                                            )
            else:
                await asyncio.sleep(1)
                new_quantity = int(quantity * 0.5)
                urls = await generate_links(quantity=new_quantity, k=k,
                                            session=ctx.bot.SessionsCaches.ImgurCachedSession.session
                                            )
        else:
            return links


@base_decorator(EnDecorators.NSFW.Imgur)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='imgur', aliases=['imgur7'])
async def command(ctx: Context, args: str = "") -> Response:
    translations = ctx.translations.NSFW.Imgur
    quantity = int(args) if args.isdigit() is True else 1
    quantity = quantity if int(ctx.author.id) in ctx.bot.config.BotConfig.imgur_permitidos else (
            quantity) if quantity <= 100 else 100
    time_start = time.perf_counter()
    k = 5 if ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower() == "imgur" else 7
    timeout = timeout_calc(quantity)
    links = await generate(ctx, quantity, k)
    responses = []
    embed = None
    if links is not None:
        finished = ctx.translations.SupportTools.Humanize.Humanize.precisedelta(time.perf_counter() - time_start,
                                                                                minimum_unit="microseconds"
                                                                                )
        await Imgur.bulk_create(
                [Imgur(user=ctx.user, link=link.split(" ", 1)[0].replace("https://i.imgur.com/", "").replace(".jpg", ""
                                                                                                             )
                       ) for link in links]
                )
        if len(links) > 1:
            embed = await ctx.bot.UploadThings.send_imgur(" ".join(link.split()[0] for link in links), ctx.bot,
                                                          ctx.bot.SessionsCaches.ImgurCachedSession.session
                                                          )
            await ImgurAggregate.create(link=embed, user=ctx.user)
        if quantity < 10:
            # if len(links) > quantity:
            if embed:
                responses.append(" ".join(links[:quantity]).replace("i.imgur.com/", "rg.psf.lt/"))
                responses.append(translations.all_images_embed.format(embed))
                return translations.links.format_response(ctx, response_list=responses)
        if quantity >= 10:
            if embed:
                responses.append(translations.all_images_embed_time.format(finished, embed))
                return translations.links.format_response(ctx, response_list=responses)
        if quantity >= 25:
            responses.append(translations.time_message.format(finished))
        for i in range(0, len(links), 10):
            chunk = links[i:i + 10]
            responses.append(" ".join(chunk).replace("i.imgur.com/", "rg.psf.lt/"))
        return translations.links.format_response(ctx, response_list=responses)
    else:
        return translations.timeout.format_response(ctx, success=False)


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.NSFW.Imgur = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        afk_template = getattr(decorator, 'template', EnDecorators.NSFW.Imgur.template).format(
                rate=rate, per=per,
                cooldown_type=cooldown_type,
                description=description,
                command_title=command_.name.capitalize(),
                command_name=command_.name.lower(),
                prefix=prefix,
                aliases=", ".join(command_.aliases)
        )

        responses[lang][command_.name.lower()] = afk_template

    return responses
