from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "This command will send a print and timestamp of the requested live stream.",
            "+preview (channel_name)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Este comando enviara um print e timestamp da live pedida.",
            "+preview (nome_do_canal)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    offline: ClassVar[list] = [
        pytest.param(
            "en",
            "Channel channelname is not live at the moment.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "O canal channelname não esta em live no momento.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    online: ClassVar[list] = [
        pytest.param(
            "en",
            r"Preview: link || VOD: https://www.twitch.tv/videos/12345?t=95566s",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"Preview: link || VOD: https://www.twitch.tv/videos/12345?t=95566s",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
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
