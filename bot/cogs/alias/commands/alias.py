# -*- coding: utf-8 -*-
import re
from itertools import chain, repeat

from twitchio.ext.commands import Command

from bot.ext.commands import base_decorator, Bucket, check, command, Context, cooldown
from bot.models import Alias, User
from bot.translations import EnUsDecorators, Response

ALIAS_NAME_REGEX = re.compile(
        r'^[-\w\u00a9\u00ae\u2000-\u3300\ud83c\ud000-\udfff\ud83d\ud000-\udfff\ud83e\ud000-\udfff]{2,30}$'
)


@base_decorator(EnUsDecorators.Alias)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='alias', aliases=[''])
async def command(ctx: Context, action: str, *args, ) -> Response:
    if action.lower() in ["add"]:
        return await add_alias(ctx, args)
    elif action.lower() in ["check", "list"]:
        return await check_alias(ctx, args)
    elif action.lower() in ["copy"]:
        return await copy_alias(ctx, args)
    elif action.lower() in ["describe"]:
        return await describe_alias(ctx, args)
    elif action.lower() in ["edit"]:
        return await edit_alias(ctx, args)
    elif action.lower() in ["link"]:
        return await link_alias(ctx, args)
    elif action.lower() in ["remove"]:
        return await remove_alias(ctx, args)
    elif action.lower() in ["rename"]:
        return await rename_alias(ctx, args)


def parse_command_by_name(ctx: Context, string: str) -> Command:
    prefix = ctx.prefix
    if string.startswith(prefix) and len(string) > len(prefix):
        return ctx.bot.get_command(string[len(prefix):])
    else:
        return ctx.bot.get_command(string)


async def add_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    name, command_, *rest = chain(args, repeat(None, 2))
    if not command_:
        return translations.Add.no_command_to_add.format_response(ctx, ctx.prefix, success=False, pipe=False)

    if not ALIAS_NAME_REGEX.match(name):
        return translations.alias_invalid_name.format_response(ctx, success=False, pipe=False)
    alias = await Alias.get_or_none(user=ctx.user, name=name)
    if alias:
        return translations.Add.alias_name_conflict.format_response(ctx, name, success=False, pipe=False)

    command_check = parse_command_by_name(ctx, command_)
    if not command_check:
        return translations.Add.command_dont_exist.format_response(ctx, command_, success=False, pipe=False)
    rest = [arg for arg in rest if arg]
    alias = await Alias.save_alias(ctx, name, command_check, command_, rest)
    return translations.Add.alias_crated.format_response(ctx, alias.name, pipe=False)


