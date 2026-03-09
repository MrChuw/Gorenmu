from __future__ import annotations

import datetime
import hashlib
import random
import string
from collections.abc import Callable, Coroutine, Iterable, Sequence
from contextlib import contextmanager, suppress
from enum import Enum, StrEnum
from typing import TYPE_CHECKING, Any, TypeVar

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


if TYPE_CHECKING:
    from bot.bot import Gorenmu


class RandomUtils:
    def __init__(self, seed: int | None = None):
        self._rng = random.Random(seed)

    @staticmethod
    def _make_seed(*values: Any, daily: bool = False, mod: int | None = None) -> int:
        seed_string = "".join(str(v).lower() for v in values)
        if daily:
            seed_string += str(datetime.date.today().toordinal())
        hash_digest = hashlib.sha256(seed_string.encode()).hexdigest()
        return int(hash_digest, 16) % mod if mod else int(hash_digest, 16)

    @classmethod
    def seeded(cls, *values: Any, daily: bool = False, mod: int | None = None) -> RandomUtils:
        seed = cls._make_seed(*values, daily=daily, mod=mod)
        return cls(seed)

    def reseed(self, *values: Any, daily: bool = False, mod: int | None = None):
        seed = self._make_seed(*values, daily=daily, mod=mod)
        self._rng.seed(seed)
        return self

    @contextmanager
    def temp_seed(self, *values: Any, daily: bool = False, mod: int | None = None):
        old_state = self._rng.getstate()
        try:
            seed = self._make_seed(*values, daily=daily, mod=mod)
            self._rng.seed(seed)
            yield self
        finally:
            self._rng.setstate(old_state)

    def random_line_from_txt(self, filename: str) -> str:
        with open(filename, encoding="utf-8") as f:
            return self._rng.choice(f.read().splitlines())

    def random_number(self, *, min_value: int = 0, max_value: int = 100, div: int = 1) -> float:
        if div != 1:
            return self._rng.randint(min_value, max_value) / div
        return self._rng.randint(min_value, max_value)

    def random_float(self, *, min_value: float = 0.0, max_value: float = 1.0, precision: int = 2) -> float:
        value = self._rng.uniform(min_value, max_value)
        return round(value, precision)

    def random_bool(self, true_chance: float = 0.5) -> bool:
        return self._rng.random() < true_chance

    def random_choice(self, options: str | list[str], *, sep: str | None = None) -> str:
        if isinstance(options, str):
            options = options.split(sep)
        return self._rng.choice(options)

    def random_choices(
        self, options: str | list[str], *, sep: str | None = None, k: int = 1, w: Sequence[float] | None = None
    ) -> list[str]:
        if isinstance(options, str) and sep:
            options = options.split(sep)
        return self._rng.choices(options, weights=w, k=k)

    def random_sample(self, options: Sequence[Any], k: int) -> list[Any]:
        return self._rng.sample(options, k)

    def random_sort(self, options: list[Any]) -> list[Any]:
        self._rng.shuffle(options)
        return options

    def random_string(
        self, length: int = 8, *, letters: bool = True, digits: bool = True, symbols: bool = False
    ) -> str:
        chars = ""
        if letters:
            chars += string.ascii_letters
        if digits:
            chars += string.digits
        if symbols:
            chars += string.punctuation
        return "".join(self._rng.choice(chars) for _ in range(length))

    def random_hex(self, length: int = 6) -> str:
        return "".join(self._rng.choice("0123456789abcdef") for _ in range(length))

    def random_color_rgb(self) -> tuple[int, int, int]:
        return self._rng.randint(0, 255), self._rng.randint(0, 255), self._rng.randint(0, 255)

    def random_element(self, iterable: Iterable[Any], default: Any = None) -> Any:
        items = list(iterable)
        return self._rng.choice(items) if items else default

    def random_weighted_dict(self, data: dict[Any, float]) -> Any:
        keys = list(data.keys())
        weights = list(data.values())
        return self._rng.choices(keys, weights=weights, k=1)[0]

    def random_gauss(self, mu: float = 0.0, sigma: float = 1.0, precision: int = 2) -> float:
        return round(self._rng.gauss(mu, sigma), precision)

    def random_date(self, start_year: int = 2020, end_year: int = 2026) -> str:
        month = self._rng.randint(1, 12)
        day = self._rng.randint(1, 28)
        return f"{self._rng.randint(start_year, end_year)}-{month:02d}-{day:02d}"

    def random_int(self, min_value: int = 0, max_value: int = 100, step: int = 1) -> int:
        if step <= 0:
            raise ValueError("The step must be positive.")
        range_size = (max_value - min_value) // step + 1
        return min_value + self._rng.randint(0, range_size - 1) * step

    # region Hide.

    def random_ipv4(self) -> str:
        return ".".join(str(self._rng.randint(0, 255)) for _ in range(4))

    def random_ipv6(self) -> str:
        return ":".join(self._rng.choice("0123456789abcdef") * 4 for _ in range(8))

    def random_mac(self, delimiter: str = ":") -> str:
        return delimiter.join(self.random_hex(2) for _ in range(6))

    def random_uuid(self) -> str:
        bytes_val = self.random_bytes(16)
        bytes_val = bytearray(bytes_val)
        bytes_val[6] = (bytes_val[6] & 0x0F) | 0x40
        bytes_val[8] = (bytes_val[8] & 0x3F) | 0x80
        hex_str = bytes_val.hex()
        return f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:32]}"

    def random_email(self, domains: list[str] | None = None) -> str:
        if domains is None:
            domains = ["test.org", "demo.net", "mail.co", "gmail.com", "outlook.com", "yahoo.com", "example.com"]
        local_part = self.random_string(8, letters=True, digits=True, symbols=False)
        local_part += self._rng.choice([".", "_", "-"]) + self.random_string(4, letters=True, digits=False)
        domain = self._rng.choice(domains)
        return f"{local_part}@{domain}"

    def random_username(self, length: int = 8) -> str:
        chars = string.ascii_lowercase + string.digits + "_"
        return "".join(self._rng.choice(chars) for _ in range(length))

    def random_full_name(self) -> str:
        first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]
        last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
        ]
        return f"{self._rng.choice(first_names)} {self._rng.choice(last_names)}"

    def random_phone(self, country_code: str = "+1", format: str = "xxx-xxx-xxxx") -> str:
        result = []
        for ch in format:
            if ch == "x":
                result.append(str(self._rng.randint(0, 9)))
            else:
                result.append(ch)
        return f"{country_code} " + "".join(result)

    def random_datetime(self, start: str = "2020-01-01", end: str = "2025-12-31", time_format: bool = True) -> str:
        start_date = datetime.date.fromisoformat(start)
        end_date = datetime.date.fromisoformat(end)
        delta_days = (end_date - start_date).days
        random_days = self._rng.randint(0, delta_days)
        random_date = start_date + datetime.timedelta(days=random_days)

        if time_format:
            hour = self._rng.randint(0, 23)
            minute = self._rng.randint(0, 59)
            second = self._rng.randint(0, 59)
            return f"{random_date}T{hour:02d}:{minute:02d}:{second:02d}"
        return random_date.isoformat()

    def random_lorem_ipsum(self, paragraphs: int = 1, sentences_per_paragraph: int = 3) -> str:
        words = [
            "lorem",
            "ipsum",
            "dolor",
            "sit",
            "amet",
            "consectetur",
            "adipiscing",
            "elit",
            "sed",
            "do",
            "eiusmod",
            "tempor",
            "incididunt",
            "ut",
            "labore",
            "et",
            "dolore",
            "magna",
            "aliqua",
            "enim",
            "ad",
            "minim",
            "veniam",
            "quis",
            "nostrud",
            "exercitation",
            "ullamco",
            "laboris",
            "nisi",
            "aliquip",
            "ex",
            "ea",
            "commodo",
        ]
        result = []
        for _ in range(paragraphs):
            sentences = []
            for _ in range(sentences_per_paragraph):
                sentence_len = self._rng.randint(5, 12)
                sentence_words = self._rng.choices(words, k=sentence_len)
                sentence = " ".join(sentence_words).capitalize() + "."
                sentences.append(sentence)
            result.append(" ".join(sentences))
        return "\n\n".join(result)

    def random_subset(self, options: Sequence[Any], *, min_k: int = 1, max_k: int | None = None) -> list[Any]:
        if not options:
            return []
        if max_k is None:
            max_k = len(options)
        k = self._rng.randint(min_k, max_k)
        return self._rng.sample(list(options), k)

    def random_enum(self, enum_class: type[EnumT]) -> EnumT:
        return self._rng.choice(list(enum_class))

    def random_bytes(self, length: int) -> bytes:
        return self._rng.getrandbits(length * 8).to_bytes(length, byteorder="big")

    def random_hex_color(self) -> str:
        return f"#{self.random_hex(6)}"

    def random_password(
        self,
        length: int = 12,
        lowercase: bool = True,
        uppercase: bool = True,
        digits: bool = True,
        symbols: bool = False,
        min_lower: int = 1,
        min_upper: int = 1,
        min_digits: int = 1,
        min_symbols: int = 0,
    ) -> str:
        groups = []
        if lowercase:
            groups.append((string.ascii_lowercase, min_lower))
        if uppercase:
            groups.append((string.ascii_uppercase, min_upper))
        if digits:
            groups.append((string.digits, min_digits))
        if symbols:
            groups.append((string.punctuation, min_symbols))

        if not groups:
            raise ValueError("At least one group of characters must be active.")

        total_min = sum(min_chars for _, min_chars in groups)
        if total_min > length:
            raise ValueError("The sum of the minimum values exceeds the total password length.")

        password_chars = []
        for chars, min_count in groups:
            password_chars.extend(self._rng.choices(chars, k=min_count))

        all_chars = "".join(chars for chars, _ in groups)
        remaining = length - len(password_chars)
        password_chars.extend(self._rng.choices(all_chars, k=remaining))

        self._rng.shuffle(password_chars)
        return "".join(password_chars)

    # endregion

    # --- Deterministic/Seeded Methods ---
    @staticmethod
    async def _pick_dynamic[T](
        coro: Coroutine[Any, Any, Any],
        fallback: T | Sequence[T],
        *,
        picker: Callable[[Sequence[T]], T],
        bot: Gorenmu,
    ) -> T:
        if bot.mock:
            return picker(fallback) if isinstance(fallback, Sequence) else fallback

        with suppress(Exception):
            results = await coro

            if isinstance(results, (list, tuple, set)) and (items := list(results)):
                return picker(items)

            if results is not None:
                return results  # type: ignore

        return picker(fallback) if isinstance(fallback, Sequence) else fallback

    class TimeBasis(StrEnum):
        SECOND_30 = "30s"
        MINUTE = "minute"
        MINUTE_5 = "5m"
        MINUTE_10 = "10m"
        MINUTE_15 = "15m"
        HOUR = "hour"
        HOUR_6 = "6h"
        HOUR_12 = "12h"
        DAILY = "daily"
        WEEKLY = "weekly"
        MONTHLY = "monthly"
        YEARLY = "yearly"

    def get_seeded_percentage(
        self,
        *seed_values: Any,
        mod: int = 101,
        time_basis: TimeBasis | None = None,
    ) -> int:
        extra = ""
        now = datetime.datetime.now()

        match time_basis:
            case RandomUtils.TimeBasis.SECOND_30:
                extra = f"{now.strftime('%Y-%m-%d-%H-%M')}-{now.second // 30}"
            case RandomUtils.TimeBasis.MINUTE:
                extra = now.strftime("%Y-%m-%d-%H-%M")
            case RandomUtils.TimeBasis.MINUTE_5:
                extra = f"{now.strftime('%Y-%m-%d-%H')}-{now.minute // 5}"
            case RandomUtils.TimeBasis.MINUTE_10:
                extra = f"{now.strftime('%Y-%m-%d-%H')}-{now.minute // 10}"
            case RandomUtils.TimeBasis.MINUTE_15:
                extra = f"{now.strftime('%Y-%m-%d-%H')}-{now.minute // 15}"
            case RandomUtils.TimeBasis.HOUR:
                extra = now.strftime("%Y-%m-%d-%H")
            case RandomUtils.TimeBasis.HOUR_6:
                extra = f"{now.strftime('%Y-%m-%d')}-{now.hour // 6}"
            case RandomUtils.TimeBasis.HOUR_12:
                extra = f"{now.strftime('%Y-%m-%d')}-{now.hour // 12}"
            case RandomUtils.TimeBasis.DAILY:
                extra = now.strftime("%Y-%j")
            case RandomUtils.TimeBasis.WEEKLY:
                extra = now.strftime("%Y-%U")
            case RandomUtils.TimeBasis.MONTHLY:
                extra = now.strftime("%Y-%m")
            case RandomUtils.TimeBasis.YEARLY:
                extra = now.strftime("%Y")

        if extra:
            seed_values = (*seed_values, extra)

        seed_int = self._make_seed(*seed_values)
        return seed_int % mod

    @staticmethod
    def pick_by_percentage[T](options: Sequence[T], percentage: float | int) -> T:
        if not options:
            raise ValueError("The options sequence cannot be empty.")
        p = max(0.0, min(100.0, float(percentage)))
        idx = round((p / 100.0) * (len(options) - 1))
        return options[idx]

    @staticmethod
    def map_percentage_to_range(percentage: float | int, min_value: int, max_value: int) -> int:
        p = max(0.0, min(100.0, float(percentage)))
        span = max_value - min_value
        return min_value + round((p / 100.0) * span)

    async def pick_dynamic[T](self, coro: Coroutine[Any, Any, Any], fallback: T | Sequence[T], bot: Gorenmu) -> T:
        return await self._pick_dynamic(coro, fallback, picker=self._rng.choice, bot=bot)

    async def pick_dynamic_seeded[T](
        self,
        coro: Coroutine[Any, Any, Any],
        fallback: T | Sequence[T],
        *seed_values: Any,
        mod: int = 101,
        time_basis: TimeBasis | None = None,
        bot: Gorenmu,
    ) -> T:
        percentage = self.get_seeded_percentage(*seed_values, mod=mod, time_basis=time_basis)
        return await self.pick_dynamic_by_percentage(coro, fallback, float(percentage), bot)

    async def pick_dynamic_by_percentage[T](
        self, coro: Coroutine[Any, Any, Any], fallback: T | Sequence[T], percentage: float, bot: Gorenmu
    ) -> T:
        def picker(seq: Sequence[T]) -> T:
            return self.pick_by_percentage(seq, percentage)

        return await self._pick_dynamic(coro, fallback, picker=picker, bot=bot)
