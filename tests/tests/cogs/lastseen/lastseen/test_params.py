# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
import pytest


class Params:
    decorators = [
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

    bot = [
        pytest.param("en", "I am everywhere, at every moment...", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "eu estou em todos os lugares, a todo momento...", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    author = [
        pytest.param("en", "you were last seen here ☝️", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "você foi visto pela última vez aqui ☝️", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    not_found = [
        pytest.param("en", "I couldn't find any user named @nonexistent_user.", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @nonexistent_user.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    not_authorized = [
        pytest.param("en", r"@no_mention_user️ was last seen \d+\ minutes ago", marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", r"@no_mention_user️ foi visto ultima vez há \d+\ minutos", marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]

    last_seen = [
        pytest.param(
            "en",
            r"@status_user_50 was last seen in @channelname: Some Text \(0\.\d+ seconds\)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"@status_user_50 foi visto em @channelname pela última vez: Some Text \(0\.\d+ seconds\)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
