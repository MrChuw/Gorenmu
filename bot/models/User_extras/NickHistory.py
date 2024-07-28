from __future__ import annotations

from tortoise import fields

from bot.models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from bot.models.User import User


class NickHistory(Base):
    nicks: Union[List[str], fields.TextField] = fields.TextField()
    created_at: fields.DatetimeField = fields.DatetimeField(auto_now_add=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="nick_history"
    )

    def __sizeof__(self):
        return len(self.nicks)

    class Meta:
        table = "nick_history"
