# -*- coding: utf-8 -*-
from somali.database.base import Base, TimestampMixin, UserMixin, fields


class Playert(Base, UserMixin, TimestampMixin):
    class_ = fields.CharField(max_length=1)
    sub_class = fields.CharField(max_length=1, default="A", null=True)
    gender = fields.CharField(max_length=1)
    encontro = fields.CharField(max_length=5, null=True)
    quote = fields.TextField()
    choice = fields.IntField(default=1)
    wins = fields.SmallIntField(default=0)
    defeats = fields.SmallIntField(default=0)
    level = fields.IntField(default=1)
    andar = fields.IntField(default=0)
    zona = fields.IntField(default=1)
    xp = fields.IntField(default=0)
    

    class Meta:
        table = "player torre"
