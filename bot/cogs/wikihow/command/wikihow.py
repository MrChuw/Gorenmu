# -*- coding: utf-8 -*-
import asyncio

from aiohttp_client_cache import CachedResponse, CachedSession

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import EnDecorators, Response


async def get_wiki(session: CachedSession, url: str) -> CachedResponse:
    async with session.disabled():
        await asyncio.sleep(1)
        response = await session.get(url, allow_redirects=True)  # NOQA
    return response  # NOQA


@base_decorator(EnDecorators.Wikihow)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='wikihow', aliases=[])
async def command(ctx: Context, *, quantity="") -> Response:
    translations = ctx.translations.Wikihow
    quantity = int(quantity) if quantity.isdigit() else 1
    quantity = min(quantity, 10) if ctx.author.name != "mr_chuw" else quantity
    session = ctx.bot.SessionsCaches.WikihowCachedSession.session
    responses = []
    try:
        for _ in range(quantity):
            wiki = await get_wiki(session, translations.url)
            while wiki.status == 404:
                wiki = await get_wiki(session, translations.url)
            if wiki.status in [200, 304]:
                responses.append(wiki.url.human_repr())
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
        decorator: EnDecorators.Wikihow = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)

        language: EnDecorators = bot.TranslationManager.languages[lang][0]
        command_body_template = getattr(language, 'template', EnDecorators.template)
        alias_template = getattr(language, 'alias_template', EnDecorators.alias_template)
        command_template = getattr(language, 'command_template', EnDecorators.command_template)
        admonition_template = getattr(language, 'admonition_template', EnDecorators.admonition_template)

        aliases = ""
        if command_.aliases:
            aliases = alias_template.format(command_title=command_.name.capitalize(),
                                            aliases=", ".join(command_.aliases)
                                            )

        command_body = command_body_template.format(command_title=command_.name.capitalize(), rate=rate, per=per,
                                                    description=description, cooldown_type=cooldown_type,
                                                    aliases=aliases
                                                    )

        if commands := getattr(decorator, 'commands', EnDecorators.Wikihow.commands):
            command_body += "".join([
                    command_template.format(prefix=prefix, command_name=command_.name.lower(), args=item.args,
                                            response=item.response
                                            ) for item in commands])

        if commands_admonitions := getattr(decorator, 'admonitions', EnDecorators.Wikihow.admonitions):
            command_body += "".join([admonition_template.format(type=admonition.type, title=admonition.title,
                                                                message=admonition.message, ) for admonition in
                                     commands_admonitions]
                                    )

        responses[lang][command_.name.lower()] = command_body

    return responses
