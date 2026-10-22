from __future__ import annotations

import asyncio
import re
from typing import TYPE_CHECKING, NamedTuple

from twitchio.ext.commands import GuardFailure

from bot.ext import Command, Context, Response, commands
from bot.models import Alias, User
from bot.utils import SessionsCaches, StringTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ParsedCommand(NamedTuple):
    command: commands.Command | commands.Group | None
    guard_result: GuardFailure | str | None
    trigger_name: str | None


ALIAS_NAME_REGEX: re.Pattern = re.compile(
    r"^[-\w\u00a9\u00ae\u2000-\u3300\ud83c\ud000-\udfff\ud83d\ud000-\udfff\ud83e\ud000-\udfff]{2,30}$"
)


class AliasCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.UploadThings: UploadThings = UploadThings(bot)
        self.StringTools: StringTools = StringTools()

    @commands.group(name="alias")
    @commands.cooldown(rate=10, per=10, key=commands.BucketType.user)
    async def alias(self, ctx: Context, *, args) -> Response:  # NOQA
        await ctx.simple_response(ctx, "Shush")
        return self.translations.Exceptions.empty(ctx, success=False)

    @alias.command(name="add", pipeble=False)
    async def add_command(self, ctx: Context, *args: str) -> Response:
        translations = self.translations
        name, command_string, rest = self.StringTools.unpack_dynamic(args, 2)
        if not command_string:
            return translations.Add.no_command_to_add(ctx.prefix)
        if not name:
            return translations.Add.error_no_name()

        if not ALIAS_NAME_REGEX.match(name):
            return translations.Alias.alias_invalid_name()
        alias = await Alias.get_alias(ctx=ctx, name=name)
        if alias:
            return translations.Add.alias_name_conflict(name)

        string_join = " ".join(value for value in rest if value)
        result = await parse_commands(ctx, f"{command_string} {string_join}")
        if not result.command:
            return translations.Add.command_dont_exist(command_string)

        if result.guard_result and result.trigger_name:
            return translations.Exceptions.guard_caught(
                result.trigger_name, result.guard_result, ctx.bot.dev_user.display_name or ""
            )

        rest = [arg for arg in rest if arg]
        alias = await Alias.create_cached(
            ctx=ctx, name=name, command=result.command, invocation=command_string, arguments=rest
        )
        return translations.Add.alias_created(alias.name)

    @alias.command(name="check", aliases=["list"], pipeble=False)
    async def check_alias(self, ctx: Context, *args: str) -> Response:
        translations = self.translations
        first_name, second_name, _ = self.StringTools.unpack_dynamic(args, n=2)

        # no arguments: list own aliases
        if not first_name and not second_name:
            return await handle_list_all(ctx, translations, self)

        if not first_name:
            return translations.Check.no_first_name()

        # prepare lists
        aliases = await Alias.list_alias(ctx, user=ctx.user)
        aliases_flat = flatten_alias_names(aliases)

        # target user if first name
        target_user = await User.get_user_or_none(ctx, name=first_name, translations=self.translations)
        target_aliases = []
        target_aliases_flat = []
        if target_user:
            target_aliases = await Alias.all_prefetch(ctx=ctx, user=target_user)
            target_aliases_flat = flatten_alias_names(target_aliases)

        # various conditions
        if not target_aliases_flat and first_name not in aliases_flat and not second_name:
            return translations.Alias.user_has_no_alias(target_user.name)
        if not target_aliases_flat and first_name in aliases_flat and not second_name:
            user = ctx.user
            alias_name = first_name
            # will look up alias below
        elif target_aliases_flat and first_name not in aliases_flat and not second_name:
            return await handle_target_list(ctx, target_user, translations, self)
        elif target_aliases_flat and first_name in aliases_flat and not second_name:
            return await handle_special_case(ctx, translations, aliases, target_aliases, first_name, target_user, self)

        # second name provided: lookup specific
        if second_name:
            user = await User.get_user_or_none(ctx, name=first_name, translations=self.translations)
            if not user:
                return translations.Exceptions.user_not_found_name(first_name)
            alias_name = second_name

        return await handle_alias_lookup(ctx, user, alias_name, translations, self)  # NOQA

    @alias.command(name="copy", pipeble=False)
    async def copy_alias(self, ctx: Context, *args: str):
        translations = self.translations
        exception = self.translations.Exceptions
        target_user_name, target_alias_name, rest = self.StringTools.unpack_dynamic(args, 2)
        new_name = rest[0] if (rest := [arg for arg in rest if arg]) else None
        if not target_user_name:
            return exception.user_not_provided(ctx)
        if not target_alias_name:
            return translations.Copy.alias_not_provided()
        if not ALIAS_NAME_REGEX.match(target_alias_name):
            return translations.Copy.target_alias_invalid_name()
        alias = await Alias.filter_cached(ctx=ctx, alias_name=target_alias_name)
        if alias:
            return translations.Add.alias_name_conflict(target_alias_name)

        target_user = await User.get_user_or_none(ctx, name=target_user_name, translations=self.translations)
        if not target_user:
            return exception.user_not_found_name(target_user_name)
        target_alias = await Alias.filter_first_prefetch(ctx=ctx, user=target_user, alias_name=target_alias_name)
        if target_alias is None:
            return translations.Copy.no_alias_found(target_alias_name, target_user.name)

        if target_alias.command is None and target_alias.parent:
            original_user = await User.get_user(
                ctx, translations=self.translations, user_id=target_alias.parent.user_id
            )
            return translations.Copy.link_to_a_link(ctx.prefix, original_user.name, target_alias.parent.name)
        else:
            if command := ctx.bot.get_command(target_alias.command or ""):
                new_alias = await Alias.create_cached(
                    ctx=ctx,
                    name=new_name or target_alias_name,
                    command=command,  # NOQA
                    invocation=target_alias.invocation,
                    arguments=target_alias.arguments,
                    parent=target_alias,
                )
            else:
                return translations.Copy.copy_success("asdf")
        if new_name:
            return translations.Copy.copy_with_name_of(target_alias_name, new_alias.name)
        return translations.Copy.copy_success(new_alias.name)

    @alias.command(name="describe", pipeble=False)
    async def describe_alias(self, ctx: Context, *args: str):
        translations = self.translations
        if not args:
            return translations.Describe.no_args_to_parse(ctx.prefix)
        name, rest = self.StringTools.unpack_dynamic(args, 1)
        if not name:
            return translations.Describe.no_args_to_parse(ctx.prefix)

        rest = [arg for arg in rest if arg]
        alias = await Alias.filter_first_prefetch(ctx=ctx, alias_name=name)

        if not alias:
            return translations.Alias.dont_have_alias(name)

        description: str = " ".join(rest).strip()
        if not description or description.lower() == "none":
            alias.description = None
            await alias.save()
            return translations.Describe.description_reverted(name)
        else:
            alias.description = description
            await alias.save()
            return translations.Describe.description_updated(name)

    @alias.command(name="edit", pipeble=False)
    async def edit_alias(self, ctx: Context, *args: str):
        translations = self.translations
        if len(args) < 2:
            return translations.Edit.no_args_provided()

        name, command_, rest = self.StringTools.unpack_dynamic(args, 2)

        if not name or not command_:
            return translations.Edit.no_args_provided()
        rest = [arg for arg in rest if arg]
        command_check = await parse_command_by_name(ctx, command_)

        if not command_check.command:
            return translations.Edit.command_dont_exist(command_)
        if command_check.guard_result and command_check.trigger_name:
            return self.translations.Exceptions.guard_caught(
                command_check.trigger_name, command_check.guard_result, ctx.bot.dev_user.display_name or ""
            )
        alias = await Alias.filter_first(ctx=ctx, alias_name=name)
        if not alias:
            return translations.Alias.dont_have_alias(name)

        if alias.command is None:  # NOQA
            return translations.Edit.edit_link()

        alias.command = command_check.command.name
        alias.invocation = command_
        alias.arguments = rest or None

        await alias.save()
        return translations.Edit.edit_success(alias.name)

    @alias.command(name="link", pipeble=False)
    async def link_alias(self, ctx: Context, *args: str):
        translations = self.translations
        exception = self.translations.Exceptions
        link_to_link = False
        original_user = None
        user_name, alias_name, custom_link_name, _ = self.StringTools.unpack_dynamic(args, 3)
        if len(args) < 2:
            return translations.Link.link_no_args(ctx.prefix)
        if not user_name or not alias_name:
            return translations.Link.link_no_args(ctx.prefix)

        name = custom_link_name or alias_name
        existing_alias = await Alias.filter_first(ctx=ctx, alias_name=name)

        if existing_alias and not custom_link_name:
            return translations.Add.alias_name_conflict(alias_name)

        if existing_alias and existing_alias.name == custom_link_name:
            return translations.Link.alias_name_already_exists(alias_name)

        target_user_data = await User.get_or_none(name=user_name)
        if not target_user_data:
            return exception.user_not_found_name(user_name)

        target_alias = await Alias.filter_first(ctx, alias_name=alias_name, user=target_user_data)

        if not target_alias or (not target_alias.command and not target_alias.parent):
            return translations.Link.user_dont_has_alias(alias_name)

        elif target_alias.command is None and target_alias.parent is not None:
            target_alias = await target_alias.parent
            await target_alias.fetch_related("user")
            original_user = await target_alias.user
            target_alias.name = alias_name
            link_to_link = True

        elif not ALIAS_NAME_REGEX.match(target_alias.name):
            return translations.Link.link_to_with_invalid_name(target_alias.name)
        elif custom_link_name and not ALIAS_NAME_REGEX.match(custom_link_name):
            return translations.Link.link_to_with_invalid_name(custom_link_name)

        await Alias.link_alias(ctx, name, target_alias)

        name_string = (
            translations.Link.link_name_string(custom_link_name or "")
            if (custom_link_name and custom_link_name != target_alias.name)
            else ""
        )

        if link_to_link:
            return translations.Link.link_to_link(target_alias.name, original_user.name, name_string)

        return translations.Link.link_success(name_string)

    @alias.command(name="remove", pipeble=False)
    async def remove_alias(self, ctx: Context, *args: str):
        name, _ = self.StringTools.unpack_dynamic(args, 1)
        if not args or not name:
            return self.translations.Remove.no_alias_name_provided()
        alias = await Alias.get_or_none(user=ctx.user, name=name)
        if not alias:
            return self.translations.Alias.dont_have_alias(name)
        alias.deleted = True
        await alias.save()
        return self.translations.Remove.alias_removed(name)

    @alias.command(name="rename", pipeble=False)
    async def rename_alias(self, ctx: Context, *args: str):
        old_alias_name, new_alias_name, _ = self.StringTools.unpack_dynamic(args, 2)
        if len(args) < 2 or not old_alias_name or not new_alias_name:
            return self.translations.Rename.no_name_provided()

        if not ALIAS_NAME_REGEX.match(new_alias_name):
            return self.translations.Alias.alias_invalid_name()
        old_alias = await Alias.filter_first(ctx=ctx, alias_name=old_alias_name)

        if not old_alias:
            return self.translations.Alias.dont_have_alias(old_alias_name)
        existing_alias = await Alias.filter_first(ctx=ctx, alias_name=new_alias_name)
        if existing_alias:
            return self.translations.Rename.alias_already_exists(new_alias_name)

        old_alias.name = new_alias_name
        await old_alias.save()
        return self.translations.Rename.alias_renamed(old_alias_name, new_alias_name)

    @alias.command(name="extras", pipeble=False)
    async def extras_alias(self, ctx: Context):  # NOQA
        return None


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


