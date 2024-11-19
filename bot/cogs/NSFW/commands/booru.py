# -*- coding: utf-8 -*-
import asyncio
import datetime
from bot.bot import Gorenmu
from bot.models import User, Channel
from bot.utils import Check, Role
from typing import Dict, Any, List, Tuple, Optional, Coroutine, Callable
from bot.ext.commands import Bucket, check, Context, cooldown, base_decorator, helper, usage, command
from bot.translations import BaseDecorators, Response
from bot.bot import Gorenmu
from bot.ext.commands import Command
import time
from yarl import URL
from bot.apis import booru
from random import choice
from random import randint



tag_amount = {
    "glbo": 10, "gelbooru": 10,  # NOQA
    "dnbo": 10, "danbooru": 10,  # NOQA
    "rule34": 10,  # NOQA
    "rlbo": 10, "realbooru": 10,  # NOQA
    "tbibo": 10, "tbib": 10,  # NOQA
    "xbbo": 10, "xbooru": 10,  # NOQA
    "sfbo": 10, "safebooru": 10,  # NOQA
    "ynbo": 10, "yandere": 10,  # NOQA
    "Knbo": 10, "konachan": 10,  # NOQA
    "hybo": 10, "hypnohub": 10,  # NOQA
    "e621bo": 10, "e621": 10,  # NOQA
    "e926bo": 10, "e926": 10,  # NOQA
    "dpbo": 1, "derpibooru": 1,  # NOQA
    "fubo": 1, "furbooru": 1,  # NOQA
    "bhbo": 10, "behoimi": 10,  # NOQA
    "phbo": 3, "paheal": 3,  # NOQA
    "knnbo": 6, "konachan_net": 6,  # NOQA
}



@base_decorator(BaseDecorators.TypeChecking)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='booru',
         aliases=[
                 "glbo", "gelbooru",  # NOQA
                 "dnbo", "danbooru",  # NOQA
                 "rule34", "rule34",  # NOQA
                 "rlbo", "realbooru",  # NOQA
                 "tbibo", "tbib",  # NOQA
                 "xbbo", "xbooru",  # NOQA
                 "ynbo", "yandere",  # NOQA
                 "knbo", "konachan",  # NOQA
                 "hybo", "hypnohub",  # NOQA
                 "e621bo", "e621",  # NOQA
                 "e926bo", "e926",  # NOQA
                 "dpbo", "derpibooru",  # NOQA
                 "fubo", "furbooru",  # NOQA
                 "bhbo", "behoimi",  # NOQA
                 "phbo", "paheal",  # NOQA
                 "knnbo", "konachan_net",  # NOQA
            ])
async def command(ctx: Context, *, args: str = "") -> Response:
    translations = ctx.translations.NSFW.Boru
    img, img_preview = None, None
    if ctx.invoke_by == "booru":
        chosen = choice(list(booru.Booru().boorus))
        max_tags = tag_amount[chosen]
        instance = booru.Booru().boorus[chosen]
    else:
        max_tags = tag_amount[ctx.invoke_by]
        instance = booru.Booru().boorus[ctx.invoke_by]
    start_time = time.time()
    amount = 1
    tags = None
    response_final = None

    if args.isdigit():
        if type(args) is str:
            amount = int(args)
        amount = (amount if ctx.author.name in ctx.bot.config.BotConfig.imgur_permitidos else min(amount, 10))

    # if args and "--" in args:
    #     amount = [x for x in args.split(" ") if "--" in x][0].replace("--", "")
    #     if amount.isdigit():
    #         if type(amount) is str:
    #             amount = int(amount)
    #         amount = (
    #             amount
    #             if ctx.author.name in ctx.bot.config.BotConfig.imgur_permitidos
    #             else min(amount, 10)
    #         )
    #         args = args.replace(f"--{amount}", "")
    #         if args:
    #             if args[0] == " ":
    #                 args = args.replace(" ", "", 1)
    #             tags = args.split()
    #             if len(tags) > max_tags:
    #                 return translations.too_much_tags.format_response(ctx, max_tags, success=False)
    #             else:
    #                 tags = " ".join(tags)
    #     else:
    #         amount = 1

    tags = ""

    while not img or not img_preview:
        img, img_preview, response_final = await response(ctx=ctx, args=tags, instance=instance, start_time=start_time,
                                                          amount=amount
                                                          )
        if not img_preview:
            return translations.unexpected_error.format_response(ctx, response_final, success=False)

    if response_final:
        return translations.success.format_response(ctx, response_final)


