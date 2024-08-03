from __future__ import annotations

from tortoise import fields

from models.base import Base
from models.timezonefield import DatetimeTzField
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from models.User.User import User


class Imgur(Base):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="imgur"
    )
    created_at = DatetimeTzField(auto_now_add=True)
    link = fields.TextField()

    class Meta:
        table = "imgur"

    async def repetidos(self):
        return await Imgur.all().values("link")
