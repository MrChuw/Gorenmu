# -*- coding: utf-8 -*-
from tortoise import signals

from somali.database.base import Base, ContentMixin, TimestampMixin, fields
from somali.webhook import Webhook


class Suggest(Base, TimestampMixin, ContentMixin):
    name = fields.CharField(max_length=64, description="Twitch username")
    channel = fields.CharField(max_length=64, description="Twitch username")

    class Meta:
        table = "suggest"


@signals.post_save(Suggest)
async def new_suggest(sender, instance, created, using_db, update_fields):
    await Webhook.suggestions(
        id=instance.id,
        content=instance.content,
        author=instance.name,
        channel=instance.channel,
        timestamp=instance.updated_at,
    )
