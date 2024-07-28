from __future__ import annotations

from tortoise import fields

from bot.models.base import Base, TimestampMixin
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from bot.models.User import User


class Annotation(Base, TimestampMixin):
    content: Union[str, fields.TextField] = fields.TextField()

    user: User = fields.ForeignKeyField("models.User", related_name="annotation")

    class Meta:
        table = "annotation"
