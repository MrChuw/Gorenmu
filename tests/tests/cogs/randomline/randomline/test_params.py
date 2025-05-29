# -*- coding: utf-8 -*-

import pytest


class Params:
    no_content = [
        pytest.param(
            "en", r"Some Text \(sent (\d+(?:\.\d+)?) seconds ago by @some_user_49\)", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            r"Some Text \(enviado há (\d+(?:\.\d+)?) seconds por @some_user_49\)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    random_content = [
        pytest.param(
            "en", r"Some Text \(sent (\d+(?:\.\d+)?) seconds ago by @some_user_49\)", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            r"Some Text \(enviado há (\d+(?:\.\d+)?) seconds por @some_user_49\)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    target_user = [
        pytest.param(
            "en", r"Some Text \(sent (\d+(?:\.\d+)?) seconds ago by @some_user_50\)", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            r"Some Text \(enviado há (\d+(?:\.\d+)?) seconds por @some_user_50\)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    target_channel = [
        pytest.param(
            "en", r"Some Text \(sent (\d+(?:\.\d+)?) seconds ago by @some_user_49\)", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            r"Some Text \(enviado há (\d+(?:\.\d+)?) seconds por @some_user_49\)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    target_channel_no_messages = [
        pytest.param("en", "Couldn't find any message from channel @some_user_49 .", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "Não encontrei nenhuma mensagem do canal @some_user_49.", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    target_user_no_messages = [
        pytest.param("en", "I couldn't find any user named @some_user_51.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", "Não consegui encontrar nenhum usuário chamado @some_user_51.", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]
