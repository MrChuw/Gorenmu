# -*- coding: utf-8 -*-
import random
import typing as t
from somali.utils import roles


aliases=['invert']
description = "Inverte a mensagem."
# usage = 'digite o comando, "número" para indicar o número de lados do dado.'
# extra_checks = [roles.mod]


async def command(ctx, *, args):
    texto = args[::-1]
    await ctx.send(texto)

