# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "Command to get information about other commands.",
            "How to use: {}help (command name)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando para obter informações sobre outros comandos.",
            "Como usar: {}help (nome do comando)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
    no_content = [
        pytest.param(
            "en",
            "Site in construction, here is the list of commands: https://gorenmu.vercel.app/",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Site em construção, aqui está a lista de comandos: https://gorenmu.vercel.app/",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    wrong_command = [
        pytest.param(
            "en", 'I dont have command with name "pign", maybe you meant "ping".', marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            'Não tenho um comando com o nome "pign", talvez você quis dizer "ping".',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    right_command = [
        pytest.param(
            "en",
            "+ping: Command to check if the bot is alive. - Cooldown: 3 seconds https://gorenmu.vercel.app/commands/ping - Aliases: pong",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "+ping: Comando para verificar se o bot esta vivo. - Cooldown: 3 segundos https://gorenmu.vercel.app/commands/ping - Aliases: pong",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    params_ = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
