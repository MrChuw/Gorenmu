import contextlib
import re
from dataclasses import dataclass
from datetime import UTC, datetime


class DateParse:
    def __init__(self, text: str, span: tuple[int, int], date: datetime):
        self.text = text
        self.span = span
        self.date = date


@dataclass(slots=True)
class DateParserConfig:
    user_formats: list[str] | None = None
    default_order: str = "DM"  # "DM" or "MD"
    base_datetime: datetime | None = None
    allow_past: bool = False
    rollover_future: bool = True
    allow_rollover: bool = False
    strict: bool = True

    def __init__(
        self,
        user_formats: list[str] | None = None,
        default_order: str = "DM",
        base_datetime: datetime | None = None,
        allow_past: bool = False,
        rollover_future: bool = True,
        allow_rollover: bool = False,
        strict: bool = True,
    ):
        self.user_formats = user_formats
        self.default_order = default_order
        self.base_datetime = base_datetime
        self.allow_past = allow_past
        self.rollover_future = rollover_future
        self.allow_rollover = allow_rollover
        self.strict = strict


# ---------- regex ----------

# Ex: 2025/12/12, 12-12-25, 01/05/2025
_TRIPLE_RE = re.compile(r"\b\d{1,4}[/.\-]\d{1,2}[/.\-]\d{1,4}\b")

# Ex: 13/12, 01-05
_DOUBLE_RE = re.compile(r"\b\d{1,2}[/.\-]\d{1,2}\b")


# ---------- helpers ----------


def _normalize_year(y_int: int, y_str: str) -> int:
    if len(y_str) == 4:
        return y_int

    elif len(y_str) == 2 and y_int < 100:
        return 2000 + y_int
    return y_int


def _roll_forward(dt: datetime, base: datetime) -> datetime:
    """Move date to the next possible future occurrence (year + 1)."""
    if dt >= base:
        return dt
    return datetime(dt.year + 1, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tzinfo=dt.tzinfo)


def _try_user_formats(text: str, formats: list[str]) -> datetime | None:
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _try_heuristic_triplet(text: str, tzdata) -> datetime | None:
    parts = re.split(r"[/.\-]", text)
    if len(parts) != 3:
        return None
    # Required order:
    # 1) Y/M/D
    # 2) D/M/Y
    # 3) M/D/Y
    s1, _, s3 = parts
    n1, n2, n3 = map(int, parts)

    candidates = [
        (_normalize_year(n1, s1), n2, n3),  # YMD
        (_normalize_year(n3, s3), n2, n1),  # DMY
        (_normalize_year(n3, s3), n1, n2),  # MDY
    ]
    for y, m, d in candidates:
        with contextlib.suppress(ValueError):
            return datetime(y, m, d, tzinfo=tzdata)
    return None


def _is_valid_or_adjust(
    dt: datetime, base: datetime, allow_past: bool, rollover_future: bool, allow_rollover: bool
) -> datetime | None:
    """
    Validate datetime against base.
    - If past is allowed → accept.
    - If past not allowed:
        - if rollover allowed → roll forward.
        - else → reject.
    """
    if dt >= base.replace(hour=0, minute=0, second=0, microsecond=0) or allow_past:
        return dt

    return _roll_forward(dt, base) if rollover_future and allow_rollover else None


def preprocess_dates(text: str, config: DateParserConfig | None = None) -> tuple[str, list[DateParse]]:
    """
    Extract and parse dates from text, returning:
        - cleaned text (dates removed)
        - list of parsed dates with metadata

    Priority:
        1) user-defined formats (strptime)
        2) heuristic triplets (Y/M/D → D/M/Y → M/D/Y)
        3) partial dates (DD/MM or MM/DD)
    """

    cfg = config or DateParserConfig()
    user_formats = cfg.user_formats
    default_order = cfg.default_order
    base_datetime = cfg.base_datetime
    allow_past = cfg.allow_past
    rollover_future = cfg.rollover_future
    allow_rollover = cfg.allow_rollover
    strict = cfg.strict

    base = base_datetime or datetime.now(UTC)
    year_default = base.year

    parsed: list[DateParse] = []
    cleaned = text
    offset = 0

    amount = text.count("/")
    matches = list(_TRIPLE_RE.finditer(text))

    if amount == 1:
        matches = list(_DOUBLE_RE.finditer(text))
    elif amount == 2:
        matches = list(_TRIPLE_RE.finditer(text))

    if not strict:
        matches = list(_TRIPLE_RE.finditer(text)) + list(_DOUBLE_RE.finditer(text))

    matches.sort(key=lambda _match: _match.start())

    for match in matches:
        raw = match.group(0)
        dt: datetime | None = None

        # ---- 1) User format ----
        if user_formats and (candidate := _try_user_formats(raw, user_formats)):
            dt = _is_valid_or_adjust(candidate, base, allow_past, rollover_future, allow_rollover=allow_rollover)

        # ---- 2) heuristic triplet ----
        if (not dt and raw.count("/") + raw.count("-") + raw.count(".") == 2) and (
            candidate := _try_heuristic_triplet(raw, tzdata=base.tzinfo)
        ):
            dt = _is_valid_or_adjust(candidate, base, allow_past, rollover_future, allow_rollover=allow_rollover)

        # ---- 3) parcial (DD/MM ou MM/DD) ----
        if not dt:
            parts = re.split(r"[/.\-]", raw)
            if len(parts) == 2:
                a, b = map(int, parts)
                with contextlib.suppress(ValueError):
                    candidate = (
                        datetime(year_default, b, a, tzinfo=base.tzinfo)
                        if default_order.upper() == "DM"
                        else datetime(year_default, a, b, tzinfo=base.tzinfo)
                    )
                    dt = _is_valid_or_adjust(candidate, base, allow_past, rollover_future, allow_rollover=True)

        if not dt:
            continue

        start, end = match.span()
        start -= offset
        end -= offset

        cleaned = cleaned[:start] + cleaned[end:]
        offset += end - start

        parsed.append(DateParse(raw, match.span(), dt))

    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned, parsed
