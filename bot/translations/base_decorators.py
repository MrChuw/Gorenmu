# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING
from .extras.response import BaseFunctions, CommandExemples
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
        decorator_names = ["Templates", "TypeChecking", "Admin", "Others", "Afk", "Alias", "Chance", "Choice", "Count",
                           "HyperTranslate", "NSFW", "RandomColor", "Reverse", "RandomLine", "Scp", "UpSideDown",
                           "Wikihow", "Wikipedia", "Annotations", "Lottery", "Safebooru", "Cookies"
                           ]

        for name in decorator_names:
            if name == "TypeChecking":
                base = None, None
            else:
                base = self.get_base(name)
            decorator_class = getattr(BaseDecorators, name)
            setattr(self, name, decorator_class(base) if name != "TypeChecking" else decorator_class(None, None))


        self.decorators = {
                'pipe': self.Others.Pipe,
                'afk': self.Afk,
                'alias': self.Alias,
                'chance': self.Chance,
                'choice': self.Choice,
                'count': self.Count,
                'hypertranslate': self.HyperTranslate,
                'randomcolor': self.RandomColor,
                'reverse': self.Reverse,
                'randomline': self.RandomLine,
                'randomscp': self.Scp,
                'upsidedown': self.UpSideDown,
                'wikihow': self.Wikihow,
                "wikipedia": self.Wikipedia,
                'annotations': self.Annotations,
                'lottery': self.Lottery,
                'safebooru': self.Safebooru,
                'cookies': self.Cookies,


                'NSFW': {
                        'imgur': self.NSFW.Imgur,
                        'imgur_repeated': self.NSFW.ImgurRepeated,
                        'booru': self.NSFW.Boru
                },

                'Dev': {
                        'nada': self.Admin.Nada,
                        'reload': self.Admin.Reload,
                        'restart': self.Admin.Restart,
                }
        }

        self.categories = ["NSFW", "Dev"]
        self.exclude_categories = ["NSFW"]
        del self.fallback, self.obj

    Templates: BaseDecorators.Templates
    TypeChecking: BaseDecorators.TypeChecking
    Admin: BaseDecorators.Admin
    Others: BaseDecorators.Others
    Afk: BaseDecorators.Afk
    Alias: BaseDecorators.Alias
    Chance: BaseDecorators.Chance
    Choice: BaseDecorators.Choice
    Count: BaseDecorators.Count
    HyperTranslate: BaseDecorators.HyperTranslate
    NSFW: BaseDecorators.NSFW
    RandomColor: BaseDecorators.RandomColor
    Reverse: BaseDecorators.Reverse
    RandomLine: BaseDecorators.RandomLine
    Scp: BaseDecorators.Scp
    UpSideDown: BaseDecorators.UpSideDown
    Wikihow: BaseDecorators.Wikihow
    Wikipedia: BaseDecorators.Wikipedia
    Annotations: BaseDecorators.Annotations
    Lottery: BaseDecorators.Lottery
    Safebooru: BaseDecorators.Safebooru
    Cookies: BaseDecorators.Cookies


    decorators: dict
    categories: list
    exclude_categories: list


class DecorationsFunctions(BaseFunctions):
    @classmethod
    def get_decorator(cls, ctx: Context) -> DecoratorType | None:
        if "usage" in dir(cls):
            return cls  # NOQA
        decorator = ctx.command.decorators[ctx.user.language]
        for classe in dir(decorator):
            if classe.startswith("__") or classe.startswith("get_"): continue
            invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
            if invoke_by == classe.lower():
                return getattr(decorator, classe)


    def get_object_or_false(self, key: str):
        obj = self.get_object_or_none(key)
        if not obj or len(obj) == 0:
            return False
        return obj


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
        self.extras = self.get_object_or_none("extras")
        self.commands = CommandExemples(self.get_object_or_false("commands"))
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
            self.template_part1: str = self.get_object("template_part1")
            self.template_part2: str = self.get_object("template_part2")
            self.template_part3: str = self.get_object("template_part3")
            self.alias_template: str = self.get_object("alias_template")
            self.command_template: str = self.get_object("command_template")
            self.admonition_template: str = self.get_object("admonition_template")

            self.bucket_type: dict[str, str] = self.get_object("bucket_type")

            del self.fallback, self.obj

        def get_bucket_type(self, bucket):
            bucket_type = self.bucket_type["default"]
            if bucket == Bucket.default:
                bucket_type = self.bucket_type["default"]

            if bucket == Bucket.channel:
                bucket_type = self.bucket_type["channel"]

            if bucket == Bucket.member:
                bucket_type = self.bucket_type["member"]

            if bucket == Bucket.user:
                bucket_type = self.bucket_type["user"]

            if bucket == Bucket.subscriber:
                bucket_type = self.bucket_type["subscriber"]

            if bucket == Bucket.mod:
                bucket_type = self.bucket_type["mod"]
            return bucket_type

    class TypeChecking(BaseFunctions):
        pass

    class Admin(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            decorator_names = ["Nada", "Reload", "Restart"]
            for name in decorator_names:
                base = self.get_base(name)
                decorator_class = getattr(BaseDecorators.Admin, name)
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
                decorator_class = getattr(BaseDecorators.Others, name)
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
                decorator_class = getattr(BaseDecorators.Afk, name)
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
                decorator_class = getattr(BaseDecorators.NSFW, name)
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
                decorator_class = getattr(BaseDecorators.Cookies, name)
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













































