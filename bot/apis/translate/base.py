"""base translator class"""

__copyright__ = "Copyright (C) 2020 Nidhal Baccouri"  # NOQA

from abc import abstractmethod
from typing import List, Optional, Union

import aiohttp
from aiohttp_client_cache import CachedSession
from bs4 import BeautifulSoup

from .constants import BASE_URLS, GOOGLE_LANGUAGES_TO_CODES
from .exceptions import (
    InvalidSourceOrTargetLanguage, LanguageNotSupportedException, NotValidLength, NotValidPayload, RequestError,
    TooManyRequests, TranslationNotFound,
)


class GoogleTranslator:
    """
    Abstract class that serve as a base translator for other different translators
    """

    def __init__(
        self,
        session: aiohttp.ClientResponse | CachedSession = aiohttp.ClientResponse,
        base_url: str = BASE_URLS.get("GOOGLE_TRANSLATE"),
        languages: dict = GOOGLE_LANGUAGES_TO_CODES,
        source: str = "auto",
        target: str = "en",
        payload_key: Optional[str] = "q",
        element_tag: Optional[str] = "div",
        element_query=None,
        **url_params,
    ):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        if element_query is None:
            element_query = {"class": "t0"}
        self.session: aiohttp.ClientResponse | CachedSession = session
        self._alt_element_query = {"class": "result-container"}
        self._base_url = base_url
        self._languages = languages
        self._supported_languages = list(self._languages.keys())
        if not source:
            raise InvalidSourceOrTargetLanguage(source)
        if not target:
            raise InvalidSourceOrTargetLanguage(target)

        self._source, self._target = self._map_language_to_code(source, target)
        self._url_params = url_params
        self._element_tag = element_tag
        self._element_query = element_query
        self.payload_key = payload_key
        super().__init__()

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, lang):
        self._source = lang

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, lang):
        self._target = lang

    def _type(self):
        return self.__class__.__name__

    def _map_language_to_code(self, *languages):
        for language in languages:
            if language in self._languages.values() or language == "auto":
                yield language
            elif language in self._languages.keys():
                yield self._languages[language]
            else:
                raise LanguageNotSupportedException(
                    language,
                    message=f"No support for the provided language.\n"
                    f"Please select on of the supported languages:\n"
                    f"{self._languages}",
                )

    def _same_source_target(self) -> bool:
        return self._source == self._target

    def get_supported_languages(self, as_dict: bool = False) -> Union[list, dict]:
        return self._languages if as_dict else self._supported_languages

    def is_language_supported(self, language: str) -> bool:
        return language == "auto" or language in self._languages.keys() or language in self._languages.values()

    @abstractmethod
    async def translate(self, text: str, **kwargs) -> str | None:
        """
        function to translate a text
        @param text: desired text to translate
        @return: str: translated text
        """
        if is_input_valid(text, max_chars=5000):
            text = text.strip()
            if self._same_source_target() or is_empty(text):
                return text
            self._url_params["tl"] = self._target
            self._url_params["sl"] = self._source

            if self.payload_key:
                self._url_params[self.payload_key] = text

            response = await self.session.get(self._base_url, params=self._url_params)
            if response.status == 429:
                raise TooManyRequests()

            if request_failed(status_code=response.status):
                raise RequestError()

            soup = BeautifulSoup(await response.text(), "html.parser")

            element = soup.find(self._element_tag, self._element_query)
            response.close()

            if not element:
                if not (element := soup.find(self._element_tag, self._alt_element_query)):
                    raise TranslationNotFound(text)
            if element.get_text(strip=True) != text.strip():
                return element.get_text(strip=True)
            to_translate_alpha = "".join(ch for ch in text.strip() if ch.isalnum())
            translated_alpha = "".join(ch for ch in element.get_text(strip=True) if ch.isalnum())
            if to_translate_alpha and translated_alpha and to_translate_alpha == translated_alpha:
                self._url_params["tl"] = self._target
                if "hl" not in self._url_params:
                    return text.strip()
                del self._url_params["hl"]
                return await self.translate(text)

        return None

    async def _translate_batch(self, batch: List[str], **kwargs) -> List[str]:
        """
        translate a list of texts
        @param batch: list of texts you want to translate
        @return: list of translations
        """
        if not batch:
            raise Exception("Enter your text list that you want to translate")
        arr = []
        for text in batch:
            translated = await self.translate(text, **kwargs)
            arr.append(translated)
        return arr

    async def translate_batch(self, batch: List[str], **kwargs) -> List[str]:
        """
        translate a list of texts
        @param batch: list of texts you want to translate
        @return: list of translations
        """
        return await self._translate_batch(batch, **kwargs)


def is_empty(text: str) -> bool:
    return not text


def request_failed(status_code: int) -> bool:
    """Check if a request has failed or not.
    A request is considered successfull if the status code is in the 2** range.

    Args:
        status_code (int): status code of the request

    Returns:
        bool: indicates request failure
    """
    return status_code > 299 or status_code < 200


def is_input_valid(text: str, min_chars: int = 0, max_chars: Optional[int] = None) -> bool:
    """
    validate the target text to translate
    @param min_chars: min characters
    @param max_chars: max characters
    @param text: text to translate
    @return: bool
    """

    if not isinstance(text, str):
        raise NotValidPayload(text)
    if max_chars and (not min_chars <= len(text) < max_chars):
        raise NotValidLength(text, min_chars, max_chars)

    return True
