# -*- coding: utf-8 -*-
import asyncio

from aiohttp_client_cache import CachedSession, response
from bs4 import BeautifulSoup

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import EnDecorators, Response


async def get_scp(session: CachedSession) -> response:
    async with session.disabled():
        response = await session.get("https://scp-wiki.wikidot.com/random:random-page")  # NOQA
    soup = BeautifulSoup(await response.text(), 'html.parser')
    iframe = soup.find('iframe', src=lambda x: x and 'https://snippets.wdfiles.com/local--code/code:' in x)
    url = iframe['src'].replace("https://snippets.wdfiles.com/local--code/code:iframe-redirect#http", "https")  # NOQA
    return await session.head(url)


@base_decorator(EnDecorators.Scp)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='randomscp', aliases=['rscp'])
async def command(ctx: Context, quantity: str = "") -> Response:
    translations = ctx.translations.Scp
    quantity = int(quantity) if quantity.isdigit() else 1
    quantity = min(quantity, 10) if ctx.author.name != "mr_chuw" else quantity
    session = ctx.bot.SessionsCaches.ScpCachedSession.session
    responses = []
    try:
        for _ in range(quantity):
            scp = await get_scp(session)
            while scp.status == 404:
                scp = await get_scp(session)
                await asyncio.sleep(1)
            if scp.status == 200:
                responses.append(scp.url.human_repr())
        return translations.links.format_response(ctx, response_list=responses)
    except Exception as e:
        ctx.bot.log.error(e, exc_info=e)
        return translations.unexpected_error.format_response(ctx, success=False)


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Scp = command_.decorators[lang]
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
        commands_admonitions = getattr(decorator, 'admonitions', EnDecorators.Scp.admonitions)
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

        if commands := getattr(decorator, 'commands', EnDecorators.Scp.commands):
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
