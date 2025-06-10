# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import re
from itertools import chain, repeat
from typing import List, NamedTuple, TYPE_CHECKING

from twitchio.ext.commands import GuardFailure

from bot.ext import Command, commands, Context
from bot.models import Alias, User
from bot.translations import BaseDecorators, BaseTranslations, Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    TAlias = BaseTranslations.Alias()  # NOQA


class ParsedCommand(NamedTuple):
    command: commands.Command | None
    guard_result: None | GuardFailure
    trigger_name: None | str


ALIAS_NAME_REGEX = re.compile(
    r"^[-\w\u00a9\u00ae\u2000-\u3300\ud83c\ud000-\udfff\ud83d\ud000-\udfff\ud83e\ud000-\udfff]{2,30}$"
)


class AliasCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: Context) -> bool:  # NOQA
        return True

    @commands.base_decorator(BaseDecorators.Alias)
    @commands.group(name="alias")
    @commands.cooldown(rate=10, per=10, key=commands.BucketType.user)
    async def alias(self, ctx: Context, *, args) -> Response:  # NOQA
        await ctx.simple_response(ctx, "Shush")
        return ctx.user.translations.Admin.Nada.vazio.format_response(ctx, success=False)

    @alias.command(name="add")
    async def add_command(self, ctx: Context, *args):
        translations = ctx.user.translations.Alias
        name, command_string, *rest = chain(args, repeat(None, 2))
        if not command_string:
            return translations.Add.no_command_to_add.format_response(ctx, ctx.prefix, success=False, pipe=False)

        if not ALIAS_NAME_REGEX.match(name):
            return translations.alias_invalid_name.format_response(ctx, success=False, pipe=False)

        alias = await Alias.get_alias(ctx=ctx, name=name)
        if alias:
            return translations.Add.alias_name_conflict.format_response(ctx, name, success=False, pipe=False)

        string_join = " ".join(value for value in rest if value)
        result = await parse_commands(ctx, f"{command_string} {string_join}")
        if not result.command:
            return translations.Add.command_dont_exist.format_response(ctx, command_string, success=False, pipe=False)

        if result.guard_result:
            return ctx.user.translations.Exceptions.guard_caught.format_response(
                ctx, result.trigger_name, result.guard_result, ctx.bot.dev_name, success=False, pipe=False
            )

        rest = [arg for arg in rest if arg]
        alias = await Alias.create_cached(
            ctx=ctx, name=name, command=result.command, invocation=command_string, arguments=rest
        )
        return translations.Add.alias_created.format_response(ctx, alias.name, pipe=False)

    @alias.command(name="check", aliases=["list"])
    async def check_alias(self, ctx: Context, *args):
        translations = ctx.user.translations.Alias
        first_name, second_name, *rest = chain(args, repeat(None, 2))

        # no arguments: list own aliases
        if not first_name and not second_name:
            return await handle_list_all(ctx, translations)

        # prepare lists
        aliases = await Alias.list_alias(ctx, user=ctx.user)
        aliases_flat = flatten_alias_names(aliases)

        # target user if first name
        target_user = await User.get_user_or_none(ctx, name=first_name)
        target_aliases = []
        target_aliases_flat = []
        if target_user:
            target_aliases = await Alias.all_prefetch(ctx=ctx, user=target_user)
            target_aliases_flat = flatten_alias_names(target_aliases)

        # various conditions
        if not target_aliases_flat and first_name not in aliases_flat and not second_name:
            return translations.user_has_no_alias.format_response(ctx, target_user.name, success=False, pipe=False)
        if not target_aliases_flat and first_name in aliases_flat and not second_name:
            user = ctx.user
            alias_name = first_name
            # will lookup alias below
        elif target_aliases_flat and first_name not in aliases_flat and not second_name:
            return await handle_target_list(ctx, target_user, translations)
        elif target_aliases_flat and first_name in aliases_flat and not second_name:
            return await handle_special_case(ctx, translations, aliases, target_aliases, first_name, target_user)

        # second name provided: lookup specific
        if second_name:
            user = await User.get_user_or_none(ctx, name=first_name)
            if not user:
                exception = ctx.user.translations.Exceptions
                return exception.user_not_found_name.format_response(ctx, first_name, success=False, pipe=False)
            alias_name = second_name

        return await handle_alias_lookup(ctx, user, alias_name, translations)  # NOQA

    @alias.command(name="copy")
    async def copy_alias(self, ctx: Context, *args):
        translations = ctx.user.translations.Alias
        exception = ctx.user.translations.Exceptions
        target_user_name, target_alias_name, *rest = chain(args, repeat(None, 2))
        new_name = rest[0] if (rest := [arg for arg in rest if arg]) else None
        if not target_user_name:
            return exception.user_not_provided.format_response(ctx, success=False, pipe=False)
        if not target_alias_name:
            return translations.Copy.alias_not_provided.format_response(ctx, success=False, pipe=False)
        if not ALIAS_NAME_REGEX.match(target_alias_name):
            return translations.Copy.target_alias_invalid_name.format_response(ctx, success=False, pipe=False)
        alias = await Alias.filter_cached(ctx=ctx, alias_name=target_alias_name)
        if alias:
            return translations.Add.alias_name_conflict.format_response(
                ctx, target_alias_name, success=False, pipe=False
            )

        target_user = await User.get_user_or_none(ctx, name=target_user_name)
        if not target_user:
            return exception.user_not_found_name.format_response(ctx, target_user_name, success=False, pipe=False)
        target_alias = await Alias.filter_first_prefetch(ctx=ctx, user=target_user, alias_name=target_alias_name)
        if target_alias is None:
            return translations.Copy.no_alias_found.format_response(
                ctx, target_alias_name, target_user.name, success=False, pipe=False
            )

        if target_alias.command is None and target_alias.parent:
            original_user = await User.get_user(ctx, user_id=target_alias.parent.user_id)
            return translations.Copy.link_to_a_link.format_response(
                ctx, ctx.prefix, original_user.name, target_alias.parent.name, success=False, pipe=False
            )
        else:
            new_alias = await Alias.create_cached(
                ctx=ctx,
                name=new_name or target_alias_name,
                command=target_alias.command,  # NOQA
                invocation=target_alias.invocation,
                arguments=target_alias.arguments,
                parent=target_alias,
            )
        if new_name:
            return translations.Copy.copy_success.format_response(ctx, target_alias_name, new_alias.name, pipe=False)
        return translations.Copy.copy_success.format_response(ctx, new_alias.name, pipe=False)

    @alias.command(name="describe")
    async def describe_alias(self, ctx: Context, *args):
        translations = ctx.user.translations.Alias
        if not args:
            return translations.Describe.no_args_to_parse.format_response(ctx, ctx.prefix, success=False, pipe=False)

        name, *rest = chain(args, repeat(None, 2))
        rest = [arg for arg in rest if arg]
        alias = await Alias.filter_cached(ctx=ctx, alias_name=name).first()

        if not alias:
            return translations.dont_have_alias.format_response(ctx, name, success=False, pipe=False)

        description = " ".join(rest).strip()
        if not description or description.lower() == "none":
            alias.description = None
            await alias.save()
            return translations.Describe.description_reverted.format_response(ctx, name, pipe=False)
        else:
            alias.description = description
            await alias.save()
            return translations.Describe.description_updated.format_response(ctx, name, pipe=False)

    @alias.command(name="edit")
    async def edit_alias(self, ctx: Context, *args):
        translations = ctx.user.translations.Alias
        if len(args) < 2:
            return translations.Edit.no_args_provided.format_response(ctx, success=False, pipe=False)

        name, command_, *rest = chain(args, repeat(None, 2))
        rest = [arg for arg in rest if arg]
        command_check = await parse_command_by_name(ctx, command_)

        if not command_check.command:
            return translations.Edit.command_dont_exist.format_response(ctx, command_, success=False, pipe=False)
        if command_check.guard_result:
            return ctx.user.translations.Exceptions.guard_caught.format_response(
                ctx, command_check.trigger_name, command_check.guard_result, ctx.bot.dev_name, success=False, pipe=False
            )

        alias = await Alias.filter_cached(ctx=ctx, alias_name=name)
        if not alias:
            return translations.dont_have_alias.format_response(ctx, name, success=False, pipe=False)

        if alias.command is None:  # NOQA
            return translations.Edit.edit_link.format_response(ctx, args, success=False, pipe=False)

        alias.command = command_check.command.name
        alias.invocation = command_
        alias.arguments = rest or None

        await alias.save()
        return translations.Edit.edit_success.format_response(ctx, alias.name, pipe=False)

    @alias.command(name="link")
    async def link_alias(self, ctx: Context, *args):
        translations = ctx.user.translations.Alias
        exception = ctx.user.translations.Exceptions
        link_to_link = False
        original_user = None
        if len(args) < 2:
            return translations.Link.link_no_args.format_response(ctx, ctx.prefix, success=False, pipe=False)

        user_name, alias_name, custom_link_name, *rest = chain(args, repeat(None, 2))
        name = custom_link_name or alias_name
        existing_alias = await Alias.filter_cached(ctx=ctx, alias_name=name)

        if existing_alias and not custom_link_name:
            return translations.Add.alias_name_conflict.format_response(ctx, alias_name, success=False, pipe=False)

        if existing_alias and existing_alias.name == custom_link_name:
            return translations.Link.alias_name_already_exists.format_response(
                ctx, alias_name, success=False, pipe=False
            )

        target_user_data = await User.get_or_none(name=user_name)
        if not target_user_data:
            return exception.user_not_found_name.format_response(ctx, user_name, success=False, pipe=False)
        target_alias = await Alias.filter_cached(ctx, user=target_user_data, alias_name=alias_name).first_prefetch()

        if not target_alias or (not target_alias.command and not target_alias.parent):
            return translations.Link.user_dont_has_alias.format_response(ctx, alias_name, success=False, pipe=False)

        elif target_alias.command is None and target_alias.parent is not None:
            target_alias: Alias = await target_alias.parent
            await target_alias.fetch_related("user")
            original_user = await target_alias.user
            target_alias.name = alias_name
            link_to_link = True

        elif not ALIAS_NAME_REGEX.match(target_alias.name):
            return translations.Link.link_to_with_invalid_name.format_response(
                ctx, translations.alias_invalid_name, success=False, pipe=False
            )
        elif custom_link_name and not ALIAS_NAME_REGEX.match(custom_link_name):
            return translations.Link.link_to_with_invalid_name.format_response(
                ctx, custom_link_name, success=False, pipe=False
            )

        await Alias.link_alias(ctx, name, target_alias)

        name_string = (
            translations.Link.link_name_string.format(custom_link_name)
            if (custom_link_name and custom_link_name != target_alias.name)
            else "."
        )

        if link_to_link:
            return translations.Link.link_to_link.format_response(
                ctx, target_alias.name, original_user.name, name_string, pipe=False
            )

        return translations.Link.link_success.format_response(ctx, name_string, pipe=False)

    @alias.command(name="remove")
    async def remove_alias(self, ctx: Context, *args):
        translations = ctx.user.translations.Alias
        if not args:
            return translations.Remove.no_alias_name_provided.format_response(ctx, success=False, pipe=False)
        name, *rest = chain(args, repeat(None, 2))
        alias = await Alias.get_or_none(user=ctx.user, name=name)
        if not alias:
            return translations.dont_have_alias.format_response(ctx, name, success=False, pipe=False)
        alias.deleted = True
        await alias.save()
        return translations.Remove.alias_removed.format_response(ctx, name, pipe=False)

    @alias.command(name="rename")
    async def rename_alias(self, ctx: Context, *args):
        translations = ctx.user.translations.Alias
        if len(args) < 2:
            return translations.Rename.no_name_provided.format_response(ctx, success=False, pipe=False)
        old_alias_name, new_alias_name, *rest = chain(args, repeat(None, 2))
        if not ALIAS_NAME_REGEX.match(new_alias_name):
            return translations.alias_invalid_name.format_response(
                ctx, translations.alias_invalid_name, success=False, pipe=False
            )
        old_alias = await Alias.filter_cached(ctx=ctx, alias_name=old_alias_name).first()

        if not old_alias:
            return translations.dont_have_alias.format_response(ctx, old_alias_name, success=False, pipe=False)
        existing_alias = await Alias.filter_cached(ctx=ctx, alias_name=new_alias_name).first()
        if existing_alias:
            return translations.Rename.alias_already_exists.format_response(
                ctx, new_alias_name, success=False, pipe=False
            )

        old_alias.name = new_alias_name
        await old_alias.save()
        return translations.Rename.alias_renamed.format_response(ctx, old_alias_name, new_alias_name, pipe=False)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(AliasCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA


# region Not need now.


async def run_guards(command: Command, ctx: Context):
    guards = command.all_guards
    for guard in guards:
        try:
            result = guard(ctx, ctx)
            if asyncio.iscoroutine(result):
                await result
        except Exception as e:
            return str(e) or type(e).__name__
    return None


async def parse_commands(ctx: Context, string: str):
    if "|" in string:
        return await parse_pipe_commands(ctx, string)
    return await parse_command_by_name(ctx, string)


async def parse_command_by_name(ctx: Context, string: str) -> ParsedCommand:
    message = ctx.message
    message.text = f"{ctx.prefix}{string}"
    cctx = await ctx.bot.get_context(message)
    if not cctx.command:
        return ParsedCommand(cctx.command, None, None)
    return ParsedCommand(cctx.command, await run_guards(cctx.command, ctx), cctx.command.name)


async def parse_pipe_commands(ctx: Context, string: str) -> ParsedCommand:
    command_list = string.split(" | ")
    first_command = await parse_command_by_name(ctx, command_list[0])
    for command in command_list:
        result = await parse_command_by_name(ctx, command)
        if result.guard_result:
            return result
    return ParsedCommand(first_command.command, None, None)


# TODO: Make the api tests
async def upload_alias(ctx: Context, aliases: list[Alias], table_name: str):
    translations = ctx.user.translations.Alias
    alias_table_headers = translations.alias_table_headers
    alias_table_replaces = translations.alias_table_replaces
    alias_table_list = []

    for alias in aliases:
        name = alias.name
        if alias.parent:
            alias = await alias.parent
        description = alias.description or alias_table_replaces[0]
        invocation = alias.invocation or ""
        arguments = " ".join(alias.arguments) or None
        if arguments and "|" in arguments:
            arguments = arguments.replace("|", r"\|")
        parent_name = alias_table_replaces[2]
        if ctx.user.id != alias.user_id:
            parent_name = await User.get(id=alias.user_id) or ""
        updated_at = alias.updated_at.strftime(ctx.user.translations.SupportTools.TimeTools.strftime)
        created_at = alias.created_at.strftime(ctx.user.translations.SupportTools.TimeTools.strftime)
        alias_table_list.append(
            {
                alias_table_headers[0]: name,
                alias_table_headers[1]: description,
                alias_table_headers[2]: invocation,
                alias_table_headers[3]: arguments,
                alias_table_headers[4]: parent_name,
                alias_table_headers[5]: updated_at,
                alias_table_headers[6]: created_at,
            }
        )

    columns = alias_table_list[0].keys()
    max_lens = {
        column: max(len(str(item[column])) for item in alias_table_list + [{column: column}]) for column in columns
    }

    header = "| " + " | ".join(column.center(max_lens[column]) for column in columns) + " |"
    separator = "| " + " | ".join(":" + "-".ljust(max_lens[column] - 1, "-") + ":" for column in columns) + " |"
    lines = [
        "| " + " | ".join(str(item[column]).center(max_lens[column]) for column in columns) + " |"
        for item in alias_table_list
    ]

    markdown_table = "\n".join([header, separator] + lines)

    data = {"markdown": markdown_table, "table_name": table_name}

    alias_cached_session = ctx.bot.SessionsCaches.AliasCachedSession.session
    response_url = await ctx.bot.UploadThings.upload_alias(data=data, session=alias_cached_session)

    return await ctx.bot.UploadThings.shortener(response_url, ["aliases"], ctx.bot, alias_cached_session)


# endregion


# region Check functions


async def handle_list_all(ctx: Context, translations):
    aliases = await Alias.all_prefetch(ctx=ctx, user=ctx.user)
    names = flatten_alias_names(aliases)
    url = await upload_alias(ctx, aliases, translations.alias_table_name.format(ctx.author.display_name))
    return translations.Check.user_alias_list.format_response(ctx, ", ".join(names), url, success=False, pipe=False)


def flatten_alias_names(aliases) -> List[str]:
    return [alias.name for alias in aliases]


def build_mention(ctx_user: User, author_name: str, target_name: str):
    if target_name == author_name:
        return ctx_user.translations.SupportTools.LanguageContext.mention
    return f"@{target_name}"


async def handle_target_list(ctx: Context, target_user, translations: TAlias):
    target_aliases = await Alias.all_prefetch(ctx=ctx, user=target_user)
    mention = build_mention(ctx.user, ctx.author.name, target_user.name)
    url = await upload_alias(ctx, target_aliases, translations.alias_table_name.format(mention))
    return translations.Check.list_of_alias_of.format_response(ctx, mention, url, pipe=False)


async def handle_special_case(
    ctx: Context, translations: TAlias, aliases, target_aliases, first_name: str, target_user
):
    url1 = await upload_alias(ctx, aliases, translations.alias_table_name.format(ctx.author.display_name))
    url2 = await upload_alias(ctx, target_aliases, translations.alias_table_name.format(target_user.name))
    return translations.Check.list_of_special_case.format_response(ctx, first_name, url1, url2, pipe=False)


async def handle_alias_lookup(ctx: Context, user, alias_name: str, translations: TAlias):
    alias = await Alias.filter_cached(ctx=ctx, user=user, alias_name=alias_name).first().prefetch_related()
    if not alias:
        mention = build_mention(ctx.user, ctx.author.name, user.name)
        return translations.Check.alias_not_found.format_response(ctx, mention, alias_name, success=False, pipe=False)

    if not alias.command and not alias.parent:
        return translations.Check.alias_deleted.format_response(ctx, alias_name, success=False, pipe=False)

    url = await upload_alias(ctx, [alias], translations.alias_table_name.format(user.name))
    invocation = f"{alias.invocation} {' '.join(alias.arguments)}"

    if not alias.command and alias.parent:
        parent_alias = await Alias.get(id=alias.parent.id, deleted=False)
        original_user = await User.get(id=parent_alias.user.id)
        return translations.Check.appendix_message.format_response(
            ctx,
            parent_alias.name,
            original_user.name,
            invocation,
            url,
            pipe=False,
        )

    return translations.Check.normal_message.format_response(ctx, alias.name, invocation, url, pipe=False)


# endregion
