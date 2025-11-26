from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base

if TYPE_CHECKING:
    from bot.models.user import User


class NickHistory(Base):
    nicks: list[str] | fields.TextField = fields.TextField()
    created_at: fields.DatetimeField = fields.DatetimeField(auto_now_add=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="nick_history")

    def __sizeof__(self):
        return len(self.nicks)

    class Meta:
        table = "nick_history"
