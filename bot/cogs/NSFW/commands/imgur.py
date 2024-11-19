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

        language: EnDecorators = bot.TranslationManager.languages[lang][0]
        command_body_template1: str = getattr(language, 'template_part1', EnDecorators.template_part1)
        command_body_template2: str = getattr(language, 'template_part2', EnDecorators.template_part2)
        command_body_template3: str = getattr(language, 'template_part3', EnDecorators.template_part3)
        alias_template: str = getattr(language, 'alias_template', EnDecorators.alias_template)
        command_template: str = getattr(language, 'command_template', EnDecorators.command_template)
        admonition_template: str = getattr(language, 'admonition_template', EnDecorators.admonition_template)

        aliases = ""
        if command_.aliases:
            aliases = alias_template.format(command_title=command_.name.capitalize(),
                                            aliases=", ".join(command_.aliases)
                                            )

        command_body = command_body_template1.format(command_title=command_.name.capitalize(), rate=rate, per=per,
                                                     cooldown_type=cooldown_type, )
        commands_admonitions = getattr(decorator, 'admonitions', EnDecorators.NSFW.Imgur.admonitions)
        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "top":
                    command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                               message=admonition.message
                                                               )

        command_body += command_body_template2.format(description=description, aliases=aliases)

        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "middle":
                    command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                               message=admonition.message
                                                               )

        command_body += command_body_template3

        if commands := getattr(decorator, 'commands', EnDecorators.NSFW.Imgur.commands):
            command_body += "".join([
                    command_template.format(prefix=prefix, command_name=command_.name.lower(), args=item.args,
                                            response=item.response
                                            ) for item in commands])

        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "bottom":
                    command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                               message=admonition.message
                                                               )

        responses[lang][command_.name.lower()] = command_body

    return responses
