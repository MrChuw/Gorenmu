from __future__ import annotations

import contextlib
import json
from datetime import datetime
from typing import Coroutine, List, Optional

from tortoise import fields

from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
from models.base import Base, UserMixin, TimestampMixin, ContentMixin, CharFieldStr, BoolFieldBool, NickHistory
from models.timezonefield import DatetimeTzField

from models.User.__init__user import (Cookies, Player, Pets, PlayerTorre, Suggest, Bug, Annotation, Status, Reminder,
                                      Copypasta, Mensage_log, Loterica, Historico_de_Nicks)


if TYPE_CHECKING:
    from ext.commands import Context


from urlextract import URLExtract
extractor = URLExtract()
extractor.update()

# TODO: Mover as coisas que são de outros schemas para os seus devidos lugares, remover tudo que não é necessário.
#  Criar funções que realmente são boas para o User.
#  Melhorar a criação do histórico de nicks.

# TODO: Somente depois que fizer oquê ta acima, começar a trabalhar no mini-script que vai ser responsável pôr renomear
#  todos os campos e tabelas para inglês.

class User(Base, UserMixin, TimestampMixin, ContentMixin):
    channel: CharFieldStr = fields.CharField(max_length=64, null=True, description="Twitch channel")
    saved_color: CharFieldStr = fields.CharField(max_length=7, null=True, description="Twitch color")
    city: CharFieldStr = fields.CharField(max_length=100, null=True)
    ping: BoolFieldBool = fields.BooleanField(default=True)
    mention: BoolFieldBool = fields.BooleanField(default=True)
    block: BoolFieldBool = fields.BooleanField(default=False)
    sponsor: BoolFieldBool = fields.BooleanField(default=True)
    nickname: CharFieldStr = fields.CharField(max_length=32, null=True)
    timestamp: DatetimeTzField = DatetimeTzField(null=True)
    language: CharFieldStr = fields.CharField(max_length=32, null=True)
    cookies: Cookies = fields.ReverseRelation["Cookies"]
    player: Player = fields.ReverseRelation["Player"]
    pets: Pets = fields.ReverseRelation["Pets"]
    player_torre: Coroutine[List[PlayerTorre]] = fields.ReverseRelation["Player_torre"]
    suggest: Suggest = fields.ReverseRelation["Suggest"]
    bug: Bug = fields.ReverseRelation["Bug"]
    annotation: Coroutine[List[Annotation]] = fields.ReverseRelation["Annotation"]
    historico_de_nicks: Coroutine[NickHistory] = fields.ReverseRelation["Historico_de_nicks"]
    status: Status = fields.ReverseRelation["Status"]
    user_1: User = fields.ReverseRelation["user_1"]
    user_2: User = fields.ReverseRelation["user_2"]
    reminder: Reminder = fields.ReverseRelation["reminder"]
    reminder_to: User = fields.ReverseRelation["reminder_to"]
    copypasta: Copypasta = fields.ReverseRelation["Copypasta"]
    mensages: Mensage_log = fields.ReverseRelation["messages"]
    Loterica: Loterica = fields.ReverseRelation["Loterica"]

    class Meta:
        table = "user"

    def __str__(self) -> str:
        return f"{self.nickname}" if self.sponsor and self.nickname else f"@{self.name}"

    async def prefixo1(self, prefixo, prefixo1: str) -> None:
        prefixo.prefix = prefixo1
        await prefixo.save()

    async def criar(ctx: Context, **kwargs) -> Optional[User]:
        user = {
            "id": ctx.author.id,
            "name": ctx.author.name,
            "channel": ctx.channel.name,
            "saved_color": ctx.author.colour,
            "content": ctx.message.content.replace("ACTION", "", 1),
            **kwargs,
        }
        await User.create(**user)
        user = await User.get(id=ctx.author.id)
        await Historico_de_Nicks.create(user=user, id=user.id, nicks=json.dumps({0: user.name}))
        return user

    async def atualizar(ctx: Context, **kwargs) -> Optional[User]:
        attrs = {
            "name": ctx.author.name,
            "channel": ctx.channel.name,
            "saved_color": ctx.author.colour,
            "content": ctx.message.content.replace("ACTION", "", 1),
            "timestamp": ctx.message.timestamp,
        }
        update_fields = []
        user = await User.get(id=ctx.author.id)
        if user.name != ctx.author.name:
            await Historico_de_Nicks.create(user=user, nicks=user.name)
        for attr, value in attrs.items():
            if attr == "content" and len(value) > 500:
                value = value[:500]
            if getattr(user, attr) != value:
                setattr(user, attr, value)
                update_fields.append(attr)
        if update_fields:
            update_fields.append("updated_at")
            await user.save(update_fields=update_fields)
        if extractor.has_urls(ctx.message.content):
            await Mensage_log.create(
                user=user,
                content=ctx.message.content,
                type="message_link",
                channel=ctx.bot.channels[ctx.channel.name],
            )
        else:
            await Mensage_log.create(
                user=user,
                content=ctx.message.content,
                type="message",
                channel=ctx.bot.channels[ctx.channel.name],
            )

        return user

    async def atualizar_ou_criar(ctx: Context, **kwargs) -> Optional[User]:
        if instance := await User.get_or_none(id=ctx.author.id):
            attrs = {
                "name": ctx.author.name,
                "channel": ctx.channel.name,
                # "saved_color": ctx.author.colour,
                "content": ctx.message.content.replace("ACTION", "", 1),
                "timestamp": ctx.message.timestamp,
            }
            update_fields = []
            if instance.name != ctx.author.name:
                await Historico_de_Nicks.create(user=instance, nicks=instance.name)
            # detectar se a mensagem é um link de qualquer formado:

            if extractor.has_urls(ctx.message.content):
                await Mensage_log.create(
                    user=instance,
                    content=ctx.message.content,
                    type="message_link",
                    channel=ctx.bot.channels[ctx.channel.name],
                )
            else:
                await Mensage_log.create(
                    user=instance,
                    content=ctx.message.content,
                    type="message",
                    channel=ctx.bot.channels[ctx.channel.name],
                )

            for attr, value in attrs.items():
                if attr == "content" and len(value) > 500:
                    value = value[:500]
                if getattr(instance, attr) != value:
                    setattr(instance, attr, value)
                    update_fields.append(attr)
            if update_fields:
                update_fields.append("updated_at")
                await instance.save(update_fields=update_fields)
            return instance
        else:
            user = {
                "id": ctx.author.id,
                "name": ctx.author.name,
                "channel": ctx.channel.name,
                "saved_color": ctx.author.colour,
                "content": ctx.message.content.replace("ACTION", "", 1),
                "timestamp": ctx.message.timestamp,
                **kwargs,
            }
            user = await User.create(**user)
            # user = await User.get(id=ctx.author.id)
            await Historico_de_Nicks.create(user=user, nicks=user.name)
            if extractor.has_urls(ctx.message.content):
                await Mensage_log.create(
                    user=user,
                    content=ctx.message.content,
                    type="message_link",
                    channel=ctx.bot.channels[ctx.channel.name],
                )
            else:
                await Mensage_log.create(
                    user=user,
                    content=ctx.message.content,
                    type="message",
                    channel=ctx.bot.channels[ctx.channel.name],
                )

            return user

    async def pegar_usuario(id=None, nome=None) -> Optional[User]:
        if id is not None:
            return await User.get_or_none(id=id)
        elif nome is not None:
            return await User.get_or_none(name=nome)


    async def update_user_info(
        self,
        apelido: Optional[str] = None,
        saved_color: Optional[str] = None,
        city: Optional[str] = None,
        mention: Optional[bool] = None,
        user_id: Optional[int] = None,
        name: Optional[str] = None,
        auto_reminds: Optional[str] = None,
    ):

        if apelido is not None:
            self.nickname = apelido
        if saved_color is not None:
            self.saved_color = saved_color
        if city is not None:
            self.city = city
        if mention is not None:
            self.mention = mention
        if auto_reminds is not None:
            self.auto_reminds = auto_reminds
        await self.save()
        return self

