from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Used to see the last time a user was online.",
            "Usage: +lastseen (user)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Usado para ver a ultima vez que um usuário esteve online.",
            "Uso: +lastseen (usuário)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bot: ClassVar[list] = [
        pytest.param("en", "I am everywhere, at every moment...", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "eu estou em todos os lugares, a todo momento...",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    author: ClassVar[list] = [
        pytest.param("en", "you were last seen here ☝️", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "você foi visto pela última vez aqui ☝️",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    not_found: ClassVar[list] = [
        pytest.param(
            "en",
            "I couldn't find any user named @nonexistent_user.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @nonexistent_user.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    not_authorized: ClassVar[list] = [
        pytest.param(
            "en",
            "@no_mention_user️ was last seen a day ago",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "@no_mention_user️ foi visto ultima vez há um dia",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    last_seen: ClassVar[list] = [
        pytest.param(
            "en",
            "@status_user_50 was last seen in @channelname: Some Text (1 day)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "@status_user_50 foi visto em @channelname pela última vez: Some Text (1 dia)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
