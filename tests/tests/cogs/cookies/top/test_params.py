from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "See who are the top cookie eaters or donors.",
            "To use: +cookie top (or pass one of the options stocked | streak | consumed | donated | received | total)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Veja quem são os melhores comedores, doadores ou acumuladores de cookies.",
            "Para usar: +cookie top (ou passe uma das opções stocked | streak | consumed | donated | received | total)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param(
            "en",
            "top 2 stocked: 🏆 @channelname: (8534) 🥈 @username: (10) "
            "|| You are in the 2th position in the ranking with 10.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 2 stocked: 🏆 @channelname: (8534) 🥈 @username: (10) "
            "|| Você está na 2ª posição na classificação com 10.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    stocked: ClassVar[list] = [
        pytest.param(
            "en",
            "top 2 stocked: 🏆 @channelname: (8534) 🥈 @username: (10) "
            "|| You are in the 2th position in the ranking with 10.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 2 stocked: 🏆 @channelname: (8534) 🥈 @username: (10) "
            "|| Você está na 2ª posição na classificação com 10.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    consumed: ClassVar[list] = [
        pytest.param(
            "en",
            "top 2 cookiers: 🏆 @channelname: (54) 🥈 @username: (0) "
            "|| You are in the 2th position in the ranking with 0.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 2 cookiers: 🏆 @channelname: (54) 🥈 @username: (0) "
            "|| Você está na 2ª posição na classificação com 0.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    donated: ClassVar[list] = [
        pytest.param(
            "en",
            "top 2 givers: 🏆 @channelname: (93) 🥈 @username: (0) "
            "|| You are in the 2th position in the ranking with 0.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 2 givers: 🏆 @channelname: (93) 🥈 @username: (0) || Você está na 2ª posição na classificação com 0.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    received: ClassVar[list] = [
        pytest.param(
            "en",
            "top 2 receivers: 🏆 @channelname: (25) 🥈 @username: (0) "
            "|| You are in the 2th position in the ranking with 0.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 2 receivers: 🏆 @channelname: (25) 🥈 @username: (0) "
            "|| Você está na 2ª posição na classificação com 0.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    total: ClassVar[list] = [
        pytest.param(
            "en",
            "top 2 total: 🏆 @username: (0) 🥈 @channelname: (0) || You are in the 1th position in the ranking with 0.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 2 total: 🏆 @username: (0) 🥈 @channelname: (0) || Você está na 1ª posição na classificação com 0.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
