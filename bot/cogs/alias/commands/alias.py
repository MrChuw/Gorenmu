# -*- coding: utf-8 -*-
import re
from itertools import chain, repeat
from bot.bot import Gorenmu

from twitchio.ext.commands import Command

from bot.ext.commands import base_decorator, Bucket, check, command, Context, cooldown
from bot.models import Alias, User
from bot.translations import EnDecorators, Response
import re

ALIAS_NAME_REGEX = re.compile(
        r'^[-\w\u00a9\u00ae\u2000-\u3300\ud83c\ud000-\udfff\ud83d\ud000-\udfff\ud83e\ud000-\udfff]{2,30}$'
)


@base_decorator(EnDecorators.Alias)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='alias', aliases=[''])
async def command(ctx: Context, action: str, *args, ) -> Response:
    # TODO: Verificar se o deleted está direito nas funções.
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


async def upload_alias(ctx: Context, aliases: list[Alias], table_name: str):  # TODO: Fazer o upload
    translations = ctx.translations.Alias
    alias_table_headers = translations.alias_table_headers
    alias_table_replaces = translations.alias_table_replaces
    alias_table_list = []

    for alias in aliases:
        name = alias.name
        if alias.parent:
            alias = alias.parent
        description = alias.description or alias_table_replaces[0]
        invocation = alias.invocation or ""
        arguments = " ".join(alias.arguments) or [1]
        if "|" in arguments:
            arguments = arguments.replace("|", r"\|")
        parent_name = alias_table_replaces[2]
        if ctx.user.id != alias.user_id:
            parent_name = await User.get(id=alias.user_id) or ""
        updated_at = alias.updated_at.strftime(ctx.translations.SupportTools.TimeTools.strftime)
        created_at = alias.created_at.strftime(ctx.translations.SupportTools.TimeTools.strftime)
        alias_table_list.append({alias_table_headers[0]: name,
                                 alias_table_headers[1]: description,
                                 alias_table_headers[2]: invocation,
                                 alias_table_headers[3]: arguments,
                                 alias_table_headers[4]: parent_name,
                                 alias_table_headers[5]: updated_at,
                                 alias_table_headers[6]: created_at
                                 })

    columns = alias_table_list[0].keys()
    max_lens = {column: max(len(str(item[column])) for item in alias_table_list + [{column: column}]) for column in
                columns}

    header = "| " + " | ".join(column.center(max_lens[column]) for column in columns) + " |"
    separator = "| " + " | ".join(":" + "-".ljust(max_lens[column] - 1, '-') + ":" for column in columns) + " |"
    lines = ["| " + " | ".join(str(item[column]).center(max_lens[column]) for column in columns) + " |" for item in
             alias_table_list]

    markdown_table = "\n".join([header, separator] + lines)


    url = 'https://alias.mrchuw.com.br/submit'
    data = {'markdown': markdown_table, 'table_name': table_name}

    alias_cached_session = ctx.bot.SessionsCaches.AliasCachedSession

    response = await alias_cached_session.session.post(url, data=data)
    response = await ctx.bot.UploadThings.shortener(response.url.human_repr(), ctx.bot, alias_cached_session.session)
    return response


async def add_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    name, command_, *rest = chain(args, repeat(None, 2))
    if not command_:
        return translations.Add.no_command_to_add.format_response(ctx, ctx.prefix, success=False, pipe=False)

    if not ALIAS_NAME_REGEX.match(name):
        return translations.alias_invalid_name.format_response(ctx, success=False, pipe=False)
    alias = await Alias.get_or_none(user=ctx.user, name=name, deleted=False)
    if alias:
        return translations.Add.alias_name_conflict.format_response(ctx, name, success=False, pipe=False)

    command_check = parse_command_by_name(ctx, command_)
    if not command_check:
        return translations.Add.command_dont_exist.format_response(ctx, command_, success=False, pipe=False)
    rest = [arg for arg in rest if arg]
    alias = await Alias.save_alias(ctx, name, command_check, command_, rest)
    return translations.Add.alias_crated.format_response(ctx, alias.name, pipe=False)


