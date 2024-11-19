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


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.NSFW.ImgurRepeated = command_.decorators[lang]
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
        commands_admonitions = getattr(decorator, 'admonitions', EnDecorators.NSFW.ImgurRepeated.admonitions)
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

        if commands := getattr(decorator, 'commands', EnDecorators.NSFW.ImgurRepeated.commands):
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
