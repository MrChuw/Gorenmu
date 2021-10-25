# -*- coding: utf-8 -*-
import random
import typing as t
from somali.utils import roles


# aliases=['dado']
description = "É um echo"
# usage = 'digite o comando, "número" para indicar o número de lados do dado.'
extra_checks = [roles.mod]


async def command(ctx):
    texto = ctx.message.content[6:]
    await ctx.send(texto)