async def check_alias(ctx: Context, args: tuple):  # TODO: test check a link alias
    translations = ctx.translations.Alias
    first_name, second_name, *rest = chain(args, repeat(None, 2))
    if not first_name and not second_name:
        aliases = await Alias.filter(channel=None, user=ctx.user, deleted=False).prefetch_related("parent")
        aliases_flat = [alias.name for alias in aliases]
        url = await upload_alias(ctx, aliases, translations.alias_table_name.format(ctx.author.display_name))
        return translations.Check.user_alias_list.format_response(ctx, ", ".join(aliases_flat), url, success=False,
                                                                  pipe=False)

    target_aliases_flat = []
    aliases = await Alias.filter(channel=None, user=ctx.user, deleted=False).prefetch_related("parent")
    aliases_flat = [alias.name for alias in aliases]

    target_user = await User.get_or_none(name=first_name)
    if target_user:
        target_aliases = await Alias.filter(channel=None, user=target_user).prefetch_related("parent")
        target_aliases_flat = [alias.name for alias in target_aliases]

    if target_aliases_flat == [] and first_name not in aliases_flat and not second_name:
        return translations.user_has_no_alias.format_response(ctx, target_user.name, success=False, pipe=False)
    elif target_aliases_flat == [] and first_name in aliases_flat and not second_name:
        user = ctx.user
        alias_name = first_name
        mention = translations.mention(ctx, user, user.name)
    elif target_aliases_flat and first_name not in aliases_flat and not second_name:
        mention = translations.mention(ctx, target_user, target_user.name)
        url = await upload_alias(ctx, target_aliases, translations.alias_table_name.format(mention))  # NOQA
        return translations.Check.list_of_alias_of.format_response(ctx, mention, url, pipe=False)
    elif target_aliases_flat and first_name in aliases_flat and not second_name:
        url1 = await upload_alias(ctx, aliases, translations.alias_table_name.format(ctx.author.display_name))
        url2 = await upload_alias(ctx, target_aliases, translations.alias_table_name.format(target_user.name))  # NOQA
        return translations.Check.list_of_special_case.format_response(ctx, first_name, url1, url2, pipe=False)

    if second_name:
        user = await User.get_or_none(name=first_name)
        if not user:
            return translations.user_not_found.format_response(ctx, first_name, success=False, pipe=False)

        alias_name = second_name
        mention = translations.mention(ctx, user, ctx.author.name)

    alias = await Alias.filter(user_id=user.id, name=alias_name, deleted=False).first().prefetch_related("parent")  # NOQA

    if not alias:
        return translations.Check.alias_not_found.format_response(ctx, mention, alias_name, success=False, pipe=False)  # NOQA

    if not alias.command and not alias.parent:  # NOQA
        return translations.Check.alias_deleted.format_response(ctx, mention, success=False, pipe=False)  # NOQA

    url = await upload_alias(ctx, [alias], translations.alias_table_name.format(user.name))
    invocation = f"{alias.invocation} {' '.join(alias.arguments)}"
    if not alias.command and alias.parent:  # NOQA
        alias = await Alias.get(id=alias.parent.id, deleted=False)
        original_user = await User.get(id=alias.user.id)
        return translations.Check.appendix_message.format_response(ctx, alias.name, original_user.name, alias.name,
                                                                   alias.name, invocation, url, pipe=False)

    return translations.Check.normal_message.format_response(ctx, alias.name, invocation, url, pipe=False)


async def copy_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    target_user_name, target_alias_name, *rest = chain(args, repeat(None, 2))
    rest = [arg for arg in rest if arg]
    new_name = None
    if rest:
        new_name = rest[0]
    if not target_user_name:
        return translations.Copy.user_not_provided.format_response(ctx, success=False, pipe=False)
    if not target_alias_name:
        return translations.Copy.alias_not_provided.format_response(ctx, success=False, pipe=False)
    if not ALIAS_NAME_REGEX.match(target_alias_name):
        return translations.Copy.target_alias_invalid_name.format_response(ctx, success=False, pipe=False)

    alias = await Alias.filter(user=ctx.user, name=target_alias_name, deleted=False).first()
    if alias:
        return translations.Add.alias_name_conflict.format_response(ctx, target_alias_name, success=False, pipe=False)

    target_user = await User.get_or_none(name=target_user_name)
    if not target_user:
        return translations.user_not_found.format_response(ctx, target_user_name, success=False, pipe=False)

    target_alias = await Alias.filter(channel=None, user=target_user, name=target_alias_name, deleted=False).first()
    if target_alias is None:
        return translations.Copy.no_alias_found.format_response(ctx, target_alias_name,
                                                                target_user.name,
                                                                success=False,
                                                                pipe=False)

    if target_alias.command is None:  # NOQA
        return translations.Copy.link_to_a_link.format_response(ctx, ctx.prefix, target_user.name,
                                                                target_alias_name,
                                                                success=False,
                                                                pipe=False)

    new_alias = await Alias.create(user_id=ctx.author.id, channel_id=None,
                                   name=target_alias_name if not new_name else new_name,
                                   command=target_alias.command,  # NOQA
                                   invocation=target_alias.invocation,
                                   arguments=target_alias.arguments, parent_id=target_alias.id, )
    if new_name:
        return translations.Copy.copy_success.format_response(ctx, target_alias_name, new_alias.name, pipe=False)
    return translations.Copy.copy_success.format_response(ctx, new_alias.name, pipe=False)


async def describe_alias(ctx: Context, args: tuple):  # NOQA
    translations = ctx.translations.Alias
    if not args:
        return translations.Describe.no_args_to_parse.format_response(ctx, ctx.prefix, success=False, pipe=False)

    name, *rest = chain(args, repeat(None, 2))
    rest = [arg for arg in rest if arg]
    alias = await Alias.filter(user=ctx.user, name=name, deleted=False).first()

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


