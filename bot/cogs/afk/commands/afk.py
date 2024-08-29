# -*- coding: utf-8 -*-
import asyncio
import datetime
from bot.bot import Gorenmu
from bot.models import User, Channel, Status
from bot.utils import Check, Role
from typing import Dict, Any, List, Tuple, Optional, Coroutine, Callable
from bot.ext.commands import Bucket, check, Context, cooldown, base_decorator, helper, usage, command, Command
from bot.translations import EnTranslations, EnDecorators, Response
from bot.translations.en.extras import Activity
from bot.utils import StringTools
from textwrap import dedent

afk_alias = [s for s in Activity().afks if s != "afk"]
rafk_alias = ["rafk"] + [f"r{s}" for s in Activity.afks if s != "afk"]
aliasas = afk_alias + rafk_alias + ["isafk"]


@base_decorator(EnDecorators.Afk)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name="afk", aliases=aliasas)
async def command(ctx: Context, *, content: str = "") -> Response:
    invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
    if invoke_by in afk_alias + ["afk"]:
        return await afk(ctx, content, invoke_by)
    elif invoke_by in rafk_alias:
        return await rafk(ctx)
    elif invoke_by == "isafk":
        return await isafk(ctx, content)


async def afk(ctx: Context, content: str, invoke_by: str) -> Response:
    translations = ctx.translations.Afk
    if len(content) >= 450:
        return translations.Afk.message_too_long.format_response(ctx, success=False, pipe=False)
    afk = translations.afks.get(invoke_by)  # NOQA
    await go_afk(afk, content, ctx)
    if not content:
        return translations.Afk.afk_response.format_response(ctx, afk.leave, afk.emoji, pipe=False)
    else:
        return translations.Afk.afk_content_response.format_response(ctx, afk.leave, afk.emoji, content, pipe=False)


async def rafk(ctx: Context) -> Response:
    translations = ctx.translations.Afk
    afk = await ctx.bot.cache.get(f"{ctx.author.id}", namespace="status")  # NOQA
    if afk is None:
        return translations.RAfk().time_expired.format_response(ctx, success=False)
    elif afk["alias"] in translations.afks:
        status = translations.afks[afk["alias"]]
        await ctx.bot.cache.delete(f"Afk-{ctx.author.id}")
        await go_rafk(afk, ctx)
        if afk["content"] == "":
            return translations.RAfk().is_afk.format_response(ctx, status.leave_again, status.emoji, pipe=False)
        else:
            return translations.RAfk().is_afk.format_response(ctx, status.leave_again, status.emoji, afk["content"], pipe=False)
    else:
        return translations.RAfk().is_not_afk.format_response(ctx, success=False, pipe=False)


async def isafk(ctx: Context, content: str) -> Response:
    translations = ctx.translations.Afk
    name = StringTools.str2name(content.split()[0])
    actions = {
        ctx.bot.nick: translations.IsAfk().bot_nick.format_response(ctx, success=False),
        ctx.author.name: translations.IsAfk().author_nick.format_response(ctx, success=False)}
    if name in actions:
        return actions[name]
    else:
        user = await User.get_or_none(name=name)
        if not user:
            return translations.IsAfk().never_seen.format_response(ctx, name)
        await user.fetch_related("status")
        if not user.status:
            return translations.IsAfk().is_not_afk.format_response(ctx, name)
        afk: Status = user.status[0]  # NOQA
        status = translations.afks[afk.alias]
        if not afk.message:
            return translations.IsAfk().is_afk.format_response(ctx, name, status.current, status.emoji)
        return translations.IsAfk().is_afk.format_response(ctx, name, status.current, status.emoji, afk.message)


async def go_afk(afk, content, ctx):
    user_status = await Status.get(user=ctx.user)
    user_status.online = False
    user_status.alias = afk.name
    user_status.message = content
    user_status.updated_at = datetime.datetime.now(datetime.timezone.utc)
    await user_status.save()


async def go_rafk(afk, ctx):
    user_status = await Status.get(user=ctx.user)
    user_status.online = False
    user_status.alias = afk["alias"]
    user_status.message = afk["content"]
    user_status.updated_at = datetime.datetime.fromisoformat(afk["updated_at"])
    await user_status.save()


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]:
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Afk = command_.decorators[lang]
        description = decorator.Afk.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        afk_template = getattr(decorator.Afk, 'template', EnDecorators.Afk.Afk.template).format(
                rate=rate,
                per=per,
                cooldown_type=cooldown_type,
                description=description,
                command_title="Afk",
                command_name="afk",
                prefix=prefix,
                aliases=", ".join(afk_alias))

        responses[lang]['afk'] = afk_template

        description = decorator.IsAfk.get_description(decorator)  # NOQA
        isafk_template = getattr(decorator.IsAfk, 'template', EnDecorators.Afk.IsAfk.template).format(
                rate=rate,
                per=per,
                cooldown_type=cooldown_type,
                description=description,
                command_title="IsAfk",
                command_name="isafk",
                prefix=prefix,
        )

        responses[lang]['isafk'] = isafk_template

        description = decorator.RAfk.get_description(decorator)  # NOQA
        isafk_template = getattr(decorator.RAfk, 'template', EnDecorators.Afk.RAfk.template).format(
                rate=rate,
                per=per,
                cooldown_type=cooldown_type,
                description=description,
                command_title="RAfk",
                command_name="rafk",
                prefix=prefix,
                aliases=", ".join(rafk_alias)
        )

        responses[lang]['rafk'] = isafk_template

    return responses













