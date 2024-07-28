from __future__ import annotations

from tortoise import fields
from datetime import datetime
from bot.models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from bot.models.User import User


class ImgurAggregate(Base):
    created_at: Union[datetime, fields.DatetimeField] = fields.DatetimeField(auto_now_add=True)
    link: Union[str, fields.TextField] = fields.TextField()

    user: User = fields.ForeignKeyField("models.User", related_name="ImgurAggregate")

    class Meta:
        table = "imgur_aggregate"
