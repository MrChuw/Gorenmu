# -*- coding: utf-8 -*-
from somali.database.base import Base, TimestampMixin, ContentMixin, fields


class Afk(Base, TimestampMixin, ContentMixin):
    user = fields.ForeignKeyField("models.User", unique=True)
    alias = fields.CharField(max_length=8, null=True)

    class Meta:
        table = "afk"
