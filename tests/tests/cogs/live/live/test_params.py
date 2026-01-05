from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Shows information about a channel's current or last broadcast.",
            "How to use: +live (channel or id)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Mostra informações sobre a live atual ou a última de um canal.",
            "Como usar: +live (canal ou id)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    live_on: ClassVar[list] = [
        pytest.param(
            "en",
            'Title: Live?! | !discord | !reddit | !roblox. || Stream started: a day ago '
            '(1 day, 2 hours, 34 minutes and 16 seconds). || Views: 42069. || Playing: Coolest Game. '
            '|| https://www.twitch.tv/xXCoolNickXx https://www.twitch.tv/videos/12345?t=95566s',
            marks=pytest.mark.en,
            id="live-on-en",
        ),
        pytest.param(
            "pt_BR",
            'Título: Live?! | !discord | !reddit | !roblox. || Transmissão iniciada: há um dia '
            '(1 dia, 2 horas, 34 minutos e 16 segundos). || Visualizações: 42069. || Jogando: Coolest Game. '
            '|| https://www.twitch.tv/xXCoolNickXx https://www.twitch.tv/videos/12345?t=95566s',
            marks=pytest.mark.pt_BR,
            id="live-on-pt",
        ),
    ]

    live_off: ClassVar[list] = [
        pytest.param(
            "en",
            'Title: Live?! | !discord | !reddit | !roblox. || Last stream: a day ago '
            '(1 day, 20 hours, 46 minutes and 28.07 seconds). || https://www.twitch.tv/xXCoolNickXx '
            'https://www.twitch.tv/videos/12345',
            marks=pytest.mark.en,
            id="last-stream-en",
        ),
        pytest.param(
            "pt_BR",
            'Título: Live?! | !discord | !reddit | !roblox. || Última transmissão: há um dia '
            '(1 dia, 20 horas, 46 minutos e 28.07 segundos). || https://www.twitch.tv/xXCoolNickXx '
            'https://www.twitch.tv/videos/12345',
            marks=pytest.mark.pt_BR,
            id="last-stream-pt",
        ),
    ]

    live_never: ClassVar[list] = [
        pytest.param(
            "en",
            "User channelname has never opened any stream.",
            marks=pytest.mark.en,
            id="last-stream-en",
        ),
        pytest.param(
            "pt_BR",
            "Usuário channelname nunca abriu nenhuma stream.",
            marks=pytest.mark.pt_BR,
            id="last-stream-pt",
        ),
    ]

    not_found: ClassVar[list] = [
        pytest.param(
            "en",
            "I couldn't find any user named @nonexistent_user.",
            marks=pytest.mark.en,
            id="notfound-en",
        ),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @nonexistent_user.",
            marks=pytest.mark.pt_BR,
            id="notfound-pt",
        ),
    ]

    online_json: ClassVar[list] = [
        {
            "displayName": "xXCoolNickXx",
            "login": "xXCoolNickXx",
            "id": "123456",
            "bio": "Cool lives :)",
            "stream": {
                "title": "Live?! | !discord | !reddit | !roblox",
                "id": "123456",
                "createdAt": "2025-08-07T14:31:39Z",
                "type": "live",
                "viewersCount": 42069,
                "game": {"displayName": "Coolest Game"},
            },
            "lastBroadcast": {
                "startedAt": "2025-08-07T14:31:43.372905Z",
                "title": "Live?! | !discord | !reddit | !roblox",
            },
        }
    ]

    offline_json: ClassVar[list] = [
        {
            "displayName": "xXCoolNickXx",
            "login": "xXCoolNickXx",
            "id": "123456",
            "bio": "Cool lives :)",
            "stream": None,
            "lastBroadcast": {
                "startedAt": "2025-08-06T20:19:26.925204Z",
                "title": "Live?! | !discord | !reddit | !roblox",
            },
        }
    ]

    never_json: ClassVar[list] = [
        {
            "displayName": "xXCoolNickXx",
            "login": "xXCoolNickXx",
            "id": "123456",
            "bio": "Cool lives :)",
            "stream": None,
            "lastBroadcast": {"startedAt": None},
        }
    ]
