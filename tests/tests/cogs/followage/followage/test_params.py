import datetime
from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Command used to check how long someone has been following a channel.",
            "+followage (user) (channel)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando utilizado para verificar a quanto tempo alguém segue um canal.",
            "+followage (usuário) (canal)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    follow: ClassVar[list] = [
        pytest.param("en", "@username follows @username for 1 day", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "@username segue @username 1 dia", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    not_follow: ClassVar[list] = [
        pytest.param(
            "en",
            "@username does not follow xxcoolchannelxx",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "@username não segue xxcoolchannelxx",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    follow_json: ClassVar[dict] = {
        "user": {
            "id": "744028864",
            "login": "xXCoolNickXx",
            "displayName": "xXCoolNickXx",
        },
        "channel": {
            "id": "28579002",
            "login": "xXCoolChannelXx",
            "displayName": "xXCoolChannelXx",
        },
        "statusHidden": False,
        "followedAt": datetime.datetime(2025, 8, 7, 17, 5, 55, tzinfo=datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "streak": {
            "elapsedDays": 27,
            "daysRemaining": 3,
            "months": 6,
            "end": "2025-10-25T07:20:00Z",
            "start": "2025-09-25T07:20:00Z",
        },
        "cumulative": {
            "elapsedDays": 27,
            "daysRemaining": 3,
            "months": 14,
            "end": "2025-10-25T07:20:00Z",
            "start": "2025-09-25T07:20:00Z",
        },
        "meta": {
            "type": "prime",
            "tier": "1",
            "endsAt": "2025-10-25T07:20:00Z",
            "renewsAt": None,
            "giftMeta": None,
        },
    }

    not_follow_json: ClassVar[dict] = {
        "user": {
            "id": "744028864",
            "login": "xXCoolNickXx",
            "displayName": "xXCoolNickXx",
        },
        "channel": {
            "id": "28579002",
            "login": "xXCoolChannelXx",
            "displayName": "xXCoolChannelXx",
        },
        "statusHidden": False,
        "followedAt": None,
        "streak": {
            "elapsedDays": 27,
            "daysRemaining": 3,
            "months": 6,
            "end": "2025-10-25T07:20:00Z",
            "start": "2025-09-25T07:20:00Z",
        },
        "cumulative": {
            "elapsedDays": 27,
            "daysRemaining": 3,
            "months": 14,
            "end": "2025-10-25T07:20:00Z",
            "start": "2025-09-25T07:20:00Z",
        },
        "meta": {
            "type": "prime",
            "tier": "1",
            "endsAt": "2025-10-25T07:20:00Z",
            "renewsAt": None,
            "giftMeta": None,
        },
    }
