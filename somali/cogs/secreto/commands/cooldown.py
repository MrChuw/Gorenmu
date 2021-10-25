# -*- coding: utf-8 -*-
from somali.utils import roles
from somali.database.models import Playert
from somali.apis.twitch import Twitch

description = "Comando proibido para todos os publicos. :)"
# aliases = ["evl"]
extra_checks = [roles.owner]


async def command(ctx, arg: str = None, cooldown: int = 1):
    if arg == None:
        if player := await Playert.get_or_none(id=ctx.author.id):
            player.choice = cooldown
            await player.save()
            ctx.response = f'Seu cooldown alterado para {cooldown}.'
    else:
        id_do_canal_passado = await Twitch.account_id(arg)
        if player := await Playert.get_or_none(id=id_do_canal_passado):
            player.choice = cooldown
            await player.save()
            ctx.response = f'Cooldown de {arg} alterado para {cooldown}.'
    



