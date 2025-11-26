from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Gift someone your daily cookie.",
            "To use: +cookie gift (user_name) (amount|all)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Presenteie alguém com seus cookies.",
            "Para usar: +cookie gift (nome_do_usuário) (quantidade|all)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bot_nick: ClassVar[list] = [
        pytest.param("en", "I don't want your cookie.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "Não quero a seu cookie.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    yourself: ClassVar[list] = [
        pytest.param("en", "Did you try gifting it yourself, wow!", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "você tentou presentear você mesmo, uau!",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    unknown_user: ClassVar[list] = [
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

    other_user_no_cookie: ClassVar[list] = [
        pytest.param(
            "en",
            "User @channelname has not yet used any command related to cookies.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "O usuário @channelname ainda não usou nenhum comando relacionado aos cookies.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    other_user_zero: ClassVar[list] = [
        pytest.param("en", ["You didn't gift anything, wow!"], marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            ["Você não deu nada de presente, uau!"],
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    other_user_negative_amount: ClassVar[list] = [
        pytest.param(
            "en",
            ["You can't give negative cookies unless you're a cookie thief... and you're not, right?"],
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            ["Você não pode dar cookies negativos, a menos que seja um ladrão de cookies... e você não é, certo?"],
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    cooldown_no_stock: ClassVar[list] = [
        pytest.param(
            "en",
            ["You don`t have any cookies 🍪 stored or waiting to be redeemed. The next one arrives in 59"],
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            ["Você não tem nenhum cookie 🍪 armazenado ou aguardando para ser resgatado. O próximo chega em 59"],
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    other_user_all: ClassVar[list] = [
        pytest.param(
            "en",
            ["you gifted @channelname with 12 cookie 🎁"],
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            ["você presenteou @channelname com 12 cookie 🎁"],
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    other_user_no_amount: ClassVar[list] = [
        pytest.param("en", ["you gave @channelname a cookie 🎁"], marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            ["você deu um cookie para @channelname 🎁"],
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    other_user_exact_amount: ClassVar[list] = [
        pytest.param(
            "en",
            ["you gifted @channelname with 10 cookie 🎁"],
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            ["você presenteou @channelname com 10 cookie 🎁"],
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    other_user: ClassVar[list] = [
        pytest.param("en", ["you gave @channelname a cookie 🎁"], marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            ["você deu um cookie para @channelname 🎁"],
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    other_user_no_stock_cooldown: ClassVar[list] = [
        pytest.param(
            "en",
            [
                "you gifted @channelname with 5 cookie 🎁",
                "you gifted @channelname with 5 cookie 🎁",
                "To gift, you must first redeem the 2 cookies you have available.",
            ],
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            [
                "você presenteou @channelname com 5 cookie 🎁",
                "você presenteou @channelname com 5 cookie 🎁",
                "Para presentear, você deve primeiro resgatar os 2 cookies que você tem disponíveis.",
            ],
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
