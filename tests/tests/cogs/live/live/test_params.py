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
            r"^Title: .*? \|\| Stream started: .*? ago \((?:\d+ year[s]?, )?(?:\d+ month[s]?, )?(?:\d+ day[s]?, )?\d+ "
            r"hour[s]?, \d+ minute[s]? and \d+\.\d+ second[s]?\)\. \|\| Views: \d+\. \|\| Playing: .*?\. \|\| "
            r"https://www\.twitch\.tv/xXCoolNickXx https://www\.twitch\.tv/videos/\d+\?t=\d+s$",
            marks=pytest.mark.en,
            id="live-on-en",
        ),
        pytest.param(
            "pt_BR",
            r"Título:\s*(?P<title>.+?)\s*\|.*?\|\|\s*Transmissão iniciada:\s*há\s*\d+\s*\w+.*?\|\|\s*Visualizações:"
            r"\s*(?P<views>\d+).*?\|\|\s*Jogando:\s*(?P<game>.+?)\s*\|\|\s*(?P<url1>https?://[^\s\?]+)(?:\s*"
            r"(?P<url2>https?://[^\s\?]+))?",
            marks=pytest.mark.pt_BR,
            id="live-on-pt",
        ),
    ]

    live_off: ClassVar[list] = [
        pytest.param(
            "en",
            r"Title: .*? \|\| Last stream: .*? ago \((?:\d+ month[s]?, )?(?:\d+ day[s]?, )?(?:\d+ hour[s]?, )?("
            r"?:\d+ minute[s]? and )?\d+\.\d+ second[s]?\)\. \|\| https://www\.twitch\.tv/xXCoolNickXx "
            r"https://www\.twitch\.tv/videos/\d+",
            marks=pytest.mark.en,
            id="last-stream-en",
        ),
        pytest.param(
            "pt_BR",
            r"Título:\s*(?P<title>.+?)\s*\|.*?\|\|\s*Última transmissão:\s*há\s*\d+\s*\w+.*?\|\|\s*(?P<url1>https?:"
            r"//[^\s\?]+)(?:\s*(?P<url2>https?://[^\s\?]+))?",
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