async def parse_commands(ctx: Context, string: str) -> ParsedCommand:
    if "|" in string:
        return await parse_pipe_commands(ctx, string)
    return await parse_command_by_name(ctx, string)


async def parse_command_by_name(ctx: Context, string: str) -> ParsedCommand:
    command_text = f"{ctx.prefix}{string}"
    mock_ctx = await ctx.bot.ContextHandler.create_mock_context(ctx, custom_text=command_text)
    command: Command = mock_ctx.command  # NOQA # ty:ignore[invalid-assignment] # sourcery skip: use-named-expression
    if not command:
        return ParsedCommand(command, None, None)
    return ParsedCommand(command, await run_guards(command, ctx), mock_ctx.command.name)


async def parse_pipe_commands(ctx: Context, string: str) -> ParsedCommand:
    command_list = string.split(" | ")
    first_command = await parse_command_by_name(ctx, command_list[0])
    for command in command_list:
        result = await parse_command_by_name(ctx, command)
        if result.guard_result:
            return result
    return ParsedCommand(first_command.command, None, None)


# TODO: Make the api tests
async def upload_alias(ctx: Context, aliases: list[Alias], table_name: str, command: AliasCmd) -> str | None:
    translations = command.translations.Table
    alias_table_headers = translations.alias_table_headers()
    alias_table_replaces = translations.alias_table_replaces()
    alias_table_list = []

    for alias in aliases:
        name = alias.name
        if alias.parent:
            alias = await alias.parent
        description = alias.description or alias_table_replaces[0]
        invocation = alias.invocation or ""
        arguments = " ".join(alias.arguments) if alias.arguments else None
        if arguments and "|" in arguments:
            arguments = arguments.replace("|", r"\|")
        parent_name = alias_table_replaces[2]
        if ctx.user.id != alias.user_id:
            parent_name = await User.get(id=alias.user_id) or ""
        updated_at = alias.updated_at.strftime(command.translations.SupportTools.TimeTools.strftime())
        created_at = alias.created_at.strftime(command.translations.SupportTools.TimeTools.strftime())
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
        column: max(len(str(item[column])) for item in [*alias_table_list, {column: column}]) for column in columns
    }

    header = "| " + " | ".join(column.center(max_lens[column]) for column in columns) + " |"
    separator = "| " + " | ".join(":" + "-".ljust(max_lens[column] - 1, "-") + ":" for column in columns) + " |"
    lines = [
        "| " + " | ".join(str(item[column]).center(max_lens[column]) for column in columns) + " |"
        for item in alias_table_list
    ]

    markdown_table = "\n".join([header, separator, *lines])

    data = {"markdown": markdown_table, "table_name": table_name}

    alias_cached_session = command.SessionsCaches.Alias.session
    response_url = await command.UploadThings.upload_alias(data=data, session=alias_cached_session)

    return await command.UploadThings.shortener(response_url, ["aliases"], alias_cached_session)