async def response(ctx: Context, args: str, instance, start_time, amount):
    img, img_preview = await choices(args=args, instance=instance, start_time=start_time, amount=amount, ctx=ctx)
    if img_preview == "error":
        return None, False, img

    response_final = None
    response = None
    if img is None and img_preview is None:
        return None, None, False

    translation = ctx.translations.NSFW.Boru
    original_str = translation.original
    preview_str = translation.preview

    if len(img) < amount:
        amount = len(img)

    for i in range(amount):
        if img[i]:
            response = f"{original_str}: {img[i]}"

        if img_preview[i]:
            if response:
                response = f"{response} || {preview_str}: {img_preview[i]}"
            else:
                response = f"{preview_str}: {img_preview[i]}"

        if response:
            response_final = f"{response_final} {response}" if response_final else response
    if response_final:
        return img, img_preview, f"{response_final} "
    return None, None, False


async def choices(args: str, instance, start_time: float, amount: int, ctx: Context):
    session, elapsed_time = ctx.bot.SessionsCaches.BooruCachedSession.session, time.time() - start_time
    instance = instance(session=session, amount=amount)
    while elapsed_time <= 15:
        try:
            image, preview = await instance.random(query=args or "", page=randint(0, 100))
            return await shortener(image, preview, ctx)
        except Exception as e:
            ctx.bot.log.error(e)
        elapsed_time = time.time() - start_time
    return ctx.translations.SupportTools.Humanize.precisedelta(elapsed_time), "error"


async def shortener(images: list[URL], images_preview: list[URL], ctx: Context):
    imagens_finais = []
    previews_finais = []
    session = ctx.bot.SessionsCaches.BooruCachedSession.session
    shorter = ctx.bot.UploadThings.shortener
    for imagem, imagem_preview in zip(images, images_preview):
        if imagem:
            imagens_finais.append(await shorter(imagem.human_repr(), ["booru"], ctx.bot, session))
        else:
            imagens_finais.append(await shorter(None, ["booru"], ctx.bot, session))

        if imagem_preview:
            previews_finais.append(await shorter(imagem_preview.human_repr(), ["booru"], ctx.bot, session))
        else:
            previews_finais.append(await shorter(None, ["booru"], ctx.bot, session))

    return imagens_finais, previews_finais


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Change_Here = command_.decorators[lang]
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

        command_body = command_body_template1.format(
                                            command_title=command_.name.capitalize(),
                                            rate=rate, per=per,
                                            cooldown_type=cooldown_type,
                                            )
        commands_admonitions = getattr(decorator, 'admonitions', EnDecorators.Change_Here.admonitions)

        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "top":
                    command_body += admonition_template.format(
                            type=admonition.type,
                            title=admonition.title,
                            message=admonition.message)

        command_body += command_body_template2.format(description=description, aliases=aliases)

        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "middle":
                    command_body += admonition_template.format(
                            type=admonition.type,
                            title=admonition.title,
                            message=admonition.message)

        command_body += command_body_template3

        if commands := getattr(decorator, 'commands', EnDecorators.Change_Here.commands):
            command_body += "".join([
                    command_template.format(prefix=prefix, command_name=command_.name.lower(), args=item.args,
                                            response=item.response
                                            ) for item in commands])
        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "bottom":
                    command_body += admonition_template.format(
                            type=admonition.type,
                            title=admonition.title,
                            message=admonition.message)

        responses[lang][command_.name.lower()] = command_body

    return responses































