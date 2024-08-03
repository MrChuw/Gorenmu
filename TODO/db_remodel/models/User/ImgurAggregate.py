from __future__ import annotations

from tortoise import fields

from models.base import Base
from models.timezonefield import DatetimeTzField
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from models.User.User import User


class Imgur_agregado(Base):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="imgur_agregado"
    )
    created_at = DatetimeTzField(auto_now_add=True)
    link = fields.TextField()

    class Meta:
        table = "imgur_agregado"