async def check_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    first_name, second_name, *rest = chain(args, repeat(None, 2))
    # TODO: Make so he create a bin.mrchuw.com.br with all the alias from the user.
    if not first_name and not second_name:
        username = ctx.author.name
        return translations.Check.user_alias_list.format_response(ctx, username, success=False, pipe=False)

    target_aliases = []
    aliases = await Alias.filter(channel__isnull=True, user=ctx.user).values_list('name', flat=True)

    target_user = await User.get_or_none(name=first_name)
    if target_user:
        target_aliases = await Alias.filter(channel__isnull=True, user=target_user).values_list('name', flat=True)

    if target_aliases == [] and first_name not in aliases:
        return translations.Check.no_alias_found.format_response(ctx, second_name, target_user.name, success=False, pipe=False)
    elif target_aliases == [] and first_name in aliases:
        user = ctx.user
        alias_name = first_name
        mention = translations.mention(ctx, user, user.name)
    elif target_aliases and first_name not in aliases:
        mention = translations.mention(ctx, target_user, ctx.author.name)
        url = "TODO"
        # TODO: The same thing of the first if.
        return translations.Check.list_of_alias_of.format_response(ctx, mention, url, pipe=False)
    else:
        url1 = "TODO from the user."
        url2 = "TODO from the user that has the same name as the alias."
        # TODO: Here the case is if some one has the same name as a alias.
        return translations.Check.list_of_special_case.format_response(ctx, first_name, url1, url2, pipe=False)

    if second_name:
        user = await User.get_or_none(name=first_name)
        if not user:
            return translations.user_not_found.format_response(ctx, first_name, success=False, pipe=False)

        alias_name = second_name
        mention = translations.mention(ctx, user, ctx.author.name)

    alias = await Alias.filter(user_id=user.id, name=alias_name).first().prefetch_related("parent")

    if not alias:
        return translations.Check.alias_not_found.format_response(ctx, mention, alias_name, success=False, pipe=False)

    appendix = ""
    if not alias.command and not alias.parent:  # NOQA
        return translations.Check.alias_deleted.format_response(ctx, mention, success=False, pipe=False)

    elif not alias.command and alias.parent:  # NOQA
        alias = await Alias.get(id=alias.parent.id)
        original_user = await User.get(id=alias.user.id)
        appendix = translations.Check.appendix.format(alias.name, original_user.name)

    message = f"{alias.invocation} {' '.join(alias.arguments)}"
    if alias.arguments:
        message = translations.Check.message.format(appendix, mention, alias_name, alias.invocation,
                                                    ' '.join(alias.arguments)
                                                    )
    # TODO: Here the case is if some one has the same name as a alias.
    url = "TODO"

    return translations.Check.final_message.format_response(ctx, message, url, pipe=False)


async def copy_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    target_user_name, target_alias_name = chain(args, repeat(None, 2))

    if not target_user_name:
        return translations.user_not_found.format_response(ctx, success=False, pipe=False)
    if not target_alias_name:
        return translations.Copy.alias_not_provided.format_response(ctx, success=False, pipe=False)
    if not ALIAS_NAME_REGEX.match(target_alias_name):
        return translations.Copy.target_alias_invalid_name.format_response(ctx, success=False, pipe=False)

    target_user = await User.get_or_none(name=target_user_name)
    if not target_user:
        return translations.user_not_found.format_response(ctx, target_user_name, success=False, pipe=False)

    target_alias = await Alias.filter(channel__isnull=True, user=target_user, name=target_alias_name).first()
    if target_alias.command is None:  # NOQA
        # TODO: See if this is point to the right user.
        return translations.Copy.link_to_a_link.format_response(ctx, ctx.prefix, target_user.name, target_alias_name,
                                                                success=False,
                                                                pipe=False)

    new_alias = await Alias.create(user_id=ctx.author.id, channel_id=None, name=target_alias_name,
            command=target_alias.command,  # NOQA
            invocation=target_alias.invocation, arguments=target_alias.arguments, parent_id=target_alias.id, )

    return translations.Copy.copy_success.format_response(ctx, new_alias.name, pipe=False)


async def describe_alias(ctx: Context, args: tuple):  # NOQA
    translations = ctx.translations.Alias
    if not args:
        return translations.Describe.no_args_to_parse.format_response(ctx, ctx.prefix, success=False, pipe=False)

    name, *rest = chain(args, repeat(None, 2))
    alias = await Alias.filter(user=ctx.user, name=name).first()

    if not alias:
        return translations.dont_have_alias.format_response(ctx, name, success=False, pipe=False)

    description = " ".join(rest).strip()
    if not description or description.lower() == "none":
        alias.description = None
        await alias.save()
        return translations.Describe.description_reseted.format_response(ctx, name, pipe=False)
    else:
        alias.description = description
        await alias.save()
        return translations.Describe.description_updated.format_response(ctx, name, pipe=False)


