# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from twitchio.ext.commands import BucketType

from .extras.response import BaseFunctions, CommandExemples

if TYPE_CHECKING:
    from bot.ext import Context


class DecorationsFunctions(BaseFunctions):
    @classmethod
    def get_decorator(cls, ctx: Context) -> DecoratorType | None:
        if "usage" in dir(cls):
            return cls  # NOQA
        decorator = ctx.command.decorators[ctx.user.language]
        for classe in dir(decorator):  # NOQA
            if classe.startswith("__") or classe.startswith("get_"):
                continue
            invoke_by = ctx.message.text.partition(" ")[0][len(ctx.prefix) :].lower()
            if invoke_by == classe.lower():
                return getattr(decorator, classe)

    def get_object_or_false(self, key: str):
        obj = self.get_object_or_none(key)
        return False if not obj or len(obj) == 0 else obj


class Admonitions:
    def __init__(self, admonitions):
        if admonitions:
            self.items = [AdmonitionItem(*item) for item in admonitions]
        else:
            self.items = []

    def __iter__(self):
        return iter(self.items)


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
    commands: CommandExemples = None
    admonitions: Admonitions = None
    template: Dict[str]


class BaseCommand(DecoratorType, DecorationsFunctions):
    def __init__(self, translation: dict):
        super().__init__(translation, None)
        self.helper = self.get_object("helper")
        self.usage = self.get_object("usage")
        self.description = self.get_object("description")
        self.extras: str = self.get_object_or_none("extras")
        self.commands = CommandExemples(self.get_object_or_false("commands"))
        self.admonitions = Admonitions(self.get_object_or_false("admonitions"))
        self.template: Dict[str] | None = self.get_object_or_none("template")


def resolve_decorator(base: Any, dotted_path: str):
    parts = dotted_path.split(".")
    current = base
    for part in parts:
        current = getattr(current, part)
    return current


class BaseDecorators:
    class TypeChecking(BaseFunctions):
        PlaceHolder: Decorators

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

    Templates: Templates

    class Admin(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)

        class Nada(BaseCommand):
            pass

        class Reload(BaseCommand):
            pass

        class Restart(BaseCommand):
            pass

    class Pipe(BaseCommand):
        pass

    class Afk(BaseCommand):
        pass

    class IsAfk(BaseCommand):
        pass

    class RAfk(BaseCommand):
        pass

    class Alias(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)
            self.helper = self.get_object("helper")
            self.usage = self.get_object("usage")

        class Add(BaseCommand):
            pass

        class Check(BaseCommand):
            pass

        class Copy(BaseCommand):
            pass

        class Describe(BaseCommand):
            pass

        class Edit(BaseCommand):
            pass

        class Link(BaseCommand):
            pass

        class Remove(BaseCommand):
            pass

        class Rename(BaseCommand):
            pass

        class Extras(BaseCommand):
            pass

    class Chance(BaseCommand):
        pass

    class Choice(BaseCommand):
        pass

    class Count(BaseCommand):
        pass

    class RandomColor(BaseCommand):
        pass

    class Reverse(BaseCommand):
        pass

    class RandomLine(BaseCommand):
        pass

    class UpSideDown(BaseCommand):
        pass

    class Scp(BaseCommand):
        pass

    class Wikihow(BaseCommand):
        pass

    class Wikipedia(BaseCommand):
        pass

    class Annotations(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)
            self.helper = self.get_object("helper")
            self.usage = self.get_object("usage")

        class Add(BaseCommand):
            pass

        class Check(BaseCommand):
            pass

        class Delete(BaseCommand):
            pass

    class HyperTranslate(BaseCommand):
        pass

    class Cookies(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)
            self.helper = self.get_object("helper")
            self.usage = self.get_object("usage")

        class Eat(BaseCommand):
            pass

        class Count(BaseCommand):
            pass

        class Gift(BaseCommand):
            pass

        class SlotMachine(BaseCommand):
            pass

        class Stock(BaseCommand):
            pass

        class Top(BaseCommand):
            pass

    class Safebooru(BaseCommand):
        pass

    class PixelSorting(BaseCommand):
        pass

    class BotInfo(BaseCommand):
        pass

    class Ping(BaseCommand):
        pass

    class Color(BaseCommand):
        pass

    class Help(BaseCommand):
        pass

    class Set(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)
            self.helper = self.get_object("helper")
            self.usage = self.get_object("usage")

        class Mention(BaseCommand):
            pass

        class City(BaseCommand):
            pass

        class Nick(BaseCommand):
            pass

        class Color(BaseCommand):
            pass

        class Reminder(BaseCommand):
            pass

    class AccountAge(BaseCommand):
        pass

    class ProfilePicture(BaseCommand):
        pass


class Decorators(BaseFunctions, BaseDecorators):
    def __init__(self, translation: Dict[str, Any], lang: str, fallback: Dict[str, Any] = None):
        super().__init__(translation["decorators"], fallback["decorators"] if fallback else None)
        self._initialize_values(translation, fallback)
        self.lang = lang

    def _initialize_values(self, translation: Dict[str, Any], fallback: Dict[str, Any] = None):
        if fallback:
            extras = BaseFunctions(translation.get("extras", {}), fallback.get("extras", {}))
        else:
            extras = BaseFunctions(translation.get("extras", {}))

        self.populate_subclasses(extras=extras, base_cls=BaseDecorators(), add_to_self=True)

        self.exclude_categories: list[str] = ["NSFW"]
