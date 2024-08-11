# -*- coding: utf-8 -*-
import asyncio
import datetime
from bot.bot import Gorenmu
from bot.models import User, Channel, Alias
from bot.utils import Check, Role
from typing import Dict, Any, List, Tuple, Optional, Coroutine, Callable
from bot.ext.commands import Bucket, check, Context, cooldown, base_decorator, helper, usage, command
from bot.translations import EnUsTranslations, EnUsDecorators, Response
from twitchio.ext.commands import Command
import re
from itertools import chain, repeat
from urllib.parse import quote

ALIAS_NAME_REGEX = re.compile(
        r'^[-\w\u00a9\u00ae\u2000-\u3300\ud83c\ud000-\udfff\ud83d\ud000-\udfff\ud83e\ud000-\udfff]{2,30}$'
)

ALIAS_DESCRIPTION_LIMIT = 250
NESTED_ALIAS_LIMIT = 10


@base_decorator(EnUsDecorators.Afk)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='alias', aliases=[''])
async def command(ctx: Context, action: str, *args, ) -> Response:
    if action.lower() in ["add"]:
        return await add_alias(ctx, args)
    elif action.lower() in ["check"]:
        return await check_alias(ctx, args)
    elif action.lower() in ["copy"]:
        return await copy_alias(ctx, args)

# TODO:
#  edit/rename
#  remove


def parse_command_by_name(ctx: Context, string: str) -> Command:
    prefix = ctx.prefix
    if string.startswith(prefix) and len(string) > len(prefix):
        return ctx.bot.get_command(string[len(prefix):])
    else:
        return ctx.bot.get_command(string)


async def add_alias(ctx: Context, args):
    translations = ctx.translations.Alias
    name, command_, *rest = chain(args, repeat(None, 2))
    if not command_:
        return translations.no_command_to_add.format_response(ctx, ctx.prefix, success=False)

    if not ALIAS_NAME_REGEX.match(name):
        return translations.alias_invalid_name.format_response(ctx, success=False)

    alias = await Alias.get_or_none(user=ctx.user, name=name)

    if alias:
        return translations.alias_name_conflict.format_response(ctx, args, success=False)

    command_check = parse_command_by_name(ctx, command_)
    if not command_check:
        return translations.command_dont_exist.format_response(ctx, command_, success=False)

    alias = await Alias.save_alias(ctx, name, command_check, command_, rest)
    await ctx.bot.cache.set([f"{ctx.author.id}-{name}"], alias.id, ttl=43200, namespace="alias")
    return translations.alias_crated.format_response(ctx, alias.name)


async def check_alias(ctx: Context, args):
    translations = ctx.translations.Alias
    first_name, second_name, *rest = chain(args, repeat(None, 2))
    # TODO: Make so he create a bin.mrchuw.com.br with all the alias from the user.
    if not first_name and not second_name:
        username = ctx.author.name
        return translations.user_alias_list.format_response(ctx, username, success=False)

    target_aliases = []
    aliases = await Alias.filter(channel__isnull=True, user=ctx.user).values_list('name', flat=True)

    target_user = await User.get_or_none(name=first_name)
    if target_user:
        target_aliases = await Alias.filter(channel__isnull=True, user=target_user).values_list('name', flat=True)

    if target_aliases == [] and first_name not in aliases:
        return translations.no_alias_found.format_response(ctx, second_name, target_user.name, success=False)
    elif target_aliases == [] and first_name in aliases:
        user = ctx.user
        alias_name = first_name
        mention = translations.mention(ctx, user, user.name)
    elif target_aliases and first_name not in aliases:
        mention = translations.mention(ctx, target_user, ctx.author.name)
        url = "TODO"
        # TODO: The same thing of the first if.
        return translations.list_of_alias_of.format_response(ctx, mention, url, success=True)
    else:
        url1 = "TODO from the user."
        url2 = "TODO from the user that has the same name as the alias."
        # TODO: Here the case is if some one has the same name as a alias.
        return translations.list_of_special_case.format_response(ctx, first_name, url1, url2)

    if second_name:
        user = await User.get_or_none(name=first_name)
        if not user:
            return translations.user_not_found.format_response(ctx, first_name, success=False)

        alias_name = second_name
        mention = translations.mention(ctx, user, ctx.author.name)

    alias = await Alias.filter(user_id=user.id, name=alias_name).first().prefetch_related("parent")

    if not alias:
        return translations.alias_not_found.format_response(ctx, mention, alias_name, success=False)

    appendix = ""
    if not alias.command and not alias.parent:  # NOQA
        return translations.alias_deleted.format_response(ctx, mention, success=False)

    elif not alias.command and alias.parent:  # NOQA
        alias = await Alias.get(id=alias.parent.id)
        original_user = await User.get(id=alias.user.id)
        appendix = translations.appendix.format(alias.name, original_user.name)

    message = f"{alias.invocation} {' '.join(alias.arguments)}"
    if alias.arguments:
        message = translations.message.format(appendix, mention, alias_name,
                                              alias.invocation, ' '.join(alias.arguments))
    # TODO: Here the case is if some one has the same name as a alias.
    url = "TODO"

    return translations.final_message.format_response(ctx, message, url)


async def copy_alias(ctx: Context, args):
    translations = ctx.translations.Alias
    target_user_name, target_alias_name = chain(args, repeat(None, 2))

    if not target_user_name:
        return translations.user_not_found.format_response(ctx, success=False)
    if not target_alias_name:
        return translations.alias_not_provided.format_response(ctx, success=False)
    if not ALIAS_NAME_REGEX.match(target_alias_name):
        return translations.target_alias_invalid_name.format_response(ctx, success=False)

    target_user = await User.get_or_none(name=target_user_name)
    if not target_user:
        return translations.user_not_found.format_response(ctx, target_user_name, success=False)

    target_alias = await Alias.filter(channel__isnull=True, user=target_user, name=target_alias_name).first()
    if target_alias.command is None:  # NOQA
        # TODO: See if this is point to the right user.
        return translations.link_to_a_link.format_response(ctx, target_user.name, target_alias_name, success=False)




