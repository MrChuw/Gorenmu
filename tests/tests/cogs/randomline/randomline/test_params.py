from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Fetches a random message from the channel or from a user in the channel.",
            "to use: `+rl channel:(channel_name)` or `+rl user:(user_name)` or `+rl` or `+rl "
            "channel:(channel_name) user:(user_name)`",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Pega uma mensagem aleatória do canal ou de um usuário em um canal.",
            'Para usar: `+rl channel:<nome do canal>` ou `+rl user:<nome do usuário>` ou `+rl` '
            'ou `+rl channel:<nome do canal> user:<nome do usuário>`',
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param(
            "en",
            r"Some Text \(sent (\d+(?:\.\d+)?) seconds ago by @username\)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"Some Text \(enviado há (\d+(?:\.\d+)?) seconds por @username\)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    random_content: ClassVar[list] = [
        pytest.param(
            "en",
            r"Some Text \(sent (\d+(?:\.\d+)?) seconds ago by @username\)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"Some Text \(enviado há (\d+(?:\.\d+)?) seconds por @username\)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    target_user: ClassVar[list] = [
        pytest.param(
            "en",
            r"Some Text \(sent (\d+(?:\.\d+)?) seconds ago by @username\)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"Some Text \(enviado há (\d+(?:\.\d+)?) seconds por @username\)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    target_channel: ClassVar[list] = [
        pytest.param(
            "en",
            r"Some Text \(sent (\d+(?:\.\d+)?) seconds ago by @username\)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"Some Text \(enviado há (\d+(?:\.\d+)?) seconds por @username\)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    target_channel_no_messages: ClassVar[list] = [
        pytest.param(
            "en",
            "Couldn't find any message from channel @some_user_49.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Não encontrei nenhuma mensagem do canal @some_user_49.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    target_user_no_messages: ClassVar[list] = [
        pytest.param(
            "en",
            "I couldn't find any user named @some_user_51.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @some_user_51.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
