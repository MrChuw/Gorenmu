from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Command used to create a reminder for when you type in chat or with a set time.",
            "How to use: +remindme <message> or +remindme in 5h <message>.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando usado para criar um lembrete para quando digitar no chat ou com tempo determinado.",
            "Como usar: +remindme <mensagem> ou +remindme in 5h <mensagem>.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_content: ClassVar[list] = [
        pytest.param(
            "en",
            "You need to provide content for this command.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Você precisa fornecer conteúdo para este comando.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    user_not_found: ClassVar[list] = [
        pytest.param(
            "en",
            "I couldn't find any user named @buy.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @buy.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    remind_me: ClassVar[list] = [
        pytest.param(
            "en",
            "you will be reminded the next time you type in chat (1)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "você será lembrado na próxima vez que você digitar no chat (1)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    dispatched: ClassVar[list] = [
        pytest.param(
            "en",
            r"^username, you left a reminder: buy milk \(1 minute and 3\d seconds ago\)$",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"^username, você deixou um lembrete: buy milk \(há 1 minuto e 3\d segundos\)$",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
