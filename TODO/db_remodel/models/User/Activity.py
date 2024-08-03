from __future__ import annotations

import contextlib
from datetime import datetime

from tortoise import fields

from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from models.User.User import User
from models.base import Base, TimestampMixin, TextFieldStr
from models.timezonefield import DatetimeTzField


class Status(Base, TimestampMixin):
    online = fields.BooleanField(default=True)
    alias = fields.TextField(null=True)
    message: TextFieldStr = fields.TextField(null=True)
    updated_at = DatetimeTzField(null=True)
    user: User = fields.ForeignKeyField("models.User", related_name="status")

    class Meta:
        table = "status"

    async def leave_afk(self):
        self.online = True
        self.updated_at = datetime.utcnow()
        await self.save()
        return True

    async def afk(self, alias, message):
        self.online = False
        self.alias = alias
        self.message = message
        self.updated_at = datetime.utcnow()
        await self.save()
        return True

    async def rafk(self, alias, message, updated_at):
        self.online = False
        self.alias = alias
        self.message = message
        self.updated_at = updated_at
        await self.save()
        return True























