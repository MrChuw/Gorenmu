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

from bot.exceptions import (
    InvalidUsername,
)

letters_and_digits = ascii_letters + digits


def datetime2str(target: datetime) -> str:
    return target.isoformat()


def dict2str(target: Optional[dict]) -> str:
    try:
        return json.dumps(target, ensure_ascii=False)
    except Exception:
        return ""


def emoji2str(target: str) -> str:
    return demojize(target)


def txt2randomline(target: str) -> str:
    with open(target, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return random.choice(lines)


def number2str(target: Union[int, float]) -> Optional[str]:
    if isinstance(target, int):
        return f"{target:,d}".replace(",", ".")
    if isinstance(target, float):
        return f"{target:,.2f}"[::-1].replace(",", ".").replace(".", ",", 1)[::-1]


def str2ascii(target: str) -> str:
    return unidecode(target).lower().strip()


def str2datetime(target: str) -> datetime:
    return datetime.fromisoformat(target)


def str2dict(target: Optional[str]) -> dict:
    try:
        return json.loads(target)
    except Exception:
        return {}


def str2float(target: Optional[str]) -> Optional[float]:
    try:
        return float(target.replace(",", "."))
    except Exception:
        return None


def str2int(target: Optional[str]) -> Optional[int]:
    try:
        return int(target)
    except Exception:
        return None


def str2hex(target: Optional[str]) -> Optional[str]:
    if not target:
        return None
    if match := re.match(r"#(?:[0-9A-Fa-f]{6})$", target):
        return match.group(0)


def str2name(target: str, default: Optional[str] = None) -> Optional[str]:
    if not target and default:
        return default
    if target:
        if target[0] == "@":
            target = target[1:]
        if target[-1] == ",":
            target = target[:-1]
        if target.replace("_", "").isalnum() and unidecode(target) == target:
            return target.lower()
    raise InvalidUsername()


def tpl2str(target: Optional[tuple]) -> str:
    try:
        return json.dumps(target)
    except Exception as e:
        logging.warning(e)
        return ""


def tpl2str2(target: Optional[tuple]) -> str:
    try:
        # return str(target)
        return json.dumps(target)
    except Exception as e:
        logging.warning(e)
        return ""


def remove_emoji(string: str) -> str:
    emoji_pattern = re.compile("["
                               "\U0001F600-\U0001F64F"  # emoticons
                               "\U0001F300-\U0001F5FF"  # symbols & pictographs
                               "\U0001F680-\U0001F6FF"  # transport & map symbols
                               "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "\U00002500-\U00002587"  # chinese char
                               "\U00002589-\U00002BEF"  # I need Unicode Character “█” (U+2588)
                               "\U00002702-\U000027B0"
                               "\U00002702-\U000027B0"
                               "\U000024C2-\U00002587"
                               "\U00002589-\U0001F251"
                               "\U0001f926-\U0001f937"
                               "\U00010000-\U0010ffff"
                               "\u2640-\u2642"
                               "\u2600-\u2B55"
                               "\u200d"
                               "\u23cf"
                               "\u23e9"
                               "\u231a"
                               "\ufe0f"  # dingbats
                               "\u3030"
                               "\u231b"
                               "\u2328"
                               "\u23cf"
                               "\u23e9"
                               "\u23ea"
                               "\u23eb"
                               "\u23ec"
                               "\u23ed"
                               "\u23ee"
                               "\u23ef"
                               "\u23f0"
                               "\u23f1"
                               "\u23f2"
                               "\u23f3"
                               "]+", flags=re.UNICODE, )
    return emoji_pattern.sub(r"", string)


def str_to_hex(value: str) -> str:
    return "".join(x for x in value if x in letters_and_digits).encode().hex()


def json_to_dict(filename: str) -> Union[dict, list]:
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def str2url(target: str) -> Optional[str]:
    return re.search(r"([0-9a-zA-Z]*\.[a-zA-Z]{2,3})", target)


def is_birthday(date: str) -> bool:
    return "ano" in date and not any(x in date for x in ["mês", "meses", "semana", "dia"])
