# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import pathlib
from typing import Any, Awaitable, Callable, TYPE_CHECKING, Union

from bot.translations.base_decorators import BaseCommand, BaseDecorators, Decorators
from bot.translations.base_responses import BaseTranslations, Translations
from bot.translations.extras import Activity, Response

if TYPE_CHECKING:
    from bot.ext import Command, Context


def open_file(filepath: pathlib.Path, fallback=None):
    if filepath.exists():
        with open(filepath, "rb") as file:
            return json.load(file)
    with open(fallback, "rb") as file:
        return json.load(file)


base_path = pathlib.Path(__file__).parent / "langs"
afks = Activity(open_file(base_path / "en/extras/activity.json")["Activity"])


def load_langs():
    en_paths = [
        base_path / "en/strings.json",
        base_path / "en/decorators.json",
        base_path / "en/site_stuff.json",
        base_path / "en/extras/cookies.json",
        base_path / "en/extras/activity.json",
        base_path / "en/extras/dungeon.json",
        base_path / "en/extras/games.json",
        base_path / "en/extras/pets.json",
        base_path / "en/extras/weather.json",
    ]

    langs = {
        "en": {
            "strings": open_file(en_paths[0]),
            "decorators": open_file(en_paths[1]),
            "site": open_file(en_paths[2]),
            "extras": {
                "cookies_path": en_paths[3],
                "activity": open_file(en_paths[4]),
                "dungeon": open_file(en_paths[5]),
                "games": open_file(en_paths[6]),
                "pets": open_file(en_paths[7]),
                "weather": open_file(en_paths[8]),
            },
        }
    }
    for lang in base_path.iterdir():
        if lang.name != "en":
            langs[lang.name] = {
                "strings": open_file(base_path / lang.name / "strings.json", en_paths[0]),
                "decorators": open_file(base_path / lang.name / "decorators.json", en_paths[1]),
                "site": open_file(base_path / lang.name / "site_stuff.json", en_paths[2]),
                "extras": {
                    "cookies_path": en_paths[3],  # TODO: Change back.
                    # "cookies_path": base_path / lang.name / "extras/cookies.json",
                    "activity": open_file(base_path / lang.name / "extras/activity.json", en_paths[4]),
                    "dungeon": open_file(base_path / lang.name / "extras/dungeon.json", en_paths[5]),
                    "games": open_file(base_path / lang.name / "extras/games.json", en_paths[6]),
                    "pets": open_file(base_path / lang.name / "extras/pets.json", en_paths[7]),
                    "weather": open_file(base_path / lang.name / "extras/weather.json", en_paths[8]),
                },
            }

    return langs


class Translation:
    def __init__(self, decorators, strings):
        self.decorators: Decorators = decorators
        self.strings: Translations = strings


class TranslationManager:
    def __init__(self):
        langs = load_langs()
        self.en = Translation(Decorators(langs["en"], "en"), Translations(langs["en"], "en"))
        self.languages = {"en": self.en}

        for lang in langs:
            if lang == "en":
                continue
            self.languages[lang] = Translation(
                Decorators(langs[lang], lang, fallback=langs["en"]),
                Translations(langs[lang], lang, fallback=langs["en"]),
            )

        self.default_language = "en"

    def get_decorators(self, language: str) -> Decorators:
        return self.languages.get(language, self.languages[self.default_language]).decorators

    def get_translation(self, language: str, key: str) -> Translations:
        translation_class = self.languages.get(language, self.languages[self.default_language]).strings
        return getattr(translation_class, key, key)

    def get_decorator(self, command: Union[Command, Callable[..., Awaitable]], ctx: Context) -> BaseCommand:
        decorators = self.get_decorators(ctx.user.language or ctx.bot.config.default_lang)
        return resolve_decorator(decorators, command.decorator_path)

    def get_translations(self, language: str) -> Translations:
        return self.languages.get(language, self.languages[self.default_language]).strings


def resolve_decorator(base: Any, dotted_path: str):
    parts = dotted_path.split(".")
    current = base
    for part in parts:
        current = getattr(current, part)
    return current
