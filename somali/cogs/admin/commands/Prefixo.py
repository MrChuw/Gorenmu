# -*- coding: utf-8 -*-
from somali.utils import roles, convert
from somali.database.models import Channel
from somali import log
from somali.apis import Twitch
from somali.bots.prefixos import prefixos


async def variavel_canal_prefixo(*ctx: str) -> None:
    id = await Twitch.account_id(ctx.channel.name)
    prefixox = await Channel.get(user_id=id)
    return prefixox

description = "Comando para mandar mudar o prefixodo canal."
extra_checks = [roles.mod]
usage = f'''Envie o comando mais prefixo que você deseja.'''



vazio = " "
async def command(ctx, prefixo: str):
    # ctx.response = "Comando desabilitado pelo bem da minha sanidade, literalmente."
    prefixo1 = prefixo
    id = await Twitch.account_id(ctx.channel.name)
    canal = await Channel.get(user_id=id)
    if len(prefixo) == 1 or prefixo:
        if prefixo in str(canal.prefix):
            ctx.response = f'O canal ja esta usando o prefixo {prefixo1}.'
        else:
            await canal.prefixo1(prefixo1)
            ctx.response = f'''O prefixo do canal foi alterado para "{prefixo1}".'''
    else:
        ctx.response = f'''Atualmente eu so consigo armazenar prefixos de 1 caractere o prefixo que você tentou usar não é valido pois contem "{len(prefixo1)}" caracteres.'''