# endregion


# region Check functions


async def handle_list_all(ctx: Context, translations: Translations, command):
    aliases = await Alias.all_prefetch(ctx=ctx, user=ctx.user)
    names = flatten_alias_names(aliases)
    url = await upload_alias(ctx, aliases, translations.Table.alias_table_name(ctx.author_display_name or ""), command)
    if not url:
        return translations.Check.user_alias_list_error()
    return translations.Check.user_alias_list(", ".join(names), url)


def flatten_alias_names(aliases) -> list[str]:
    return [alias.name for alias in aliases]


async def handle_target_list(ctx: Context, target_user: User, translations: Translations, command):
    target_aliases = await Alias.all_prefetch(ctx=ctx, user=target_user)
    mention = translations.SupportTools.LanguageContext.mention(ctx.author_display_name or "", target_user.name)
    url = await upload_alias(ctx, target_aliases, translations.Table.alias_table_name(mention), command)
    if not url:
        return translations.Table.alias_table_upload_error(
            name=ctx.author_display_name or "", dev_name=ctx.bot.dev_user.display_name or ""
        )
    return translations.Check.list_of_alias_of(mention, url)


async def handle_special_case(
    ctx: Context, translations: Translations, aliases, target_aliases, first_name: str, target_user: User, command
):
    url1 = await upload_alias(ctx, aliases, translations.Table.alias_table_name(ctx.author_display_name or ""), command)
    url2 = await upload_alias(ctx, target_aliases, translations.Table.alias_table_name(target_user.name), command)
    if not url1 or not url2:
        return translations.Table.alias_table_upload_error(
            name=ctx.author_display_name or "", dev_name=ctx.bot.dev_user.display_name or ""
        )
    return translations.Check.list_of_special_case(first_name, url1, url2)


async def handle_alias_lookup(ctx: Context, user, alias_name: str, translations: Translations, command) -> Response:
    alias = await Alias.filter_first_prefetch(ctx=ctx, user=user, alias_name=alias_name)
    if not alias:
        mention = translations.SupportTools.LanguageContext.mention(ctx.author_display_name or "", user.name)
        return translations.Check.alias_not_found(mention, alias_name)

    if not alias.command and not alias.parent:
        return translations.Check.alias_deleted(alias_name)

    url = await upload_alias(ctx, [alias], translations.Table.alias_table_name(user.name), command)
    if not url:
        return translations.Table.alias_table_upload_error(
            name=ctx.author_display_name or "", dev_name=ctx.bot.dev_user.display_name or ""
        )
    invocation = f"{alias.invocation} {' '.join(alias.arguments)}" if alias.arguments else ""

    if not alias.command and alias.parent:
        parent_alias = await Alias.get(id=alias.parent.id, deleted=False)
        original_user = await User.get(id=parent_alias.user.id)
        return translations.Check.appendix_message(parent_alias.name, original_user.name, invocation, url)

    return translations.Check.normal_message(alias.name, invocation, url)


# endregion
