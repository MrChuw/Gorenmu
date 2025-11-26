from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.user import User


class Reminder(Base, TimestampMixin):
    from_user: User = fields.ForeignKeyField("models.User", related_name="reminder")
    to_user: User = fields.ForeignKeyField("models.User", related_name="reminder_to")
    content = fields.TextField(default=None)
    scheduled_for = fields.DateField(default=None, null=True)
    sent = fields.BooleanField(default=False)

    class Meta:
        table = "reminder"
