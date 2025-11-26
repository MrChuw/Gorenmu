from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Command to get Twitch or hex color info.",
            "How to use: +color (username | hex)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando para obter informações de cor do Twitch ou hexadecimal.",
            "Como usar: +color (usuário | hex)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    hex_color: ClassVar[list] = [
        pytest.param(
            "en",
            "#FF4500 its Named: Vermilion https://color.mrchuw.com.br/hex/FF4500",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "#FF4500 Nome: Vermilion https://color.mrchuw.com.br/hex/FF4500",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    valid_nick: ClassVar[list] = [
        pytest.param(
            "en",
            "@some_nick color is: #FF4500. Named: Vermilion https://color.mrchuw.com.br/hex/FF4500",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "@some_nick a cor é: #FF4500. Nome: Vermilion https://color.mrchuw.com.br/hex/FF4500",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    hex_name: ClassVar[list] = [
        pytest.param(
            "en",
            "@ff4500 color is: #FF4500. Named: Vermilion || #FF4500 its Named: Vermilion "
            "https://color.mrchuw.com.br/hex/FF4500",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "@ff4500 a cor é: #FF4500. Nome: Vermilion || #FF4500 Nome: Vermilion "
            "https://color.mrchuw.com.br/hex/FF4500",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_db: ClassVar[list] = [
        pytest.param(
            "en",
            "@some_nick color is: #FF4500. Named: Vermilion || And has the following saved color: #FF4500. "
            "Named: Vermilion. https://color.mrchuw.com.br/hex/FF4500",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "@some_nick a cor é: #FF4500. Nome: Vermilion || E tem a seguinte cor salva: #FF4500. "
            "Nome: Vermilion. https://color.mrchuw.com.br/hex/FF4500",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_user_no_hex: ClassVar[list] = [
        pytest.param(
            "en",
            "User not found or valid hex color provided.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Usuário não encontrado ou cor hexadecimal válida fornecida.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_no_color: ClassVar[list] = [
        pytest.param(
            "en",
            "Provided user has no color defined on twitch.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "O usuário não tenha nenhuma cor definida no Twitch.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
