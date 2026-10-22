from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.fields.relational import ForeignKeyRelation
from tortoise.models import Model
from twitchio.ext.commands import Command, Group

from bot.models.base import TimestampMixin
from bot.types.named_tuples import AliasCached

SET_NULL = fields.SET_NULL

if TYPE_CHECKING:
    from bot.ext import Context
    from bot.models.channel import Channel
    from bot.models.user import User


class Alias(Model, TimestampMixin):
    id = fields.IntField(primary_key=True, db_db_index=True)
    user: User = fields.ForeignKeyField("models.User", related_name="Alias", null=True, on_delete=SET_NULL)  # ty:ignore[invalid-assignment]
    channel: ForeignKeyRelation[Channel] | None = fields.ForeignKeyField(
        "models.Channel", related_name="Alias", null=True, on_delete=SET_NULL
    )
    name = fields.CharField(max_length=50, db_index=True)
    command = fields.CharField(max_length=50, null=True)
    invocation = fields.CharField(max_length=50, null=True)
    arguments: list[str] | None = fields.JSONField(null=True)  # ty:ignore[invalid-assignment]
    description: str | None = fields.TextField(null=True)  # ty:ignore[invalid-assignment]
    parent: Alias | None = fields.ForeignKeyField(
        "models.Alias", related_name="children", null=True, on_delete=SET_NULL
    )  # ty:ignore[invalid-assignment]
    deleted = fields.BooleanField(default=False)

    user_id: int
    channel_id: int
    parent_id: int

    class Meta:
        table = "command_alias"
        verbose_name = "Custom Command Alias"
        verbose_name_plural = "Custom Command Aliases"

    indexes = [("user", "channel", "name"), ("channel",), ("command",), ("parent",)]  # NOQA: RUF012

    @staticmethod
    async def save_alias(ctx: Context, name: str, command_check: Command, invocation, rest) -> Alias:
        alias = Alias(
            user_id=ctx.author.id,
            channel_id=None,
            name=name,
            command=command_check.name,
            invocation=invocation,
            arguments=rest or [""],
        )
        await alias.save()
        cached = AliasCached(alias=alias, invocation=invocation, arguments=rest or [""])
        await ctx.bot.memcache.Alias.set(name=name, user_id=ctx.user.id, to_cache=cached)
        return alias

    @staticmethod
    async def link_alias(ctx: Context, name: str, parent: Alias, user: User | None = None):
        user: User = user or ctx.user  # type: ignore[assignment] ¯\_(ツ)_/¯
        alias = Alias(user=user, name=name, description=parent.description, parent=parent)
        await alias.save()
        cached = AliasCached(alias=alias, invocation=parent.invocation, arguments=parent.arguments, parent=parent)
        await ctx.bot.memcache.Alias.set(name=name, user_id=user.id, to_cache=cached)
        return alias

    @staticmethod
    async def get_alias(ctx: Context, name: str, user: User | None = None, deleted: bool = False) -> Alias | None:
        user: User = user or ctx.user  # type: ignore[assignment] ¯\_(ツ)_/¯
        memcache = ctx.bot.memcache.Alias
        cached_item = await memcache.get(key=name, user_id=user.id)
        if cached_item and cached_item.alias:
            return None if cached_item.alias.deleted and not deleted else cached_item.alias
        alias = await Alias.filter(user=user, name=name, deleted=deleted).first()
        if alias:
            await alias.fetch_related("parent")
            to_cache = AliasCached(alias=alias, invocation=alias.invocation, arguments=alias.arguments)
            await memcache.set(name=alias.name, user_id=user.id, to_cache=to_cache)

        return alias

    @staticmethod
    async def create_cached(
        ctx: Context,
        name: str,
        command: Command | Group,
        invocation: str,
        arguments: list[str] | None = None,
        description: str | None = None,
        parent: Alias | None = None,
    ) -> Alias:
        if arguments is None:
            arguments = [""]
        existing_alias = await Alias.get_alias(ctx, name=name)
        if existing_alias:
            return existing_alias
        if parent:
            alias = Alias(
                user=ctx.user, name=name or parent.name, description=description or parent.description, parent=parent
            )
        else:
            alias = Alias(
                user_id=ctx.author.id,
                name=name,
                command=command.name,
                invocation=invocation,
                arguments=arguments,
                description=description,
                parent=parent,
            )
        await alias.save()

        cached = AliasCached(alias=alias, invocation=invocation, arguments=arguments, parent=parent)
        await ctx.bot.memcache.Alias.set(name=name, user_id=ctx.user.id, to_cache=cached)
        return alias

    @staticmethod
    async def list_alias(ctx: Context, user_id: int | None = None, user: User | None = None) -> list[Alias]:
        user: User = user or ctx.user  # type: ignore[assignment] ¯\_(ツ)_/¯
        target_user_id = user_id or user.id
        memcache = ctx.bot.memcache.Alias
        cached_aliases = await memcache.list(user_id=target_user_id)
        if cached_aliases:
            return [a for a in cached_aliases if not a.deleted]
        db_aliases = await Alias.filter(user_id=target_user_id, deleted=False).all()
        if db_aliases:
            pairs = []
            for alias in db_aliases:
                await alias.fetch_related("parent")
                cached_obj = AliasCached(alias=alias, invocation=alias.invocation, arguments=alias.arguments)
                pairs.append((alias.name, cached_obj))
            await memcache.multi_set(pairs, user_id=target_user_id)
        return db_aliases

    @staticmethod
    async def filter_first_prefetch(
        ctx: Context, alias_name: str, user: User | None = None, prefetch: str = "parent"
    ) -> Alias | None:
        target_user = user or ctx.user
        alias = await Alias.get_alias(ctx, name=alias_name, user=target_user)
        if alias and prefetch:
            await alias.fetch_related(prefetch)
        return alias

    @staticmethod
    async def all_prefetch(ctx: Context, user: User | None = None, prefetch: str = "parent") -> list[Alias]:
        aliases = await Alias.list_alias(ctx, user=user)
        if aliases and prefetch:
            for alias in aliases:
                await alias.fetch_related(prefetch)

        return aliases

    @staticmethod
    async def first_prefetch(ctx: Context, user: User | None = None, prefetch: str = "parent") -> Alias | None:
        target_user: User = user or ctx.user  # type: ignore[assignment] ¯\_(ツ)_/¯
        memcache = ctx.bot.memcache.Alias
        cached_aliases = await memcache.list(user_id=target_user.id)
        active_aliases = [a for a in cached_aliases if not a.deleted]
        if cached_aliases and active_aliases:
            alias = active_aliases[0]
            if prefetch:
                await alias.fetch_related(prefetch)
            return alias
        alias = await Alias.filter(user=target_user, deleted=False).first()
        if alias:
            if prefetch:
                await alias.fetch_related(prefetch)
            to_cache = AliasCached(alias=alias, invocation=alias.invocation, arguments=alias.arguments)
            await memcache.set(name=alias.name, user_id=target_user.id, to_cache=to_cache)

        return alias

    @staticmethod
    async def filter_cached(ctx: Context, user: User | None = None, alias_name: str | None = None) -> list[Alias]:
        target_user = user or ctx.user
        if alias_name:
            alias = await Alias.get_alias(ctx, name=alias_name, user=target_user)
            return [alias] if alias else []

        return await Alias.list_alias(ctx, user=target_user)

    @staticmethod
    async def filter_first(ctx: Context, user: User | None = None, alias_name: str | None = None) -> Alias | None:
        target_user = user or ctx.user
        if alias_name:
            alias = await Alias.get_alias(ctx, name=alias_name, user=target_user)
            return alias or None

        aliases = await Alias.list_alias(ctx, user=target_user)
        return aliases[0] if aliases else None
