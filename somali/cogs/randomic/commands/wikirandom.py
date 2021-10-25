# -*- coding: utf-8 -*-
from asyncio.exceptions import TimeoutError
import requests
from somali.apis import Dicio
from somali.utils import checks, convert, roles

aliases = ["wrandom"]
description = "Jogo de Wikipedia aleatoria, a entrada dura 30 segundas"
extra_checks = [roles.mod, checks.game]


async def command(ctx):
    pattern: str = convert.txt2randomline("somali//data//syllables.txt")
    users: list = []
    # words: list = []
    entrar = ['entrar', 'participar']

    def play(message) -> bool:
        # if len(message.content.split(" ")) != 1:
        #     return False
        # if not message.content.isalpha():
        #     return False
        # word = message.content.lower()
        # if pattern not in word or word in words:
        #     return False
        # words.append(word)
        # if not Dicio.exists(word):
        #     return False
        if message.content.lower() in entrar:
            if message.author.name not in users:
                users.append(message.author.name)
            else:
                return False

    def check(message) -> bool:
        if message.echo:
            return False
        if message.channel.name != ctx.channel.name:
            return False
        if not ctx.bot.channels[message.channel.name]["online"]:
            return False
        return play(message)

    try:
        ctx.response = (
            "Você inicio um jogo de Wikipedia aleatorio. "
            'Para entrar digite "Entrar|Participar".'
        )
        await ctx.bot.reply(ctx)
        ctx.bot.cache.set(f"game-{ctx.channel.name}", ctx.author.name, ex=30)
        waits = ctx.bot._waiting.copy()
        await ctx.bot.wait_for("message", check, timeout=30)
    except TimeoutError:
        if users:
            # users = sorted(users.items(), key=lambda x: x[1], reverse=True)
            for jogador in users:
                res = requests.get("https://pt.wikipedia.org/wiki/Special:Random")
                await ctx.send(f"{jogador} FBBlock {res.url}")
        else:
            for jogador in users:
                res = requests.get("https://pt.wikipedia.org/wiki/Special:Random")
                await ctx.send(f"{jogador} FBBlock {res.url}")
            # await ctx.send("AAAAAAAAAAAAAAAAAA")
    finally:
        ctx.response = None
        ctx.bot.cache.delete(f"game-{ctx.channel.name}")
        for wait in ctx.bot._waiting:
            if wait not in waits:
                ctx.bot._waiting.remove(wait)
                break
