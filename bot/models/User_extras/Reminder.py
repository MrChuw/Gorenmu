from __future__ import annotations

from tortoise import fields

from models.base import Base, TimestampMixin
from models.timezonefield import DatetimeTzField
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from models.User.User import User

class Reminder(Base, TimestampMixin):
    from_user: User = fields.ForeignKeyField("models.User", related_name="reminder")
    to_user: User = fields.ForeignKeyField("models.User", related_name="reminder_to")
    content = fields.TextField(default=None)
    scheduled_for = DatetimeTzField(default=None, null=True)
    enviado = fields.BooleanField(default=False)

    class Meta:
        table = "reminder"
