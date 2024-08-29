# translations/__init__.py
from bot.translations.en import EnDecorators, EnTranslations, Response, BaseClass
from bot.translations.pt_br import PtBrDecorators, PtBrTranslations


class TranslationManager:
    def __init__(self):
        self.languages = {
            "en": (EnDecorators, EnTranslations),
            "pt_br": (PtBrDecorators, PtBrTranslations),
        }
        self.default_language = "en"

    def get_decorators(self, language: str) -> EnDecorators:
        return self.languages.get(language, self.languages[self.default_language])[0]

    def get_translation(self, language: str, key: str) -> EnTranslations:
        translation_class = self.languages.get(language, self.languages[self.default_language])[1]
        return getattr(translation_class, key, key)

    def get_decorator(self, language: str) -> EnDecorators:
        return self.get_decorators(language)

    def get_translations(self, language: str) -> EnTranslations:
        return self.languages.get(language, self.languages[self.default_language])[1]
