# -*- coding: utf-8 -*-
from somali.database.base import Base, TimestampMixin, fields


class SystemLog(Base, TimestampMixin):
    error = fields.CharField(max_length=500, null=True)

    class Meta:
        table = "systemlog"
