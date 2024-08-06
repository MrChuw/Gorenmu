# translations/__init__.py
from bot.translations.base import BaseDecorators, BaseTranslations
from bot.translations.en_us import EnUsDecorators, EnUsTranslations
from bot.translations.pt_br import PtBrDecorators, PtBrTranslations
from .base import Response

class TranslationManager:
    def __init__(self):
        self.languages = {
            "en-us": (EnUsDecorators, EnUsTranslations),
            "pt-br": (PtBrDecorators, PtBrTranslations),
        }
        self.default_language = "en-us"

    def get_decorators(self, language: str) -> BaseDecorators:
        return self.languages.get(language, self.languages[self.default_language])[0]

    def get_translation(self, language: str, key: str) -> str:
        translation_class = self.languages.get(language, self.languages[self.default_language])[1]
        return getattr(translation_class, key, key)

    def get_decorator(self, language: str) -> BaseDecorators:
        return self.get_decorators(language)

    def get_translations(self, language: str) -> BaseTranslations:
        return self.languages.get(language, self.languages[self.default_language])[1]
