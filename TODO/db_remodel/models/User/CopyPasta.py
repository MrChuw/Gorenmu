from __future__ import annotations

from tortoise import fields

from models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from models.User.User import User


class Copypasta(Base, TimestampMixin):
    content = fields.TextField()
    visivel = fields.BooleanField(default=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="copypasta"
    )

    class Meta:
        table = "copypasta"
