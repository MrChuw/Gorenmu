# -*- coding: utf-8 -*-
from somali.database.base import Base, TimestampMixin, fields
from somali import config


class Channel(Base, TimestampMixin):
    user = fields.ForeignKeyField("models.User", unique=True)
    followers = fields.IntField(null=True, description="Twitch followers")
    banwords = fields.JSONField(default={})
    disabled = fields.JSONField(default={})
    online = fields.BooleanField(default=True)
    prefix = fields.CharField(max_length=1, default="+")

    class Meta:
        table = "channel"

    @classmethod
    async def append_json(cls, id, field, key, value) -> None:
        instance = await cls.get(user_id=id)
        json = getattr(instance, field)
        json[key] = value
        setattr(instance, field, json)
        await instance.save()

    @classmethod
    async def remove_json(cls, id, field, key) -> None:
        instance = await cls.get(user_id=id)
        json = getattr(instance, field)
        json.pop(key)
        setattr(instance, field, json)
        await instance.save()

    async def prefixo1(prefixo, prefixo1: str) -> None:
        prefixo.prefix = prefixo1
        await prefixo.save()

    @classmethod
    async def entrar_canal():
        return

