# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
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

    live_on = [
        pytest.param(
            "en",
            r"^\('Title: .*? \|\| Stream started: .*? ago \((?:\d+ month[s]?, )?(?:\d+ day[s]?, )?\d+ hour[s]?, "
            r"\d+ minute[s]? and \d+\.\d+ second[s]?\)\. \|\| Views: \d+\. \|\| Playing: .*?\. \|\| "
            r"https://www\.twitch\.tv/xXCoolNickXx https://www\.twitch\.tv/videos/\d+\?t=\d+s',\)$",
            marks=pytest.mark.en,
            id="live-on-en",
        ),
        pytest.param(
            "pt_BR",
            r"^\('Título: .*?\. \|\| Transmissão iniciada: há .*? \((?:\d+ mês(?:es)?, )?(?:\d+ dia[s]?, )?\d+ "
            r"(?:hora|horas), \d+ (?:minuto|minutos) e \d+\.\d+ (?:segundo|segundos)\)\. \|\| Visualizações: \d+\. "
            r"\|\| Jogando: .*?\. \|\| https://www\.twitch\.tv/\w+ https://www\.twitch\.tv/videos/\d+\?t=\d+s',\)$",
            marks=pytest.mark.pt_BR,
            id="live-on-pt",
        ),
    ]

    live_off = [
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
            r"^\('Título: .*? \|\| Última transmissão: há .*? \((?:\d+ mês(?:es)?, )?(?:\d+ dia[s]?, )?(?:\d+ "
            r"hora[s]?, )?(?:\d+ minuto[s]? e )?\d+\.\d+ segundo[s]?\)\. \|\| https://www\.twitch\.tv/xXCoolNickXx "
            r"https://www\.twitch\.tv/videos/\d+',\)$",
            marks=pytest.mark.pt_BR,
            id="last-stream-pt",
        ),
    ]

    not_found = [
        pytest.param("en", "I couldn't find any user named @nonexistent_user.", marks=pytest.mark.en, id="notfound-en"),
        pytest.param(
            "pt_BR",
            "Não consegui encontrar nenhum usuário chamado @nonexistent_user.",
            marks=pytest.mark.pt_BR,
            id="notfound-pt",
        ),
    ]

    online_json = [
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

    offline_json = [
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
