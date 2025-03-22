# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING


from .extras.response import BaseFunctions, CommandExemples
from twitchio.ext.commands import BucketType



if TYPE_CHECKING:
    from bot.ext.commands import Context
    from bot.ext import Command
    from bot.translations import TranslationManager


class Decorators(BaseFunctions):
    def __init__(self, translation: dict, fallback: dict = None):
        fallback_decorators = fallback['decorators'] if fallback else None
        extras = translation['extras'] if 'extras' in translation else fallback['extras']
        extras_fallback = fallback['extras'] if fallback else None
        extras = BaseFunctions(extras, extras_fallback)
        super().__init__(translation['decorators'], fallback_decorators)

        self.populate_subclasses(
                base_cls=BaseDecorators(),
                add_to_self=True
        )

        self.decorators: dict[str, BaseDecorators] = {
                'pipe': self.Pipe,
                'afk': self.Afk,
                'isafk': self.IsAfk,
                'rafk': self.RAfk,
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
                        'disable_nsfw': self.Admin.DisableNSFW,
                }
        }

        self.categories: list[str] = ["NSFW", "Dev"]
        self.exclude_categories: list[str] = ["NSFW"]

    Templates: BaseDecorators.Templates
    TypeChecking: BaseDecorators.TypeChecking
    Pipe: BaseDecorators.Pipe
    Afk: BaseDecorators.Afk
    IsAfk: BaseDecorators.IsAfk
    RAfk: BaseDecorators.RAfk
    Alias: BaseDecorators.Alias
    Chance: BaseDecorators.Chance
    Choice: BaseDecorators.Choice
    Count: BaseDecorators.Count
    HyperTranslate: BaseDecorators.HyperTranslate
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

    NSFW: BaseDecorators.NSFW
    Admin: BaseDecorators.Admin


class DecorationsFunctions(BaseFunctions):
    @classmethod
    def get_decorator(cls, ctx: Context) -> DecoratorType | None:
        if "usage" in dir(cls):
            return cls  # NOQA
        decorator = ctx.command.decorators[ctx.user.language]
        for classe in dir(decorator):
            if classe.startswith("__") or classe.startswith("get_"): continue
            invoke_by = ctx.message.text.partition(" ")[0][len(ctx.prefix):].lower()
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

        def get_bucket_type(self, bucket):
            bucket_type = self.bucket_type["default"]
            if bucket == BucketType.default:
                bucket_type = self.bucket_type["default"]

            if bucket == BucketType.channel:
                bucket_type = self.bucket_type["channel"]

            if bucket == BucketType.user:
                bucket_type = self.bucket_type["user"]

            return bucket_type

    class TypeChecking(BaseFunctions):
        PlaceHolder: Decorators


    class Pipe(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2024-09-09")

    class Afk(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-16T12:20:00.000-03:00")

    class IsAfk(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-16T12:20:00.000-03:00")

    class RAfk(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-16T12:20:00.000-03:00")

    class Alias(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-16T12:20:00.000-03:00")

    class Chance(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-17T20:00:00.000-03:00")

    class Choice(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-17T20:00:00.000-03:00")

    class Count(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-17T20:00:00.000-03:00")

    class HyperTranslate(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-22T12:54:31.259-03:00")

    class RandomColor(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-17T20:00:00.000-03:00")

    class Reverse(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-17T20:00:00.000-03:00")

    class RandomLine(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-19T12:20:00.000-03:00")

    class Scp(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-19T21:06:00.000-03:00")

    class UpSideDown(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-19T21:06:00.000-03:00")

    class Wikihow(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-19T21:06:00.000-03:00")

    class Wikipedia(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-09", "2025-03-19T21:06:00.000-03:00")

    class Annotations(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-10", "2025-03-20T23:39:00.000-03:00")

    class Lottery(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-16T12:17:48.181-03:00", "2024-09-17T12:17:48.181-03:00")

    class Safebooru(BaseCommand):
        def __init__(self, translation: dict):
            super().__init__(translation, "2024-09-19T14:58:36.046-03:00", "2024-09-19T14:58:36.046-03:00")

    class Cookies(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)

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


    class NSFW(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)

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

    class Admin(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)

        class Nada(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2025-03-16T12:20:00.000-03:00")
        Nada: Nada

        class Reload(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-09", "2025-03-16T12:20:00.000-03:00")
        Reload: Reload

        class Restart(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2024-09-18T18:25:27.911-03:00", "2025-03-18T12:20:00.000-03:00")
        Restart: Restart

        class DisableNSFW(BaseCommand):
            def __init__(self, translation: dict):
                super().__init__(translation, "2025-03-14T13:19:12.370-03:00", "2025-03-14T13:19:12.370-03:00")
        DisableNSFW: DisableNSFW






def inject_translations(command: Command, translations: TranslationManager):
    translations_decorators = {}
    fallback = translations.languages["en"].decorators
    categories = ["", "NSFW", "Dev"]

    for lang, lang_data in translations.languages.items():
        translation = lang_data.decorators
        decorators_dict = translation.__dict__
        for category in categories:
            decorators = translation.decorators.get(category, translation.decorators)
            if command.name.lower() in decorators:
                translations_decorators[lang] = decorators[command.name.lower()]
                break
        else:
            for category in categories:
                fallback_decorators = fallback.get(category, translation.decorators)
                if command.name.lower() in fallback_decorators:
                    translations_decorators[lang] = fallback_decorators[command.name.lower()]
                    break

    command.decorators = translations_decorators
    return command
