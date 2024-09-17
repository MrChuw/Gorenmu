from __future__ import annotations

from tortoise import fields

from bot.models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from bot.models.User import User

class Reminder(Base, TimestampMixin):
    from_user: User = fields.ForeignKeyField("models.User", related_name="reminder")
    to_user: User = fields.ForeignKeyField("models.User", related_name="reminder_to")
    content = fields.TextField(default=None)
    scheduled_for = fields.DateField(default=None, null=True)
    sent = fields.BooleanField(default=False)

    class Meta:
        table = "reminder"
