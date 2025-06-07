# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from collections import defaultdict
from typing import TYPE_CHECKING

from bot.ext import Command, Context
from bot.translations import BaseCommand, Translation

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class BaseAdmonitions:
    def __init__(self, data: dict):
        self.admonition_type = data.get("admonition_type")
        self.position = data.get("position")
        self.title = data.get("title")
        self.message = data.get("message")

    @staticmethod
    def from_list(data: list):
        return [BaseAdmonitions(d) for d in data]


def custom_format(template, **kwargs):
    placeholders = ["rate", "per", "description", "command_title", "command_name", "prefix", "aliases", "cooldown_type"]

    pattern = re.compile(r"\{(" + "|".join(placeholders) + r")}")

    def replace(match: re.Match[str]) -> str:
        placeholder = match.group(1)
        return str(kwargs.get(placeholder, match.group(0)))

    return pattern.sub(replace, template)


class DynamicDescriptions:
    def __init__(self, bot: Gorenmu):
        self.bot: Gorenmu = bot

    def normal_description(self, command_data: Command) -> dict[str, dict[str, str]]:
        responses = defaultdict(dict)
        cooldown_ = command_data._buckets[0]  # NOQA
        for lang in command_data.decorators:
            language: Translation = self.bot.TranslationManager.languages[lang]
            decorator: BaseCommand = command_data.decorators[lang]
            cooldown_type = language.decorators.Templates.get_bucket_type(cooldown_._key)  # NOQA

            aliases = self._format_aliases(command_data, language.decorators.Templates.alias_template)
            command_body = self._build_command_body(command_data, cooldown_type, aliases, decorator, language)

            responses[lang][command_data.name.lower()] = command_body

        return responses

    def template_description(self, command_data: Command, ctx: Context = None) -> dict[str, dict[str, str]]:
        responses = defaultdict(dict)
        cooldown_ = command_data._buckets[0]  # NOQA
        per = cooldown_._cooldown._per  # NOQA
        rate = cooldown_._cooldown._rate  # NOQA
        prefix = ctx.prefix if ctx else self.bot.config.BotConfig.prefix[0]
        for lang in command_data.decorators:
            decorator: BaseCommand = command_data.decorators[lang]
            description = decorator.description
            language: Translation = self.bot.TranslationManager.languages[lang]
            cooldown_type = language.decorators.Templates.get_bucket_type(cooldown_._key)  # NOQA
            templates = decorator.template
            template = "\n\n\n".join([templates[template] for template in templates])
            template = custom_format(
                template=template,
                rate=rate,
                per=per,
                cooldown_type=cooldown_type,
                description=description,
                command_title=command_data.name.capitalize(),
                command_name=command_data.name.lower(),
                prefix=prefix,
                aliases=", ".join([]),
            )

            responses[lang][command_data.name.lower()] = template

        return responses

    @staticmethod
    def _format_aliases(command_data: Command, alias_template: str):
        if command_data.aliases:
            return alias_template.format(
                command_title=command_data.name.capitalize(), aliases=", ".join(command_data.aliases)
            )
        return ""

    def _build_command_body(
        self, command_data: Command, cooldown_type, aliases, decorator: BaseCommand, language: Translation
    ):
        rate: int = command_data._buckets[0]._cooldown._rate  # NOQA
        per: int = command_data._buckets[0]._cooldown._per  # NOQA
        command_name: str = command_data.name
        prefix = self.bot.config.BotConfig.prefix[0]
        command_body = language.decorators.Templates.template_part1.format(
            command_title=command_name.capitalize(), rate=rate, per=per, cooldown_type=cooldown_type
        )

        command_body += self._add_admonitions(
            decorator.admonitions, "top", language.decorators.Templates.admonition_template
        )
        command_body += language.decorators.Templates.template_part2.format(
            description=decorator.description, aliases=aliases
        )
        command_body += self._add_admonitions(
            decorator.admonitions, "middle", language.decorators.Templates.admonition_template
        )

        if commands := decorator.commands:
            command_body += language.decorators.Templates.template_part3
            command_body += "".join(
                [
                    language.decorators.Templates.command_template.format(
                        prefix=prefix, command_name=command_name.lower(), args=item.args, response=item.response
                    )
                    for item in commands
                ]
            )

        command_body += self._add_admonitions(
            decorator.admonitions, "bottom", language.decorators.Templates.admonition_template
        )

        return command_body

    @staticmethod
    def _add_admonitions(admonitions, position, admonition_template: str):
        if not admonitions:
            return ""
        admonitions = BaseAdmonitions.from_list(admonitions)
        return "".join(
            admonition_template.format(
                type=admonition.admonition_type, title=admonition.title, message=admonition.message
            )
            for admonition in admonitions
            if admonition.position == position
        )
