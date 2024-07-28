from __future__ import annotations

from tortoise import fields

from bot.models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from bot.models.User import User


class BotsIgnore(Base, TimestampMixin):
    active: Union[bool, fields.BooleanField] = fields.BooleanField(default=True)
    user: User = fields.ForeignKeyField("models.User", related_name="user_bot")

    class Meta:
        unique_together = ("id", "user")
        table = "bots_ids"
