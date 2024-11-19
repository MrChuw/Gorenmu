# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING
from .extras.response import BaseFunctions
from twitchio.ext.commands import Bucket

if TYPE_CHECKING:
    from bot.ext.commands import Context



class Decorators(BaseFunctions):
    def __init__(self, translation: dict, fallback: dict = None):
        fallback_decorators = fallback['decorators'] if fallback else None
        extras = translation['extras'] if 'extras' in translation else fallback['extras']
        extras_fallback = fallback['extras'] if fallback else None
        extras = BaseFunctions(extras, extras_fallback)
        super().__init__(translation['decorators'], fallback_decorators)
        decorator_names = ["Templates", "TypeChecking", "Admin", "Others", "Afk", "Alias", "Choice", "Count",
                           "HyperTranslate", "NSFW", "RandomColor", "Reverse", "RandomLine", "Scp", "UpSideDown",
                           "Wikihow", "Wikipedia", "Annotations", "Lottery", "Safebooru", "Cookies"
                           ]

        for name in decorator_names:
            if name == "TypeChecking":
                base = (None, None)
            else:
                base = self.get_base(name)
            decorator_class = getattr(BaseDecorators, name)
            setattr(self, name, decorator_class(base))


        self.decorators = {
                'pipe': BaseDecorators.Others.Pipe,
                'afk': BaseDecorators.Afk,
                'alias': BaseDecorators.Alias,
                'chance': BaseDecorators.Chance,
                'choice': BaseDecorators.Choice,
                'count': BaseDecorators.Count,
                'hypertranslate': BaseDecorators.HyperTranslate,
                'randomcolor': BaseDecorators.RandomColor,
                'reverse': BaseDecorators.Reverse,
                'randomline': BaseDecorators.RandomLine,
                'rscp': BaseDecorators.Scp,
                'upsidedown': BaseDecorators.UpSideDown,
                'wikihow': BaseDecorators.Wikihow,
                'annotations': BaseDecorators.Annotations,
                'lottery': BaseDecorators.Lottery,


                'NSFW': {
                        'imgur': BaseDecorators.NSFW.Imgur,
                        'imgur_repeated': BaseDecorators.NSFW.ImgurRepeated,
                },

                'Dev': {
                        'nada': BaseDecorators.Admin.Nada,
                        'reload': BaseDecorators.Admin.Reload,
                        'restart': BaseDecorators.Admin.Restart,
                }
        }

        self.categories = ["NSFW", "Dev"]
        self.exclude_categories = ["NSFW"]
        del self.fallback, self.obj
    ...



class DecorationsFunctions(BaseFunctions):
    @classmethod
    def get_decorator(cls, ctx: Context) -> DecoratorType | None:
        if "usage" in dir(cls):
            return cls  # NOQA
        decorator = ctx.command.decorators[ctx.user.language]
        for classe in dir(decorator):
            invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
            if invoke_by == classe.lower():
                return getattr(decorator, classe)

    @classmethod
    def get_helper(cls, ctx: Context) -> str:
        return cls.get_decorator(ctx).helper.format(ctx.prefix)

    @classmethod
    def get_usage(cls, ctx: Context) -> str:
        return cls.get_decorator(ctx).usage.format(ctx.prefix)

    @classmethod
    def get_description(cls, ctx: Context | DecoratorType) -> str:
        return cls.get_decorator(ctx).description

    def get_object_or_false(self, key: str):
        obj = self.get_object(key)
        if len(obj) == 0:
            return False
        return obj


class CommandExemples:
    def __init__(self, data):
        self.items = [CommandExemplesItem(**item) for item in data] if data else False

    def __iter__(self):
        return iter(self.items) if self.items else iter([])


class CommandExemplesItem:
    def __init__(self, args, response):
        self.args = args
        self.response = response


class Admonitions:
    def __init__(self, admonitions):
        self.items = [AdmonitionItem(**item) for item in admonitions] if admonitions else False

    def __iter__(self):
        return iter(self.items) if self.items else iter([])


class AdmonitionItem:
    def __init__(self, admonition_type, title, message, position="bottom"):
        if position not in {"top", "middle", "bottom"}:
            position = "bottom"
        self.type = admonition_type
        self.title = title
        self.message = message
        self.position = position


class DecoratorType:
    helper: str
    usage: str
    description: str
    extras: str = ""
    created: str
    updated: str
    commands: CommandExemples = None
    admonitions: Admonitions = None
    template: str


