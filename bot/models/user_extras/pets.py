from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from bot.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from bot.models.user import User


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

    @staticmethod
    async def create_pet(specie: str, user: User, name: str | None = None):
        return await Pets.create(user=user, specie=specie, name=name)

    async def update_name(self, name: str):
        self.name = name
        await self.save()
        return self

    async def change_owner(self, new_owner: User):
        self.user = new_owner
        await self.save()
        return self
