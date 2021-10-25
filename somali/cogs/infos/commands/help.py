# -*- coding: utf-8 -*-
from somali import config
import os


base = "somali/cogs"
lista = os.listdir(base)
if "secreto" in lista: lista.remove("secreto")
lista1 = "', '".join(str(e) for e in lista).title()

description = "Uma breve lista de comandos"
# aliases = ["ff"]
usage = (f"""Para usar help você tem que digitar 'help' e escolher entre as seguintes listas de comandos: '{lista1}'.""")

async def command(ctx, arg: str):
    pasta1 = arg
    pastas = os.listdir(base)
    c = None
    for command in ctx.bot.commands.values():
        if arg == command.name or (command.aliases and arg in command.aliases):
            c = command
            break
    if arg in pastas:
        for pasta in pastas:
            if pasta1 in pasta:
                if pasta == pasta1:
                    if pasta in os.listdir(base):
                        # if lista3 := os.listdir(base):
                        # lista3 = os.listdir(base).pop(0)
                        lista4 = (os.listdir(f"somali/cogs/{pasta}/commands"))
                        if "__pycache__" in lista4: lista4.remove("__pycache__")
                        # lista5 = lista4.remove("__pycache__")
                        lista5 = "', '".join(str(e) for e in lista4)
                        lista5 = lista5.replace('.py', '').title()
                        ctx.response = f"Os comandos são: '{lista5}'"
                        break

    elif c.aliases:
        aliases = ", ".join([ctx.prefix + alias for alias in c.aliases])
        ctx.response = f"{ctx.prefix}{c.name} ({aliases}): {c.description}"
    else:
        ctx.response = f"{ctx.prefix}{c.name}: {c.description}"






    # elif pasta == os.listdir(base).pop(1):
    #     lista3 = os.listdir(base).pop(1); lista4 = (os.listdir(f"somali/cogs/{lista3}/commands")); lista5 = lista4.remove("__pycache__"); lista5 = "', '".join(str(e) for e in lista4); lista5 = lista5.replace('.py', '').title()
    #     ctx.response = f"Os comandos são: '{lista5}'"
    # elif pasta == os.listdir(base).pop(2):
    #     lista3 = os.listdir(base).pop(2); lista4 = (os.listdir(f"somali/cogs/{lista3}/commands")); lista5 = lista4.remove("__pycache__"); lista5 = "', '".join(str(e) for e in lista4); lista5 = lista5.replace('.py', '').title()
    #     ctx.response = f"Os comandos são: '{lista5}'"
    # elif pasta == os.listdir(base).pop(3):
    #     lista3 = os.listdir(base).pop(3); lista4 = (os.listdir(f"somali/cogs/{lista3}/commands")); lista5 = lista4.remove("__pycache__"); lista5 = "', '".join(str(e) for e in lista4); lista5 = lista5.replace('.py', '').title()
    #     ctx.response = f"Os comandos são: '{lista5}'"
    # elif pasta == os.listdir(base).pop(4):
    #     lista3 = os.listdir(base).pop(4); lista4 = (os.listdir(f"somali/cogs/{lista3}/commands")); lista5 = lista4.remove("__pycache__"); lista5 = "', '".join(str(e) for e in lista4); lista5 = lista5.replace('.py', '').title()
    #     ctx.response = f"Os comandos são: '{lista5}'"
    # elif pasta == os.listdir(base).pop(5):
    #     lista3 = os.listdir(base).pop(5); lista4 = (os.listdir(f"somali/cogs/{lista3}/commands")); lista5 = lista4.remove("__pycache__"); lista5 = "', '".join(str(e) for e in lista4); lista5 = lista5.replace('.py', '').title()
    #     ctx.response = f"Os comandos são: '{lista5}'"
    # elif pasta == os.listdir(base).pop(6):
    #     lista3 = os.listdir(base).pop(6); lista4 = (os.listdir(f"somali/cogs/{lista3}/commands")); lista5 = lista4.remove("__pycache__"); lista5 = "', '".join(str(e) for e in lista4); lista5 = lista5.replace('.py', '').title()
    #     ctx.response = f"Os comandos são: '{lista5}'"
    # elif pasta == os.listdir(base).pop(7):
    #     lista3 = os.listdir(base).pop(7); lista4 = (os.listdir(f"somali/cogs/{lista3}/commands")); lista5 = lista4.remove("__pycache__"); lista5 = "', '".join(str(e) for e in lista4); lista5 = lista5.replace('.py', '').title()
    #     ctx.response = f"Os comandos são: '{lista5}'"