async def edit_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    if len(args) < 2:
        return translations.Edit.no_args_provided.format_response(ctx, success=False, pipe=False)

    name, command_, *rest = chain(args, repeat(None, 2))
    command_check = parse_command_by_name(ctx, command_)

    if not command_check:
        return translations.Edit.command_dont_exist.format_response(ctx, command_, success=False, pipe=False)

    alias = await Alias.filter(user=ctx.user, name=name).first()
    if not alias:
        return translations.dont_have_alias.format_response(ctx, name, success=False, pipe=False)

    if alias.command is None:  # NOQA
        return translations.Edit.edit_link.format_response(ctx, args, success=False, pipe=False)

    alias.command = command_check.name
    alias.invocation = command_
    alias.arguments = rest if rest else None

    await alias.save()
    return translations.Edit.edit_success.format_response(ctx, alias.name, pipe=False)


async def link_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    if len(args) < 2:
        return translations.Link.link_no_args.format_response(ctx, success=False, pipe=False)

    user_name, alias_name, custom_link_name, *rest = chain(args, repeat(None, 2))
    name = custom_link_name or alias_name

    existing_alias = await Alias.filter(user=ctx.user, name=name).first()

    if existing_alias:
        return translations.Link.alias_name_already_exists.format_response(ctx, success=False, pipe=False)

    target_user_data = await User.get_or_none(name=user_name)
    if not target_user_data:
        return translations.user_not_found.format_response(ctx, user_name, success=False, pipe=False)

    target_alias = await (
        Alias.filter(channel__isnull=True, user=target_user_data, name=name).first().prefetch_related("parent"))
    appendix = ""

    if not target_alias:
        return translations.Link.user_dont_has_alias.format_response(ctx, name, success=False, pipe=False)
    elif target_alias.command is None and target_alias.parent_id is not None:  # NOQA
        # Se o alias já é um link, usa o alias original
        # target_alias = await Alias.get_or_none(id=target_alias.parent)
        target_alias: Alias = await target_alias.parent
        await target_alias.fetch_related("user")

        original_user = await target_alias.user
        appendix = translations.Link.appendix_link.format(target_alias.name, original_user.name)
        target_alias.name = alias_name

    elif not ALIAS_NAME_REGEX.match(target_alias.name):
        return translations.Link.link_with_invalid_name.format_response(ctx, translations.alias_invalid_name,
                                                                        success=False,
                                                                        pipe=False)

    await Alias.create(user=ctx.user, channel=None, name=name, command=None, invocation=None, arguments=None,
                       description=target_alias.description, parent=target_alias
                       )

    name_string = translations.Link.link_name_string.format(custom_link_name) if (
            custom_link_name and custom_link_name != target_alias.name) else ""

    return translations.Link.link_success.format_response(ctx, name_string, appendix, pipe=False)


async def remove_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    if len(args) < 2:
        return translations.Remove.no_alias_name_provided.format_response(ctx, success=False, pipe=False)
    name, *rest = chain(args, repeat(None, 2))
    alias = await Alias.get_or_none(user=ctx.user, name=name)
    if not alias:
        return translations.dont_have_alias.format_response(ctx, name, success=False, pipe=False)
    alias.deleted = True
    await alias.save()
    return translations.Remove.alias_removed.format_response(ctx, name, pipe=False)


async def rename_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    if len(args) < 2:
        return translations.Rename.no_name_provided.format_response(ctx, success=False, pipe=False)
    old_alias_name, new_alias_name, *rest = chain(args, repeat(None, 2))
    if not ALIAS_NAME_REGEX.match(new_alias_name):
        return translations.alias_invalid_name.format_response(ctx, translations.alias_invalid_name, success=False, pipe=False)
    old_alias = await Alias.get_or_none(user=ctx.user, name=old_alias_name)

    if not old_alias:
        return translations.dont_have_alias.format_response(ctx, old_alias_name, success=False, pipe=False)
    existing_alias = await Alias.filter(user=ctx.user, name=new_alias_name).first()
    if existing_alias:
        return translations.Rename.alias_already_exists.format_response(ctx, new_alias_name, success=False, pipe=False)

    old_alias.name = new_alias_name
    await old_alias.save()
    return translations.Rename.alias_renamed.format_response(ctx, old_alias_name, new_alias_name, pipe=False)
