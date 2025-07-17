from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.User import User


class Pets(Base, TimestampMixin):
    name = fields.CharField(max_length=100, null=True)
    specie = fields.CharField(max_length=100)
    # level = NumberAttribute(default=1)
    # experience = NumberAttribute(null=True)
    # energy = NumberAttribute(null=True)
    # fun = NumberAttribute(null=True)
    # hunger = NumberAttribute(null=True)
    # hygiene = NumberAttribute(null=True)
    # love = NumberAttribute(null=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="pets")

    class Meta:
        table = "pet"
