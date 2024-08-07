# translations/__init__.py
from bot.translations.en_us import EnUsDecorators, EnUsTranslations
from bot.translations.pt_br import PtBrDecorators, PtBrTranslations
from .en_us import Response

class TranslationManager:
    def __init__(self):
        self.languages = {
            "en-us": (EnUsDecorators, EnUsTranslations),
            "pt-br": (PtBrDecorators, PtBrTranslations),
        }
        self.default_language = "en-us"

    def get_decorators(self, language: str) -> EnUsDecorators:
        return self.languages.get(language, self.languages[self.default_language])[0]

    def get_translation(self, language: str, key: str) -> EnUsTranslations:
        translation_class = self.languages.get(language, self.languages[self.default_language])[1]
        return getattr(translation_class, key, key)

    def get_decorator(self, language: str) -> EnUsDecorators:
        return self.get_decorators(language)

    def get_translations(self, language: str) -> EnUsTranslations:
        return self.languages.get(language, self.languages[self.default_language])[1]
