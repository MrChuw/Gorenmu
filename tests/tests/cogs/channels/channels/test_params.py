from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Shows the list of channels where the bot is present.",
            "To use: +channels [quantity|ping]",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Mostra a lista de canais em que o bot está presente.",
            "Para usar: +channels [quantity|ping]",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param(
            "en",
            "@mrchuw️, @channelname️, @some_user_45️, @some_user_46️, "
            "@some_user_47️, @some_user_48️, @some_user_49️, @some_user_50️",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "@mrchuw️, @channelname️, @some_user_45️, @some_user_46️, "
            "@some_user_47️, @some_user_48️, @some_user_49️, @some_user_50️",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    params_quantity: ClassVar[list] = [
        pytest.param("en", "I'm logged in 8 channels.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Estou logado em 8 canais.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    params_: ClassVar[list] = [
        pytest.param("en", "blablabla", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "blablabla", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]
