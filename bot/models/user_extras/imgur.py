from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base

if TYPE_CHECKING:
    from bot.models.user import User


class Imgur(Base):
    created_at: fields.DatetimeField = fields.DatetimeField(auto_now_add=True)
    link: fields.TextField = fields.TextField()

    user: User = fields.ForeignKeyField("models.User", related_name="Imgur")

    class Meta:
        table = "imgur"

    @staticmethod
    async def duplicates():
        return await Imgur.all().values("link")
