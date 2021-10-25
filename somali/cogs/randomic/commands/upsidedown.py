# -*- coding: utf-8 -*-
import random
import typing as t
from somali.utils import roles
import upsidedown


aliases=['cbaixo']
description = "Coloca o texto de cabeça para baixo"
# usage = 'digite o comando, "número" para indicar o número de lados do dado.'
# extra_checks = [roles.mod]


async def command(ctx, *, args):
    texto = upsidedown.transform(args)
    await ctx.send(texto)

