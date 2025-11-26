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
            "top 5 stocked: 🏆 @channelname: (8534) 🥈 @some_user_45: (4185) 🥉 @some_user_44: (4092) "
            "🏅 @some_user_43: (3999) 🏅 @some_user_42: (3906) || You are in the 8th position in the ranking with 10.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 5 stocked: 🏆 @channelname: (8534) 🥈 @some_user_45: (4185) 🥉 @some_user_44: (4092) "
            "🏅 @some_user_43: (3999) 🏅 @some_user_42: (3906) || Você está na 8ª posição na classificação com 10.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    stocked: ClassVar[list] = [
        pytest.param(
            "en",
            "top 5 stocked: 🏆 @channelname: (8534) 🥈 @some_user_45: (4185) "
            "🥉 @some_user_44: (4092) 🏅 @some_user_43: (3999) 🏅 @some_user_42: "
            "(3906) || You are in the 8th position in the ranking with 10.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 5 stocked: 🏆 @channelname: (8534) 🥈 @some_user_45: (4185) "
            "🥉 @some_user_44: (4092) 🏅 @some_user_43: (3999) 🏅 @some_user_42: (3906)"
            " || Você está na 8ª posição na classificação com 10.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    consumed: ClassVar[list] = [
        pytest.param(
            "en",
            "top 5 cookiers: 🏆 @some_user_45: (3285) 🥈 @some_user_44: (3212) "
            "🥉 @some_user_43: (3139) 🏅 @some_user_42: (3066) 🏅 @some_user_41: "
            "(2993) || You are in the 8th position in the ranking with 0.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 5 cookiers: 🏆 @some_user_45: (3285) 🥈 @some_user_44: (3212) "
            "🥉 @some_user_43: (3139) 🏅 @some_user_42: (3066) 🏅 @some_user_41: (2993)"
            " || Você está na 8ª posição na classificação com 0.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    donated: ClassVar[list] = [
        pytest.param(
            "en",
            "top 5 givers: 🏆 @some_user_45: (2520) 🥈 @some_user_44: (2464) "
            "🥉 @some_user_43: (2408) 🏅 @some_user_42: (2352) 🏅 @some_user_41: "
            "(2296) || You are in the 8th position in the ranking with 0.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 5 givers: 🏆 @some_user_45: (2520) 🥈 @some_user_44: (2464) "
            "🥉 @some_user_43: (2408) 🏅 @some_user_42: (2352) 🏅 @some_user_41: (2296)"
            " || Você está na 8ª posição na classificação com 0.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    received: ClassVar[list] = [
        pytest.param(
            "en",
            "top 5 receivers: 🏆 @some_user_45: (2430) 🥈 @some_user_44: (2376) "
            "🥉 @some_user_43: (2322) 🏅 @some_user_42: (2268) 🏅 @some_user_41: "
            "(2214) || You are in the 8th position in the ranking with 0.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 5 receivers: 🏆 @some_user_45: (2430) 🥈 @some_user_44: (2376) "
            "🥉 @some_user_43: (2322) 🏅 @some_user_42: (2268) 🏅 @some_user_41: (2214)"
            " || Você está na 8ª posição na classificação com 0.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    total: ClassVar[list] = [
        pytest.param(
            "en",
            "top 5 total: 🏆 @some_user_40: (0) 🥈 @some_user_41: (0) "
            "🥉 @some_user_42: (0) 🏅 @some_user_43: (0) 🏅 @some_user_44: "
            "(0) || You are in the 1th position in the ranking with 0.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "top 5 total: 🏆 @some_user_40: (0) 🥈 @some_user_41: (0) "
            "🥉 @some_user_42: (0) 🏅 @some_user_43: (0) 🏅 @some_user_44: (0)"
            " || Você está na 1ª posição na classificação com 0.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
