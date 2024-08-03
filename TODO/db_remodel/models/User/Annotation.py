from __future__ import annotations

from tortoise import fields

from models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from models.User.User import User


class Annotation(Base, TimestampMixin):
    content = fields.TextField()

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="annotation"
    )

    class Meta:
        table = "annotation"
