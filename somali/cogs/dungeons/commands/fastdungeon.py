# -*- coding: utf-8 -*-
from somali.cogs.dungeons import (
    options_sub_class,
    resume_dungeon,
)
from somali.database.models import Player
from somali.utils import timetools

description = "Entre na dungeon e adquira experiência sem precisar tomar uma escolha"
aliases = ["fed", "fd"]


async def command(ctx):
    if player := await Player.get_or_none(name=ctx.author.name):
        if not player.sub_class:
            option1, option2 = options_sub_class(player.class_, player.gender)
            ctx.response = (
                f'antes de continuar, digite "{ctx.prefix}ed" e sua nova classe: {option1} ou {option2}'
            )
        elif cooldown := timetools.on_cooldown(player.updated_at, now=ctx.message.timestamp, s=60):
            ctx.response = f"aguarde {cooldown} para entrar em outra dungeon ⌛"
        else:
            multiplier = 2 if ctx.user.sponsor else 10
            player, response = resume_dungeon(player, multiplier=multiplier)
            player.last_at = ctx.message.timestamp
            await player.save()
            ctx.response = response
    else:
        ctx.response = (
            "antes de continuar, escolha sua classe! "
            f'Digite "{ctx.prefix}ed" e: Guerreiro(a), Arqueiro(a) ou Mago(a)'
        )