class BaseCommand(DecoratorType, DecorationsFunctions):
    def __init__(self, translation: dict, created: str, updated: str):
        super().__init__(translation, None)
        self.helper = self.get_object("helper")
        self.usage = self.get_object("usage")
        self.description = self.get_object("description")
        self.extras = self.get_object("extras")
        self.commands = self.get_object_or_false("commands")
        self.admonitions = self.get_object_or_false("admonitions")
        self.template = self.get_object_or_false("template")
        self.created = created
        self.updated = updated
        self.template = self.get_object_or_none("template")
        del self.fallback, self.obj


class BaseDecorators:
    class Templates(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.template_part1 = self.get_object("template_part1")
            self.template_part2 = self.get_object("template_part2")
            self.template_part3 = self.get_object("template_part3")
            self.alias_template = self.get_object("alias_template")
            self.command_template = self.get_object("command_template")
            self.admonition_template = self.get_object("admonition_template")

            self.bucket_default = self.get_object("bucket_default")
            self.bucket_channel = self.get_object("bucket_channel")
            self.bucket_member = self.get_object("bucket_member")
            self.bucket_user = self.get_object("bucket_user")
            self.bucket_subscriber = self.get_object("bucket_subscriber")
            self.bucket_mod = self.get_object("bucket_mod")

            del self.fallback, self.obj

        @staticmethod
        def get_bucket_type(bucket):
            bucket_type = "geral"
            if bucket == Bucket.default:
                bucket_type = "dont know"

            if bucket == Bucket.channel:
                bucket_type = "all user per channel"

            if bucket == Bucket.member:
                bucket_type = "user per channel"

            if bucket == Bucket.user:
                bucket_type = "user independent of channel"

            if bucket == Bucket.subscriber:
                bucket_type = "subscriber"

            if bucket == Bucket.mod:
                bucket_type = "moderation"
            return bucket_type

    class TypeChecking(BaseFunctions):
        pass

    class Admin(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            decorator_names = ["Nada", "Reload", "Restart"]
            for name in decorator_names:
                base = self.get_base(name)
                decorator_class = getattr(BaseDecorators, name)
                setattr(self, name, decorator_class(base))
            del self.fallback, self.obj

        class Nada(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2024-09-09")

        class Reload(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2024-09-09")

        class Restart(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-18T18:25:27.911-03:00", "2024-09-18T18:25:27.911-03:00")

        Nada: Nada
        Reload: Reload
        Restart: Restart

    class Others(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            decorator_names = ["Pipe"]
            for name in decorator_names:
                base = self.get_base(name)
                decorator_class = getattr(BaseDecorators, name)
                setattr(self, name, decorator_class(base))
            del self.fallback, self.obj

        class Pipe(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2024-09-09")

        Pipe: Pipe

    class Afk(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            decorator_names = ["Afk", "IsAfk", "RAfk"]
            for name in decorator_names:
                base = self.get_base(name)
                decorator_class = getattr(BaseDecorators, name)
                setattr(self, name, decorator_class(base))
            del self.fallback, self.obj


        class Afk(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2024-09-09")

        class IsAfk(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2024-09-09")

        class RAfk(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2024-09-09")

        Afk: Afk
        IsAfk: IsAfk
        RAfk: RAfk

    class Alias(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class Chance(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class Choice(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class Count(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class HyperTranslate(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class NSFW(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            decorator_names = ["Imgur", "ImgurRepeated", "Boru"]
            for name in decorator_names:
                base = self.get_base(name)
                decorator_class = getattr(BaseDecorators, name)
                setattr(self, name, decorator_class(base))
            del self.fallback, self.obj

        class Imgur(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2024-09-09")

        class ImgurRepeated(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2024-09-09")

        class Boru(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2024-09-09")

        Imgur: Imgur
        ImgurRepeated: ImgurRepeated
        Boru: Boru

    class RandomColor(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class Reverse(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class RandomLine(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class Scp(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class UpSideDown(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class Wikihow(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class Wikipedia(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class Annotations(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-10", "2024-09-10")

    class Lottery(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-16T12:17:48.181-03:00", "2024-09-17T12:17:48.181-03:00")

    class Safebooru(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-19T14:58:36.046-03:00", "2024-09-19T14:58:36.046-03:00")

    class Cookies(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            decorator_names = ["CookieCount", "Gift", "SlotMachine", "Stock", "Top"]
            for name in decorator_names:
                base = self.get_base(name)
                decorator_class = getattr(BaseDecorators, name)
                setattr(self, name, decorator_class(base))
            del self.fallback, self.obj

        class CookieCount(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-28", "2024-09-28")

        class Gift(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-28", "2024-09-28")

        class SlotMachine(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-28", "2024-09-28")

        class Stock(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-28", "2024-09-28")

        class Top(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-28", "2024-09-28")

        CookieCount: CookieCount
        Gift: Gift
        SlotMachine: SlotMachine
        Stock: Stock
        Top: Top













































