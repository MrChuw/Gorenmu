# -*- coding: utf-8 -*-
import random
import typing as t
import dice

aliases=['dado']
description = "um dado ne, digite o comando, \"número\" para indicar o número de lados do dado."
usage = 'digite o comando, "número" para indicar o número de lados do dado.'


async def command(ctx, arg: str = ""):
    if not arg:
        arg = "1d20"
    elif "d" not in arg:
        arg = f"1d{arg}"
    dices = arg.lower().split("d")
    amount = int(dices[0].replace(",", ".")) if dices[0] else None
    sides = int(dices[1].replace(",", ".")) if dices[1] else None
    roll = sum([random.randint(1, round(sides)) for i in range(round(amount))])
    if amount > 1e2:
        ctx.response = "Muito dado para rolar preguiça."
    elif sides > 1e3:
        ctx.response = "Muito dado para rolar preguiça."
    else:
        ctx.response = f"você rolou {roll} 🎲"

