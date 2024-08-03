# -*- coding: utf-8 -*-

import datetime
import functools
import warnings
from typing import Any, Optional, Type, TYPE_CHECKING, TypeVar, Union

from tortoise import timezone
from tortoise.exceptions import ConfigurationError
from tortoise.fields.base import Field
from tortoise.timezone import get_timezone, get_use_tz, localtime

try:
    from ciso8601 import parse_datetime
except ImportError:
    from iso8601 import parse_date

    parse_datetime = functools.partial(parse_date, default_timezone=None)

if TYPE_CHECKING:
    from tortoise.models import Model

DatetimeFieldQueryValueType = TypeVar("DatetimeFieldQueryValueType", datetime.datetime, int, float, str)


class DatetimeTzField(Field[datetime.datetime], datetime.datetime):
    """
    Datetime field.

    ``auto_now`` and ``auto_now_add`` is exclusive.
    You can opt to set neither or only ONE of them.

    ``auto_now`` (bool):
            Always set to ``datetime.utcnow()`` on save.
    ``auto_now_add`` (bool):
            Set to ``datetime.utcnow()`` on first save only.
    """

    SQL_TYPE = "TIMESTAMP"

    class _db_mysql:
        SQL_TYPE = "DATETIME(6)"

    class _db_postgres:
        SQL_TYPE = "TIMESTAMPTZ"

    class _db_mssql:
        SQL_TYPE = "DATETIME2"

    class _db_oracle:
        SQL_TYPE = "TIMESTAMP WITH TIME ZONE"

    def __init__(self, auto_now: bool = False, auto_now_add: bool = False, **kwargs: Any) -> None:
        if auto_now_add and auto_now:
            raise ConfigurationError("You can choose only 'auto_now' or 'auto_now_add'")
        super().__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now | auto_now_add

    def to_python_value(self, value: Any) -> Optional[datetime.datetime]:
        if value is not None:
            if isinstance(value, datetime.datetime):
                value = value
            elif isinstance(value, int):
                value = datetime.datetime.fromtimestamp(value)
            else:
                value = parse_datetime(value)
            if timezone.is_naive(value):
                value = timezone.make_aware(value, get_timezone())
            else:
                value = localtime(value)
        self.validate(value)
        return value

    def to_db_value(
        self, value: Optional[DatetimeFieldQueryValueType], instance: "Union[Type[Model], Model]"
    ) -> Optional[DatetimeFieldQueryValueType]:
        # Only do this if it is a Model instance, not class. Test for guaranteed instance var
        if hasattr(instance, "_saved_in_db") and (
            self.auto_now or (self.auto_now_add and getattr(instance, self.model_field_name) is None)
        ):
            now = timezone.now()
            setattr(instance, self.model_field_name, now)
            return now  # type:ignore[return-value]
        if value is not None:
            if isinstance(value, datetime.datetime) and get_use_tz():
                if timezone.is_naive(value):
                    warnings.warn(
                        "DateTimeField %s received a naive datetime (%s)"
                        " while time zone support is active." % (self.model_field_name, value),
                        RuntimeWarning,
                    )
                    value = timezone.make_aware(value, "UTC")
        self.validate(value)
        return value

    @property
    def constraints(self) -> dict:
        data = {}
        if self.auto_now_add:
            data["readOnly"] = True
        return data

    def describe(self, serializable: bool) -> dict:
        desc = super().describe(serializable)
        desc["auto_now_add"] = self.auto_now_add
        desc["auto_now"] = self.auto_now
        return desc
