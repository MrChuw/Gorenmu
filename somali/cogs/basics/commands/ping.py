# -*- coding: utf-8 -*-
import random
import asyncio

description = "Verifique se o bot está online"
aliases = ["pong"]


async def command(ctx):
    invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
    # pesos = [0.55, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, ]
    # pings = ["Saco, deixei a bolinha passar.",
    #         f"{await asyncio.sleep(5) }Foi mau acabei dormindo, toma a bola de volta, ping 🏓" if invoke_by == "pong" else "Foi mau acabei dormindo, toma a bola de volta, pong 🏓",
    #         "Não estou afim de devolver, vou ficar batendo a bolinha do meu lado da mesa, ping 🏓" if invoke_by == "pong" else "Não estou afim de devolver, vou ficar batendo a bolinha do meu lado da mesa, pong 🏓",
    #         "Por qual motivo nós estamos fazendo isso mesmo?",
    #         "E se eu te falar que eu não sei jogar ping pong e esse tempo todo estou somente fazendo barulho com a boca.",
    #         "Cansei, vou me sentar aqui um minutinho.",
    #         "O que é a vida?",
    #         f"{await asyncio.sleep(5)} \"👻 BU\"",
    #         f"{await asyncio.sleep(5)} Cansei vou dormir.",
    #         f"{await asyncio.sleep(10)} Ainda ta esperando, so vai embora, não quero mais jogar.",
            # (
            #  await asyncio.sleep(5),
            #  await ctx.send("/color Red"),
            #  await ctx.send("/me Oque é a vida?"),
            #  await asyncio.sleep(5),
            #  await ctx.send("/color OrangeRed"), 
            #  await ctx.send("/color Red"), 
            #  await asyncio.sleep(5), 
            #  await ctx.send("/me Abujamra - Eu vou terminar nossa conversa com uma pergunta muito simples."), 
            #  await ctx.send("/color OrangeRed"), 
            #  await asyncio.sleep(5), 
            #  await ctx.send("/color GoldenRod"), 
            #  await ctx.send("/me Sterblitch - Não termine me ferrando."), 
            #  await ctx.send("/color OrangeRed"), 
            #  await asyncio.sleep(5), 
            #  await ctx.send("/color Red"), 
            #  await ctx.send("/me Abujamra - Muito simples."),
            #  await ctx.send("/color OrangeRed"),
            #  await asyncio.sleep(5),
            #  await ctx.send("/color GoldenRod"),
            #  await ctx.send("/me Sterblitch - Por favor…"),
            #  await ctx.send("/color OrangeRed"),
            #  await asyncio.sleep(5), 
            #  await ctx.send("/color Red"),
            #  await ctx.send("/me Abujamra - Sterblitch…"),
            #  await ctx.send("/color OrangeRed"),
            #  await asyncio.sleep(5),
            #  await ctx.send("/color GoldenRod"),
            #  await ctx.send("/me Sterblitch - Por favor…"),
            #  await ctx.send("/color OrangeRed"),
            #  await asyncio.sleep(5),
            #  await ctx.send("/color Red"),
            #  await ctx.send("/me Abujamra - O que é a vida?"),
            #  await ctx.send("/color OrangeRed"),
            #  await asyncio.sleep(5),
            #  await ctx.send("/color GoldenRod"),
            #  await ctx.send("/me Sterblitch - Não tenho a mínima ideia."),
            #  await ctx.send("/color OrangeRed"),
            #  await asyncio.sleep(5),
            #  await ctx.send("/color Red"),
            #  await ctx.send("/me Abujamra - O que é a vida?"),
            #  await ctx.send("/color OrangeRed"),
            #  await asyncio.sleep(5),
            #  await ctx.send("/color GoldenRod"),
            #  await ctx.send("/me Sterblitch - A vida é poder ter momentos como esse para mim, para mim. Por mais que eu esteja sendo fofo, talvez a vida para mim seja momentos fofos, sabe? De poder trabalhar com o que eu gosto, de poder pagar plano de saúde para os meus avós, poder ser perfeito para as pessoas. Porque eu sei o que que eu passo, mas para mim a vida é poder fazer coisa bacana."), 
            #  await ctx.send("/color OrangeRed"),
            #  await asyncio.sleep(5),
            #  await ctx.send("/color Red"),
            #  await ctx.send("/me Abujamra - O que é a vida?"),
            #  await ctx.send("/color OrangeRed"), 
            #  await asyncio.sleep(5), await ctx.send("/color GoldenRod"), 
            #  await ctx.send("/me Sterblitch - É ter memória talvez."), 
            #  await ctx.send("/color OrangeRed"), 
            #  await asyncio.sleep(5),
            #  await ctx.send("/color Red"), 
            #  await ctx.send("/me Abujamra - O que é a vida?"),
            #  await ctx.send("/color OrangeRed"),
            #  await asyncio.sleep(5),
            #  await ctx.send("/color GoldenRod"),
            #  await ctx.send("/me Sterblitch - Me responde, por favor, cara…"),
            #  await ctx.send("/color OrangeRed"),
            #  await asyncio.sleep(5), 
            #  await ctx.send("/color Red"),
            #  await ctx.send("/me Abujamra - Eu te responde dizendo... Acabou o nosso papo."), 
            #  await ctx.send("/color OrangeRed"), 
            #  await asyncio.sleep(1),
            #  await ctx.send("/color OrangeRed"),)
            # ]
    # ping_escolhido = random.choices([pings, None], weights=(0.90, 0.10))
    # if ping_escolhido:
    #     ping_escolhido = random.choices(pings, weights=pesos)
    percentagem = random.randrange(1, 500)
    # percentagem = 9
    if percentagem == 1:
        ctx.response = ("Saco, deixei a bolinha passar.")

    elif percentagem == 2:
        await asyncio.sleep(5)
        ctx.response = ("Foi mau acabei dormindo, toma a bola de volta, ping 🏓" if invoke_by ==
                        "pong" else "Foi mau acabei dormindo, toma a bola de volta, pong 🏓")

    elif percentagem == 2:
        ctx.response = ("Não estou afim de devolver, vou ficar batendo a bolinha do meu lado da mesa, ping 🏓" if invoke_by ==
                        "pong" else "Não estou afim de devolver, vou ficar batendo a bolinha do meu lado da mesa, pong 🏓")

    elif percentagem == 3:
        ctx.response = ("Por qual motivo nós estamos fazendo isso mesmo?")

    elif percentagem == 4:
        ctx.response = (
            "E se eu te falar que eu não sei jogar ping pong e esse tempo todo estou somente fazendo barulho com a boca.")

    elif percentagem == 5:
        ctx.response = ("Cansei, vou me sentar aqui um minutinho.")

    elif percentagem == 6:
        await asyncio.sleep(5)
        ctx.response = ("👻 BU")

    elif percentagem == 7:
        await asyncio.sleep(5)
        ctx.response = ("Cansei vou dormir.")

    elif percentagem == 8:
        await asyncio.sleep(10)
        ctx.response = (
            "Ainda ta esperando, so vai embora, não quero mais jogar.")

    if percentagem == 9:
        await ctx.send("/color Red")
        await ctx.send("/me Oque é a vida?")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(3)
        await ctx.send("/color Red")
        await ctx.send("/me Abujamra - Eu vou terminar nossa conversa com uma pergunta muito simples.")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color GoldenRod")
        await ctx.send("/me Sterblitch - Não termine me ferrando.")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color Red")
        await ctx.send("/me Abujamra - Muito simples.")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color GoldenRod")
        await ctx.send("/me Sterblitch - Por favor…")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color Red")
        await ctx.send("/me Abujamra - Sterblitch…")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color GoldenRod")
        await ctx.send("/me Sterblitch - Por favor…")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color Red")
        await ctx.send("/me Abujamra - O que é a vida?")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color GoldenRod")
        await ctx.send("/me Sterblitch - Não tenho a mínima ideia.")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color Red")
        await ctx.send("/me Abujamra - O que é a vida?")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color GoldenRod")
        await ctx.send("/me Sterblitch - A vida é poder ter momentos como esse para mim, para mim. Por mais que eu esteja sendo fofo, talvez a vida para mim seja momentos fofos, sabe? De poder trabalhar com o que eu gosto, de poder pagar plano de saúde para os meus avós, poder ser perfeito para as pessoas. Porque eu sei o que que eu passo, mas para mim a vida é poder fazer coisa bacana.")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color Red")
        await ctx.send("/me Abujamra - O que é a vida?")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color GoldenRod")
        await ctx.send("/me Sterblitch - É ter memória talvez.")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color Red")
        await ctx.send("/me Abujamra - O que é a vida?")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color GoldenRod")
        await ctx.send("/me Sterblitch - Me responde, por favor, cara…")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(5)
        await ctx.send("/color Red")
        await ctx.send("/me Abujamra - Eu te responde dizendo... Acabou o nosso papo.")
        await ctx.send("/color OrangeRed")
        await asyncio.sleep(1)
        await ctx.send("/color OrangeRed")

    elif percentagem == 10:
        ctx.response = ("O que é a vida?")
        ctx.response = ping_escolhido[0]
    else:
        ctx.response = ("ping 🏓" if invoke_by == "pong" else "pong 🏓")
    # percentagem = random.randint(0, 500)

