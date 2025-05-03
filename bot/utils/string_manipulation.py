# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import logging
import random
import re
from datetime import datetime
from string import ascii_letters, digits
from typing import Optional, Union

from emoji import demojize
from unidecode import unidecode

from bot.exceptions import InvalidUsername

letters_and_digits = ascii_letters + digits


class StringTools:
    @staticmethod
    def datetime2str(target: datetime) -> str:
        return target.isoformat()

    @staticmethod
    def dict2str(target: Optional[dict]) -> str:
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
        with open(target, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        return random.choice(lines)

    @staticmethod
    def number2str(target: Union[int, float]) -> Optional[str]:
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
    def str2dict(target: Optional[str]) -> dict:
        try:
            return json.loads(target)
        except json.JSONDecodeError as e:
            logging.info(e)
            return {}

    @staticmethod
    def str2float(target: Optional[str]) -> Optional[float]:
        try:
            return float(target.replace(",", "."))
        except ValueError:
            return None
        except TypeError:
            return None
        except Exception as e:
            logging.info(e)
            return None

    @staticmethod
    def str2int(target: Optional[str]) -> Optional[int]:
        try:
            return int(target)
        except ValueError:
            return None
        except TypeError:
            return None
        except Exception as e:
            logging.info(e)
            return None

    @staticmethod
    def str2hex(target: Optional[str]) -> Optional[str]:
        if not target:
            return None
        return match[0] if (match := re.match(r"#[0-9A-Fa-f]{6}$", target)) else None

    @staticmethod
    def str2name(target: str, default: Optional[str] = None) -> Optional[str]:
        if not target:
            return default or None
        if target[0] == "@":
            target = target[1:]
        if target[-1] == ",":
            target = target[:-1]
        if target.replace("_", "").isalnum() and unidecode(target) == target:
            return target.lower()
        raise InvalidUsername

    @staticmethod
    def tpl2str(target: Optional[tuple]) -> str:
        try:
            return json.dumps(target)
        except Exception as e:
            logging.warning(e)
            return ""

    @staticmethod
    def tpl2str2(target: Optional[tuple]) -> str:
        try:
            # return str(target)
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
            "▉-⯯"  # I need Unicode Character “█” (U+2588)
            "✂-➰"
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
            "️"  # dingbats
            "〰"
            "⌛"
            "⌨"
            ""
            "⏩"
            "⏪"
            "⏫"
            "⏬"
            "⏭"
            "⏮"
            "⏯"
            "⏰"
            "⏱"
            "⏲"
            "⏳"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r"", string)

    @staticmethod
    def str_to_hex(value: str) -> str:
        return "".join(x for x in value if x in letters_and_digits).encode().hex()

    @staticmethod
    def json_to_dict(filename: str) -> Union[dict, list]:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def str2url(target: str) -> Optional[str]:
        return re.search(r"([0-9a-zA-Z]*\.[a-zA-Z]{2,3})", target)

    @staticmethod
    def is_birthday(date: str) -> bool:
        return "ano" in date and not any(x in date for x in ["mês", "meses", "semana", "dia"])
