from __future__ import annotations

import json
import logging
import random
import re
import string
from datetime import datetime
from string import ascii_letters, digits

from emoji import demojize
from unidecode import unidecode
from urlextract import URLExtract

from bot.exceptions import InvalidUsernameError
from bot.utils.singleton import Singleton

letters_and_digits = ascii_letters + digits
url_extractor = URLExtract()


class StringTools(metaclass=Singleton):
    @staticmethod
    def inv_char():
        return chr(int("FE0F", 16))

    @staticmethod
    def start_remove_punctuation(content):
        if content[0] in string.punctuation:
            return StringTools.inv_char() + content
        return content

    @staticmethod
    def datetime2str(target: datetime) -> str:
        return target.isoformat()

    @staticmethod
    def dict2str(target: dict | None) -> str:
        try:
            return json.dumps(target, ensure_ascii=False)
        except TypeError:
            return ""
        except Exception as e:
            logging.info(e)
            return ""

    @staticmethod
    def emoji2str(target: str) -> str:
        return demojize(target)

    @staticmethod
    def txt2randomline(target: str) -> str:
        with open(target, encoding="utf-8") as f:
            lines = f.read().splitlines()
        return random.choice(lines)

    @staticmethod
    def number2str(target: int | float) -> str | None:
        if isinstance(target, int):
            return f"{target:,d}".replace(",", ".")
        if isinstance(target, float):
            return f"{target:,.2f}"[::-1].replace(",", ".").replace(".", ",", 1)[::-1]
        return None

    @staticmethod
    def str2ascii(target: str) -> str:
        return unidecode(target).lower().strip()

    @staticmethod
    def str2datetime(target: str) -> datetime:
        return datetime.fromisoformat(target)

    @staticmethod
    def str2dict(target: str | None) -> dict:
        try:
            return json.loads(target)
        except json.JSONDecodeError as e:
            logging.info(e)
            return {}

    @staticmethod
    def str2float(target: str | None) -> float | None:
        try:
            return float(target.replace(",", "."))
        except (ValueError, TypeError):
            return None
        except Exception as e:
            logging.info(e)
            return None

    @staticmethod
    def str2int(target: str | None) -> int | None:
        try:
            return int(target)
        except (ValueError, TypeError):
            return None
        except Exception as e:
            logging.info(e)
            return None

    @staticmethod
    def str2hex(target: str | None) -> str | None:
        if not target:
            return None
        return match[0] if (match := re.match(r"#[0-9A-Fa-f]{6}$", target)) else None

    @staticmethod
    def str2name(target: str, default: str | None = None) -> str | None:
        if not target:
            return default or None
        if target[0] == "@":
            target = target[1:]
        if target[-1] == ",":
            target = target[:-1]
        if target.replace("_", "").isalnum() and unidecode(target) == target:
            return target.lower()
        raise InvalidUsernameError

    @staticmethod
    def str2name_or(target: str) -> str | None:
        if target[0] == "@":
            target = target[1:]
        if target[-1] == ",":
            target = target[:-1]
        if target.replace("_", "").isalnum() and unidecode(target) == target:
            return target.lower()
        return target

    @staticmethod
    def tpl2str(target: tuple | None) -> str:
        try:
            return json.dumps(target)
        except Exception as e:
            logging.warning(e)
            return ""

    @staticmethod
    def remove_emoji(string: str) -> str:
        emoji_pattern = re.compile(
            "["
            "😀-🙏"  # emoticons
            "🌀-🗿"  # symbols & pictographs
            "🚀-🛿"  # transport & map symbols
            "🇠-🇿"  # flags (iOS)
            "─-▇"  # chinese char
            "▉-⯯"
            "✂-➰"
            "Ⓜ-▇"
            "▉-🉑"
            "🤦-🤷"
            "𐀀-􏿿"
            "♀-♂"
            "☀-⭕"
            "‍"
            "⏏"
            "⌚"
            "️"
            "〰"
            "⌛"
            "⌨"
            "⏩-⏳"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r"", string)

    @staticmethod
    def str_to_hex(value: str) -> str:
        return "".join(x for x in value if x in letters_and_digits).encode().hex()

    @staticmethod
    def json_to_dict(filename: str) -> dict | list:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def str2url(target: str) -> str | None:
        return re.search(r"([0-9a-zA-Z]*\.[a-zA-Z]{2,3})", target)

    @staticmethod
    def find_prefixed_option(options: list[str], prefix: str) -> str | None:
        return next((opt.replace(prefix, "") for opt in options if opt.startswith(prefix)), None)

    def remove_prefixed_option(self, text: str, prefix: str) -> tuple[str, str | None]:
        if option := self.find_prefixed_option(text.split(" "), prefix):
            text = text.replace(f"{prefix}{option}", "").replace("  ", " ")
        return text, option

    @staticmethod
    def extract_and_remove_field(text: str, field: str, default: str | float | None = None) -> tuple[str, str | None]:
        pattern = rf'{field}:(?:"(.*?)"|(\S+))'
        if match := re.search(pattern, text):
            value = match[1] or match[2]
            text = text.replace(match[0], "")
            return text, value
        return text, default

    @staticmethod
    def extract_and_remove_all_fields(text: str, field: str, default: list[str] | None = None) -> tuple[str, list[str]]:
        if default is None:
            default = []
        pattern = rf'{field}:(?:"(.*?)"|(\S+))'
        matches = re.findall(pattern, text)
        values = [m[0] or m[1] for m in matches]
        cleaned_text = re.sub(pattern, "", text).strip()
        return cleaned_text, values or default

    @staticmethod
    def is_int(text: str) -> bool:
        text = text.strip()
        try:
            int(text)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(text: str) -> bool:
        text = text.strip().replace(",", ".")
        try:
            float(text)
            return True
        except ValueError:
            return False

    def to_amount(self, text: str, default: int = 1) -> int | float:
        if not text:
            return default
        text = text.strip().replace(",", ".")
        if self.is_int(text):
            return int(text)
        elif self.is_float(text):
            return float(text)
        return default

    def to_all(self, text: str, amount_available: int, lang_all: list, default: int = 1) -> tuple[int | float, bool]:
        if not text:
            return default, False
        text = text.strip().lower()
        if text in lang_all:
            return amount_available, True
        return self.to_amount(text, default), False

    @staticmethod
    def urls_extract(text: str):
        return url_extractor.find_urls(text=text)
