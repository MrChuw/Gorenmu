from __future__ import annotations

from tortoise import fields

from bot.models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from bot.models.User import User






class Bug(Base, TimestampMixin):
    content: Union[str, fields.TextField] = fields.TextField()

    viewed: Union[bool, fields.BooleanField] = fields.BooleanField(default=False)
    response: Union[str, fields.TextField] = fields.TextField(default=None, null=True)
    reminded: Union[bool, fields.BooleanField] = fields.BooleanField(default=False)

    user: User = fields.ForeignKeyField("models.User", related_name="bug")

    class Meta:
        table = "bug"
