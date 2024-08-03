from __future__ import annotations

from tortoise import fields

from models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from models.User.User import User






class Bug(Base, TimestampMixin):
    content = fields.TextField()

    visto = fields.BooleanField(default=False)
    resposta = fields.TextField(default=None, null=True)
    resposta_enviada = fields.BooleanField(default=False)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="bug"
    )

    class Meta:
        table = "bug"
