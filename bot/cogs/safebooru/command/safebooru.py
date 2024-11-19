# -*- coding: utf-8 -*-
import time

from yarl import URL
from random import randint

from bot.apis import booru
from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response


@base_decorator(BaseDecorators.TypeChecking)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='safebooru', aliases=['sfbo'])
async def command(ctx: Context, *, args: str = "") -> Response:
    translations, instance, start_time = ctx.translations.NSFW.Boru, booru.Booru().boorus["safebooru"], time.time()
    amount = int(args.split(" ")[0]) if args.split(" ")[0].isdigit() and ctx.author.id is ctx.bot.config.BotConfig.dev_userid else min(int(args.split(" ")[0]) if args.split(" ")[0].isdigit() else 1, 10)
    tags = args.split(" ")[1:] if args.split(" ")[0].isdigit() else args.split(" ")

    if len(tags) > 10:
        return translations.too_much_tags.format_response(ctx, 10, success=False)

    while True:
        img, img_preview, response_final = await response(ctx, " ".join(tags), instance, start_time, amount)
        if not img_preview:
            return translations.unexpected_error.format_response(ctx, response_final, success=False)
        if response_final:
            return translations.success.format_response(ctx, response_final)


async def response(ctx: Context, args: str, instance, start_time, amount):
    img, img_preview = await choices(args, instance, start_time, amount, ctx)
    if img_preview == "error":
        return None, False, img

    translation = ctx.translations.NSFW.Boru
    if not img or not img_preview:
        return None, None, False

    response_final = " ".join(
            f"{translation.original}: {img[i]} || {translation.preview}: {img_preview[i]}" if img_preview[
                i] else f"{translation.original}: {img[i]}" for i in range(min(amount, len(img)))
    )
    return img, img_preview, response_final or False


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
    session, shorter = ctx.bot.SessionsCaches.BooruCachedSession.session, ctx.bot.UploadThings.shortener

    async def shorten(imagem):
        return await shorter(imagem.human_repr() if imagem else None, ["booru"], ctx.bot, session)

    return ([await shorten(imagem) for imagem in images],
            [await shorten(imagem_preview) for imagem_preview in images_preview])


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Safebooru = command_.decorators[lang]
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
        commands_admonitions = getattr(decorator, 'admonitions', EnDecorators.Safebooru.admonitions)

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

        if commands := getattr(decorator, 'commands', EnDecorators.Safebooru.commands):
            command_body += "".join([
                    command_template.format(prefix=prefix, command_name=command_.name.lower(), args=item.args,
                                            response=item.response
                                            ) for item in commands]
            )
        if commands_admonitions:
            for admonition in commands_admonitions:
                if admonition.position == "bottom":
                    command_body += admonition_template.format(type=admonition.type, title=admonition.title,
                                                               message=admonition.message
                                                               )

        responses[lang][command_.name.lower()] = command_body

    return responses
