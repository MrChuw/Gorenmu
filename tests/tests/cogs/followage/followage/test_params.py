# -*- coding: utf-8 -*-
import datetime

import pytest


class Params:
    decorators = [
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

    follow = [
        pytest.param("en", r"@username follows @username for ", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", r"@username segue @username ", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    not_follow = [
        pytest.param("en", "@username does not follow xxcoolchannelxx", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "@username não segue xxcoolchannelxx", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    follow_json = {
        "user": {"id": "744028864", "login": "xXCoolNickXx", "displayName": "xXCoolNickXx"},
        "channel": {"id": "28579002", "login": "xXCoolChannelXx", "displayName": "xXCoolChannelXx"},
        "statusHidden": False,
        "followedAt": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
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
        "meta": {"type": "prime", "tier": "1", "endsAt": "2025-10-25T07:20:00Z", "renewsAt": None, "giftMeta": None},
    }

    not_follow_json = {
        "user": {"id": "744028864", "login": "xXCoolNickXx", "displayName": "xXCoolNickXx"},
        "channel": {"id": "28579002", "login": "xXCoolChannelXx", "displayName": "xXCoolChannelXx"},
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
        "meta": {"type": "prime", "tier": "1", "endsAt": "2025-10-25T07:20:00Z", "renewsAt": None, "giftMeta": None},
    }
