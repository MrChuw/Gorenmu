# translations/__init__.py
from bot.translations.base_responses import Translations, BaseTranslations
from bot.translations.base_decorators import Decorators, BaseDecorators, BaseCommand
from bot.translations.extras import Response
import json
import pathlib


def open_file(filepath: pathlib.Path, fallback=None):
    if filepath.exists():
        with open(filepath, "rb") as file:
            return json.load(file)
    with open(fallback, "rb") as file:
        return json.load(file)


def load_langs():
    base_path = pathlib.Path("bot/translations/langs")
    langs = {}

    en_paths = [
            base_path / "en/strings.json",
            base_path / "en/decorators.json",
            base_path / "en/extras/cookies.json",
            base_path / "en/extras/activity.json",
            base_path / "en/extras/dungeon.json",
            base_path / "en/extras/games.json",
            base_path / "en/extras/pets.json",
            base_path / "en/extras/weather.json",
    ]

    langs["en"] = {
            "strings": open_file(en_paths[0]),
            "decorators": open_file(en_paths[1]),
            "extras": {
                    "cookies_path": en_paths[2],
                    "activity": open_file(en_paths[3]),
                    "dungeon": open_file(en_paths[4]),
                    "games": open_file(en_paths[5]),
                    "pets": open_file(en_paths[6]),
                    "weather": open_file(en_paths[7]),
            }
    }

    for lang in base_path.iterdir():
        if lang.name != "en":
            langs[lang.name] = {
                    "strings": open_file(base_path / lang.name / "strings.json", en_paths[0]),
                    "decorators": open_file(base_path / lang.name / "decorators.json", en_paths[1]),
                    "extras": {
                            "cookies_path": base_path / lang.name / "extras/cookies.json",
                            "activity": open_file(base_path / lang.name / "extras/activity.json", en_paths[3]),
                            "dungeon": open_file(base_path / lang.name / "extras/dungeon.json", en_paths[4]),
                            "games": open_file(base_path / lang.name / "extras/games.json", en_paths[5]),
                            "pets": open_file(base_path / lang.name / "extras/pets.json", en_paths[6]),
                            "weather": open_file(base_path / lang.name / "extras/weather.json", en_paths[7]),
                    }
            }

    return langs


class Translation:
    def __init__(self, decorators, strings):
        self.decorators = decorators
        self.strings = strings


class TranslationManager:
    def __init__(self, mock: bool = False):
        langs = load_langs()
        self.languages = {}

        self.languages["en"] = Translation(Decorators(langs["en"]), Translations(langs["en"]))

        for lang in langs:
            if lang == "en":
                continue
            self.languages[lang] = Translation(Decorators(langs[lang], langs["en"]), Translations(langs[lang], langs["en"]))

        self.default_language = "en"
        # if mock:
        #     from .en.site_templates import EnSiteTemplates
        #     from .pt_br.site_templates import PtBrSiteTemplates
        #     self.site: dict[str, EnSiteTemplates] = {  # NOQA
        #             "en": EnSiteTemplates,
        #             "pt_br": PtBrSiteTemplates,
        #     }

    def get_decorators(self, language: str) -> Decorators:
        return self.languages.get(language, self.languages[self.default_language]).decorators

    def get_translation(self, language: str, key: str) -> Translations:
        translation_class = self.languages.get(language, self.languages[self.default_language]).strings
        return getattr(translation_class, key, key)

    def get_decorator(self, language: str) -> Decorators:
        return self.get_decorators(language)

    def get_translations(self, language: str) -> Translations:
        return self.languages.get(language, self.languages[self.default_language]).strings