async def edit_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    if len(args) < 2:
        return translations.Edit.no_args_provided.format_response(ctx, success=False, pipe=False)

    name, command_, *rest = chain(args, repeat(None, 2))
    rest = [arg for arg in rest if arg]
    command_check = parse_command_by_name(ctx, command_)

    if not command_check:
        return translations.Edit.command_dont_exist.format_response(ctx, command_, success=False, pipe=False)

    alias = await Alias.filter(user=ctx.user, name=name, deleted=False).first()
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
    link_to_link = False
    if len(args) < 2:
        return translations.Link.link_no_args.format_response(ctx, success=False, pipe=False)

    user_name, alias_name, custom_link_name, *rest = chain(args, repeat(None, 2))
    rest = [arg for arg in rest if arg]
    name = custom_link_name or alias_name

    existing_alias = await Alias.filter(user=ctx.user, name=name, deleted=False).first()

    if existing_alias and not custom_link_name:
        return translations.Add.alias_name_conflict.format_response(ctx, alias_name, success=False, pipe=False)

    target_user_data = await User.get_or_none(name=user_name)
    if not target_user_data:
        return translations.user_not_found.format_response(ctx, user_name, success=False, pipe=False)

    target_alias = await (Alias.filter(user=target_user_data, name=alias_name,
                                       deleted=False).first().prefetch_related("parent"))

    if not target_alias and not target_alias.parent:
        return translations.Link.user_dont_has_alias.format_response(ctx, alias_name, success=False, pipe=False)
    elif target_alias.command is None and target_alias.parent_id is not None:  # NOQA
        target_alias: Alias = await target_alias.parent
        await target_alias.fetch_related("user")
        original_user = await target_alias.user
        target_alias.name = alias_name
        link_to_link = True

    elif not ALIAS_NAME_REGEX.match(target_alias.name):
        return translations.Link.link_with_invalid_name.format_response(ctx, translations.alias_invalid_name,
                                                                        success=False,
                                                                        pipe=False)

    await Alias.link_alias(ctx.user, name, target_alias)

    name_string = translations.Link.link_name_string.format(custom_link_name) if (
            custom_link_name and custom_link_name != target_alias.name) else "."

    if link_to_link:
        return translations.Link.link_to_link.format_response(ctx, target_alias.name, original_user.name, name_string,  # NOQA
                                                              pipe=False)

    return translations.Link.link_success.format_response(ctx, name_string, pipe=False)


async def remove_alias(ctx: Context, args: tuple):
    translations = ctx.translations.Alias
    if len(args) < 1:
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
        return translations.alias_invalid_name.format_response(ctx, translations.alias_invalid_name, success=False,
                                                               pipe=False)
    old_alias = await Alias.get_or_none(user=ctx.user, name=old_alias_name, deleted=False)

    if not old_alias:
        return translations.dont_have_alias.format_response(ctx, old_alias_name, success=False, pipe=False)
    existing_alias = await Alias.filter(user=ctx.user, name=new_alias_name, deleted=False).first()
    if existing_alias:
        return translations.Rename.alias_already_exists.format_response(ctx, new_alias_name, success=False, pipe=False)

    old_alias.name = new_alias_name
    await old_alias.save()
    return translations.Rename.alias_renamed.format_response(ctx, old_alias_name, new_alias_name, pipe=False)


def dynamic_description(command_: Command, bot: Gorenmu, ctx: Context = None, ) -> dict[str, dict[str, str]]: # TODO: Fazer o templeta do alias
    responses: dict[str, dict[str, str]] = {}
    cooldown_ = command_._cooldowns[0]  # NOQA
    per = cooldown_._per  # NOQA
    rate = cooldown_._rate  # NOQA
    prefix = ctx.prefix if ctx else bot.config.BotConfig.prefix[0]
    for lang in command_.decorators:
        if lang not in responses:
            responses[lang] = {}
        decorator: EnDecorators.Alias = command_.decorators[lang]
        description = decorator.get_description(decorator)  # NOQA
        base_decorators = bot.TranslationManager.get_decorator(lang)
        cooldown_type = base_decorators.get_bucket_type(cooldown_.bucket)
        # Exemplo de uso
        afk_template = custom_format(
                getattr(decorator, 'template', EnDecorators.Alias.template),
                rate=rate,
                per=per,
                cooldown_type=cooldown_type,
                description=description,
                command_title=command_.name.capitalize(),
                command_name=command_.name.lower(),
                prefix=prefix, aliases=", ".join([])
        )

        responses[lang][command_.name.lower()] = afk_template

    return responses


def custom_format(template, **kwargs):
    # Expressão regular para identificar apenas os placeholders que você deseja substituir
    pattern = re.compile(r"\{(rate|per|cooldown_type|description|command_title|command_name|prefix|aliases)}")

    # Função para substituir apenas os placeholders definidos em kwargs
    def replace(match):
        placeholder = match.group(1)
        return str(kwargs.get(placeholder, match.group(0)))

    # Substituir apenas os placeholders definidos em pattern
    return pattern.sub(replace, template)



