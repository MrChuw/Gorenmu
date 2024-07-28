from __future__ import annotations

from datetime import datetime
from tortoise import fields

from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from bot.models import User

from bot.models.base import Base, TimestampMixin, TextFieldStr

class Status(Base, TimestampMixin):
    online: Union[bool, fields.BooleanField] = fields.BooleanField(default=True)
    alias: Union[str, fields.TextField] = fields.TextField(null=True)
    message: Union[str, fields.TextField] = fields.TextField(null=True)
    updated_at: Union[datetime, fields.DatetimeField] = fields.DatetimeField(null=True)
    user: User = fields.ForeignKeyField("models.User", related_name="status")

    class Meta:
        table = "status"























