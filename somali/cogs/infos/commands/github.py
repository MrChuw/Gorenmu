# -*- coding: utf-8 -*-
import asyncio
import random

description = "Receba O link secreto"
aliases = ["git"]
usage = "digite o comando"
link = "https://github.com/Bobotinho/bot"
link1 = "https://www.google.com.br/"

async def command(ctx):
    await ctx.send("Então você quer o meu link super-secreto ne, espera ai que eu vou ali buscar ele...")
    await asyncio.sleep(random.randint(0, 10))
    await ctx.send(f"Achei um link acho que é esse que tu que certo {link1}")
    await asyncio.sleep(2)
    await ctx.send("Pera não era esse link que tu queria, então ta espera mais um pouco que eu vou buscar o certo.")
    await asyncio.sleep(random.randint(0,5))
    await ctx.send(f'''Ai então {link} , a verdade é que eu não passo de uma copia barata e mau feita do @bobotinho, e o meu "criador" so pretende me encher de comando inutil, então vai la da uma força no bot original, e da estrelinha pra ele se tiver conta no git.''')
    