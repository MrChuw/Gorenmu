from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Shows general bot statistics, uptime, and metadata like site and developer.",
            "How to use: +botinfo | +site | +uptime",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Exibe estatísticas gerais do bot, tempo de atividade e metadados como site e desenvolvedor.",
            "Como usar: +botinfo | +site | +uptime",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param(
            "en",
            r"I am connected to 8 channels, with (7[0-9]|[89][0-9]|\d{3,}) commands, "
            r"made by @mr_chuw in Python \(Twitchio\)\. Bot website: https://gorenmu\.vercel\.app/",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"Estou conectado a canais 8, com comandos (7[0-9]|[89][0-9]|\d{3,}), "
            r"criados por @mr_chuw em Python \(Twitchio\)\. Site do bot: https://gorenmu\.vercel\.app/",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    site: ClassVar[list] = [
        pytest.param("en", "https://gorenmu.vercel.app/", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "https://gorenmu.vercel.app/", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    uptime: ClassVar[list] = [
        pytest.param("en", 'I woke up 1 day ago.', marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Eu acordei há 1 dia",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
