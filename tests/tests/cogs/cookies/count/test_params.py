from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Get status about cookies.",
            "To use: +cookie count (user_name)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Veja o status dos cookies.",
            "Para usar: +cookie count (nome_do_usuário)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_name: ClassVar[list] = [
        pytest.param(
            "en",
            "you have already eaten 54 cookies 🥠. Has 8534 in stock. "
            "Was presented with 25. Gifted 93. And has a total of 2 unredeemed.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "você já comeu já comeu 54 biscoitos 🥠. Tem 8534 em estoque. "
            "Foi apresentado com 25. Presenteou 93. E tem um total de 2 não resgatados.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bot_name: ClassVar[list] = [
        pytest.param(
            "en",
            "I have infinite cookies, and I give away a fraction of them to you.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Tenho cookies infinitos e dou uma fração deles para você.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    other_user: ClassVar[list] = [
        pytest.param(
            "en",
            "@channelname have already eaten 54 cookies 🥠. Has 8534 in stock. "
            "Was presented with 25. Gifted 93. And has a total of 2 unredeemed.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "@channelname já comeu já comeu 54 biscoitos 🥠. Tem 8534 em estoque. "
            "Foi apresentado com 25. Presenteou 93. E tem um total de 2 não resgatados.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    author_with_a_bunch_of_things: ClassVar[list] = [
        pytest.param(
            "en",
            "you have already eaten 54 cookies 🥠. "
            "Has 8534 in stock. Was presented with 25. Gifted 93. "
            "And has a total of 2 unredeemed.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "você já comeu já comeu 54 biscoitos 🥠. "
            "Tem 8534 em estoque. Foi apresentado com 25. "
            "Presenteou 93. E tem um total de 2 não resgatados.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_not_found: ClassVar[list] = [
        pytest.param(
            "en",
            "user @random_user has not yet been registered and has not used any cookie commands.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "o usuário @random_user ainda não foi registrado e não usou nenhum comando de cookie.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
