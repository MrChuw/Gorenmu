from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model
from twitchio.ext.commands import Command

from bot.ext.named_tuples import AliasCached
from bot.models.base import TimestampMixin

SET_NULL = fields.SET_NULL

if TYPE_CHECKING:
    from bot.ext import Context
    from bot.models.Channel import Channel
    from bot.models.User import User


class Alias(Model, TimestampMixin):
    id = fields.IntField(primary_key=True, db_db_index=True)
    user: User = fields.ForeignKeyField("models.User", related_name="Alias", null=True, on_delete=SET_NULL)
    channel: Channel = fields.ForeignKeyField("models.Channel", related_name="Alias", null=True, on_delete=SET_NULL)
    name: str = fields.CharField(max_length=50, db_index=True)
    command: str = fields.CharField(max_length=50, null=True)
    invocation: str = fields.CharField(max_length=50, null=True)
    arguments: list = fields.JSONField(null=True)
    description: str = fields.TextField(null=True)
    parent: Alias = fields.ForeignKeyField("models.Alias", related_name="children", null=True, on_delete=SET_NULL)
    deleted = fields.BooleanField(default=False)
    user_id: int
    channel_id: int
    parent_id: int

    class Meta:
        table = "command_alias"
        verbose_name = "Custom Command Alias"
        verbose_name_plural = "Custom Command Aliases"

    indexes = [("user", "channel", "name"), ("channel",), ("command",), ("parent",)]

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
    async def link_alias(ctx: Context, name: str, parent: Alias, user: User = None):
        user = user or ctx.user
        alias = Alias(user=user, name=name, description=parent.description, parent=parent)
        await alias.save()
        cached = AliasCached(alias=alias, invocation=parent.invocation, arguments=parent.arguments, parent=parent)
        await ctx.bot.memcache.Alias.set(name=name, user_id=ctx.user.id, to_cache=cached)
        return alias

    @staticmethod
    async def get_alias(ctx: Context, name: str, user: User = None, deleted: bool = False) -> Alias | None:
        user = user or ctx.user
        query = CachedAliasQuerySet(ctx, user, name, deleted)
        alias = await query.first()
        return alias or None

    @staticmethod
    async def create_cached(
        ctx: Context,
        name: str,
        command: Command = None,
        invocation: str = None,
        arguments: list[str] = None,
        description: str = None,
        parent: Alias = None,
    ) -> Alias:
        if arguments is None:
            arguments = [""]

        query = CachedAliasQuerySet(ctx, ctx.user, name)
        existing_alias = await query.first()
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
            )
        await alias.save()
        cached = AliasCached(alias=alias, invocation=invocation, arguments=arguments)

        await ctx.bot.memcache.Alias.set(name=name, user_id=ctx.user.id, to_cache=cached)

        return alias

    @staticmethod
    async def all_prefetch(ctx: Context, user: User = None, prefetch: str = "parent") -> list[Alias]:
        return await CachedAliasQuerySet(ctx=ctx, user=user).all().prefetch_related(prefetch)

    @staticmethod
    async def first_prefetch(ctx: Context, user: User = None, prefetch: str = "parent") -> list[Alias]:
        return await CachedAliasQuerySet(ctx=ctx, user=user).first().prefetch_related(prefetch)

    @staticmethod
    async def list_alias(ctx: Context, user_id: int = None, user: User = None) -> list[Alias]:
        return await ctx.bot.memcache.Alias.list(user_id=user_id or user.id)

    @staticmethod
    def filter_cached(ctx: Context, user: User = None, alias_name: str = None) -> CachedAliasQuerySet:
        return CachedAliasQuerySet(ctx=ctx, user=user, alias_name=alias_name)

    @staticmethod
    async def filter_first_prefetch(
        ctx: Context, user: User = None, alias_name: str = None, prefetch: str = "parent"
    ) -> Alias:
        return await CachedAliasQuerySet(ctx=ctx, user=user, alias_name=alias_name).first().prefetch_related(prefetch)


class CachedAliasQuerySet:  # TODO: The same thing with other caches...
    def __init__(self, ctx: Context, user: User, alias_name: str = None, deleted: bool = False):
        self.ctx = ctx
        self.user = user or ctx.user
        self.alias_name = alias_name
        if alias_name is not None:
            self._query = Alias.filter(user=self.user, name=self.alias_name, deleted=deleted)
        else:
            self._query = Alias.filter(user=self.user, deleted=deleted)
        self._method = "first"
        self._prefetch: list[str] = []

    def all(self) -> CachedAliasQuerySet:
        self._method = "all"
        return self

    def first(self) -> CachedAliasQuerySet:
        self._method = "first"
        return self

    def prefetch_related(self, *args: str) -> CachedAliasQuerySet:
        if not args:
            args = ("parent",)
        self._prefetch.extend(args)
        return self

    def first_prefetch(self, *args: str) -> CachedAliasQuerySet:
        if not args:
            args = ("parent",)
        self._prefetch.extend(args)
        self._method = "first"
        return self

    def all_prefetch(self, *args: str) -> CachedAliasQuerySet:
        if not args:
            args = ("parent",)
        self._prefetch.extend(args)
        self._method = "all"
        return self

    async def run(self) -> Alias | list[Alias] | None:
        memcache = self.ctx.bot.memcache.Alias
        if self.alias_name is None and self._method == "all":
            result = await self._query.all()
            cached = {}
            for alias in result:
                cached[alias.name] = AliasCached(alias=alias, invocation=alias.invocation, arguments=alias.arguments)
                if self._prefetch:
                    await alias.fetch_related(*self._prefetch)
            await self.ctx.bot.memcache.Alias.multi_set(list(cached.items()), user_id=self.user.id)
            return result

        aliases = await memcache.list(user_id=self.user.id)
        alias: Alias = next((a for a in aliases if a.name == self.alias_name), None)

        if alias:
            if self._prefetch:
                await alias.fetch_related(*self._prefetch)
            return None if alias.deleted else alias

        if self._method == "first":
            result = await self._query.first()
            if result:
                if self._prefetch:
                    await result.fetch_related(*self._prefetch)
                alias_tuple = AliasCached(alias=result, invocation=result.invocation, arguments=result.arguments)
                await memcache.set(name=result.name, user_id=self.user.id, to_cache=alias_tuple)
                return result if result and not result.deleted else None

        if self._method == "all":
            result = await self._query.all()
            return result
        return None

    def __await__(self):
        return self.run().__await__()
