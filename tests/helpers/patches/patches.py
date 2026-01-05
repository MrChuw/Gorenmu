from __future__ import annotations

import asyncio
import datetime
import types
from collections import defaultdict
from contextlib import AsyncExitStack
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

from freezegun import freeze_time

from bot.apis.ivrfi.parsers.subage import SubAge
from bot.apis.ivrfi.parsers.user import UserElement
from bot.apis.weather import Forecast, Geocoding
from bot.cogs.preview.command.preview import PreviewCmd
from bot.handlers import TokensHandler
from bot.models.base import TimestampMixin

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class MockBuilder:
    def __init__(self, mock_context):
        self.patches = defaultdict(list)
        self.mock_context = mock_context
        self._stack: AsyncExitStack | None = None
        self.patched = types.SimpleNamespace()
        self.Color: MockBuilder._Color = self._Color(self)
        self.Bot: MockBuilder._Bot = self._Bot(self)
        self.Session: MockBuilder._Session = self._Session(self)
        self.Emotes: MockBuilder._Emotes = self._Emotes(self)
        self.Errors: MockBuilder._Errors = self._Errors(self)
        self.Commands: MockBuilder._Commands = self._Commands(self)
        self.Asyncio: MockBuilder._Asyncio = self._Asyncio(self)
        self.ApiIvrFi: MockBuilder._ApiIvrFi = self._ApiIvrFi(self)
        self.Apis: MockBuilder._Apis = self._Apis(self)
        self.Default: MockBuilder._Default = self._Default(self)
        self.Handlers: MockBuilder._Handlers = self._Handlers(self)
        self.Db: MockBuilder._Db = self._Db(self)

    class _Errors:
        def __init__(self, builder):
            self.builder = builder
            self.bot: Gorenmu = (
                builder.mock_context.bot if hasattr(builder.mock_context, "bot") else builder.mock_context
            )

        def import_module(self, side_effect: Any = None) -> MockBuilder:
            self.builder.patches["import_module"].append(patch("importlib.import_module", side_effect=side_effect))
            return self.builder

        def os_execv(self, side_effect: Any = None) -> MockBuilder:
            self.builder.patches["execv"].append(patch("os.execv", side_effect=side_effect))
            return self.builder

        def send_bug(self, side_effect: Any = None) -> MockBuilder:
            self.builder.patches["execv"].append(
                patch.object(self.bot.CommandHandler, "send_bug", side_effect=side_effect)
            )
            return self.builder

    class _Color:
        def __init__(self, builder):
            self.builder = builder

        def name(self, return_value: str = "Vermilion") -> MockBuilder:
            self.builder.patches["color_name"].append(patch("bot.apis.color.Color.name", return_value=return_value))
            return self.builder

    class _Bot:
        def __init__(self, builder):
            self.builder = builder
            self.bot = builder.mock_context.bot if hasattr(builder.mock_context, "bot") else builder.mock_context

        def fetch_user_error(self, side_effect: Any = None) -> MockBuilder:
            self.builder.patches["fetch_user_error"].append(
                patch.object(self.bot, "fetch_user", side_effect=side_effect)
            )
            return self.builder

        def fetch_user(self, name="mock_user", user_id=1234, created_at=None, stream=False) -> MockBuilder:
            if name is None:
                mock_fetch = AsyncMock(return_value=None)
            else:
                mock_user = MagicMock()
                mock_user.name = name
                mock_user.id = user_id
                mock_user.stream = stream
                mock_user.created_at = created_at or datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC)
                mock_fetch = AsyncMock(return_value=mock_user)
            self.builder.patches["fetch_user"].append(patch.object(self.bot, "fetch_user", mock_fetch))
            return self.builder

        def fetch_chatters_color(self, return_value: str | None = "FF4500") -> MockBuilder:
            mock_color = MagicMock()
            mock_color.hex_clean = return_value
            mock_chatter = MagicMock()
            mock_chatter.color = mock_color if return_value else return_value
            mock_fetch = AsyncMock(return_value=[mock_chatter])
            self.builder.patches["fetch_chatters_color"].append(
                patch.object(self.bot, "fetch_chatters_color", mock_fetch)
            )
            return self.builder

        def silence_errors(self) -> MockBuilder:
            self.builder.patches["silence_errors"].append(patch.object(self.bot.log, "error"))
            return self.builder

        def fetch_videos(self) -> MockBuilder:
            return_value = MagicMock()
            return_value.id = "12345"
            mock_fetch = AsyncMock(return_value=[return_value])
            self.builder.patches["fetch_videos"].append(patch.object(self.bot, "fetch_videos", mock_fetch))
            return self.builder

        def delete_eventsub_subscription(self) -> MockBuilder:
            mock_delete = AsyncMock(return_value=True)
            self.builder.patches["delete_eventsub_subscription"].append(
                patch.object(self.bot, "delete_eventsub_subscription", mock_delete)
            )
            return self.builder

    class _Session:
        def __init__(self, builder):
            self.builder = builder

        def get_json(self, session, return_value: Any = None, side_effect=None, status: int = 200) -> MockBuilder:
            mock_response = AsyncMock()
            mock_response.json.return_value = return_value or {}
            mock_response.status = status
            mock_get = AsyncMock(return_value=mock_response, side_effect=side_effect)
            self.builder.patches["session_get_json"].append(patch.object(session, "get", mock_get))
            return self.builder

        def get(self, session, return_value: str | None = None, side_effect=None, status: int = 200) -> MockBuilder:
            mock_response = AsyncMock()
            mock_response.text = AsyncMock(return_value=return_value or "")
            mock_response.status = status
            mock_get = AsyncMock(return_value=mock_response, side_effect=side_effect)
            self.builder.patches["session_get"].append(patch.object(session, "get", mock_get))
            return self.builder

        def post_json(self, session, return_value: Any = None, side_effect=None, status: int = 200) -> MockBuilder:
            mock_response = AsyncMock()
            mock_response.json.return_value = return_value or {}
            mock_response.status = status
            mock_get = AsyncMock(return_value=mock_response, side_effect=side_effect)
            self.builder.patches["session_get_json"].append(patch.object(session, "post", mock_get))
            return self.builder

        def post(self, session, return_value: str | None = None, side_effect=None, status: int = 200) -> MockBuilder:
            mock_response = AsyncMock()
            mock_response.text = AsyncMock(return_value=return_value or "")
            mock_response.status = status
            mock_get = AsyncMock(return_value=mock_response, side_effect=side_effect)
            self.builder.patches["session_get"].append(patch.object(session, "post", mock_get))
            return self.builder

        def get_not_cached(
            self, target, return_value: str | None = None, side_effect=None, status: int = 200
        ) -> MockBuilder:
            mock_url = MagicMock()
            mock_url.human_repr = MagicMock(return_value=return_value)
            mock_response = MagicMock()
            mock_response.status = status
            mock_response.url = mock_url
            mock_get = AsyncMock(return_value=mock_response, side_effect=side_effect)
            self.builder.patches["get_not_cached"].append(patch.object(target, "get_not_cached", mock_get))
            return self.builder

    class _Emotes:
        def __init__(self, builder):
            self.builder = builder

        def get_7tv(self, return_value: Any = None) -> MockBuilder:
            self.builder.patches["get_7tv"].append(
                patch("bot.apis.emotes.Emotes.get_7tv", AsyncMock(return_value=return_value))
            )
            return self.builder

        def get_bttv(self, return_value: Any = None) -> MockBuilder:
            self.builder.patches["get_bttv"].append(
                patch("bot.apis.emotes.Emotes.get_bttv", AsyncMock(return_value=return_value))
            )
            return self.builder

        def get_ffz(self, return_value: Any = None) -> MockBuilder:
            self.builder.patches["get_ffz"].append(
                patch("bot.apis.emotes.Emotes.get_ffz", AsyncMock(return_value=return_value))
            )
            return self.builder

        def get_emotes(self, return_value: Any = None) -> MockBuilder:
            self.builder.patches["get_emotes"].append(
                patch("bot.apis.emotes.Emotes.get_emotes", AsyncMock(return_value=return_value))
            )
            return self.builder

        def get_random_by_amount(self, return_value: Any = None) -> MockBuilder:
            self.builder.patches["get_random_by_amount"].append(
                patch("bot.apis.emotes.Emotes.get_random_by_amount", AsyncMock(return_value=return_value))
            )
            return self.builder

    class _Commands:
        def __init__(self, builder):
            self.builder = builder
            import bot.cogs.randomscp.command.randomscp as randomscp

            self.randomscp = randomscp

        def get_scp(self, return_value: str | None = None, side_effect=None, status=200) -> MockBuilder:
            mock_get = AsyncMock(side_effect=side_effect)
            mock_url = MagicMock(human_repr=MagicMock(return_value=return_value or "www.some_url.com"))
            mock_get.return_value = MagicMock(status=status, url=mock_url)
            self.builder.patches["get_scp"].append(patch.object(self.randomscp, "get_scp", mock_get))
            return self.builder

        def get_preview(self, return_value: str | None = None, side_effect=None, status=200) -> MockBuilder:
            mock_get = AsyncMock(side_effect=side_effect)
            mock_get.return_value = return_value or "www.some_url.com"
            self.builder.patches["get_preview"].append(patch.object(PreviewCmd, "get_preview", mock_get))
            return self.builder

    class _Asyncio:
        def __init__(self, builder):
            self.builder = builder

        def sleep(self, seconds: float = 0) -> MockBuilder:
            async def fixed_sleep(_):
                if seconds > 0:
                    await asyncio.sleep(seconds)
                return None

            self.builder.patches["sleep"].append(patch("asyncio.sleep", AsyncMock(side_effect=fixed_sleep)))
            return self.builder

        def get_event_loop_time(self, times: list[int] | None = None) -> MockBuilder:
            times = times or [0, *list(range(1, 35))]
            mock_loop = MagicMock()
            mock_loop.time.side_effect = times
            self.builder.patches["get_event_loop"].append(patch("asyncio.get_event_loop", return_value=mock_loop))
            return self.builder

    class _Apis:
        def __init__(self, builder):
            self.builder = builder
            self.OpenMeteo: MockBuilder._Apis._OpenMeteo = self._OpenMeteo(builder)

        class _OpenMeteo:
            def __init__(self, builder):
                self.builder = builder

            def geocoding(self, response: list[dict[str, int]]) -> MockBuilder:
                mock_response = AsyncMock()
                mock_response.results = Geocoding({"results": response}).results
                self.builder.patches["apis_open_meteo_geocoding"].append(
                    patch("bot.apis.weather.open_meteo.OpenMeteo.geocoding", AsyncMock(return_value=mock_response))
                )
                return self.builder

            def forecast(self, data: dict[str, str | int]) -> MockBuilder:
                self.builder.patches["apis_open_meteo_forecast"].append(
                    patch("bot.apis.weather.open_meteo.OpenMeteo.forecast", AsyncMock(return_value=Forecast(data)))
                )
                return self.builder

    class _ApiIvrFi:
        def __init__(self, builder):
            self.builder = builder
            self.Twitch: MockBuilder._ApiIvrFi._Twitch = self._Twitch(builder)

        class _Twitch:
            def __init__(self, builder):
                self.builder = builder
                self.User: MockBuilder._ApiIvrFi._Twitch._User = self._User(builder)
                self.Channel: MockBuilder._ApiIvrFi._Twitch._Channel = self._Channel(builder)

            class _User:
                def __init__(self, builder):
                    self.builder = builder

                def fetch_user(self, dict_to_parse: dict | None = None) -> MockBuilder:
                    self.builder.patches["ivrfi_user_fetch_user"].append(
                        patch(
                            "bot.apis.ivrfi.api.ApiIvrFi.Twitch.User.fetch_user",
                            AsyncMock(
                                return_value=(UserElement.from_dict(dict_to_parse[0]) if dict_to_parse else None)
                            ),
                        )
                    )
                    return self.builder

            class _Channel:
                def __init__(self, builder):
                    self.builder = builder

                def fetch_preview(self, dict_to_parse: dict | None = None) -> MockBuilder:
                    self.builder.patches["ivrfi_user_fetch_user"].append(
                        patch(
                            "bot.apis.ivrfi.api.ApiIvrFi.Twitch.Channel.fetch_followage",
                            AsyncMock(return_value=(SubAge.from_dict(dict_to_parse) if dict_to_parse else None)),
                        )
                    )
                    return self.builder

    class _Default:
        def __init__(self, builder):
            self.builder = builder
            self.Datetime: MockBuilder._Default._Datetime = self._Datetime(builder)

        class _Datetime:
            def __init__(self, builder):
                self.builder = builder

            def now(self, time: datetime.datetime) -> MockBuilder:
                patcher = freeze_time(time)
                self.builder.patches["datetime_now"].append(patcher)
                return self.builder

            def now_forced(self, time: datetime.datetime) -> MockBuilder:
                class FixedDatetime(datetime.datetime):
                    @classmethod
                    def now(cls, tz=None):
                        return time

                self.builder.patches["datetime_now"].append(patch.object(datetime, "datetime", FixedDatetime))

                return self.builder

    class _Handlers:
        def __init__(self, builder):
            self.builder = builder
            self.TwitchTokens: MockBuilder._Handlers._TwitchTokens = self._TwitchTokens(builder)

        class _TwitchTokens:
            def __init__(self, builder):
                self.builder = builder

            def get_event_sub_subscriptions(self) -> MockBuilder:
                mock_sub = AsyncMock(return_value=True)
                self.builder.patches["get_event_sub_subscriptions"].append(
                    patch.object(TokensHandler, "get_event_sub_subscriptions", mock_sub)
                )

                return self.builder

    class _Db:
        def __init__(self, builder):
            self.builder = builder
            self.TimestampMixin: MockBuilder._Db._TimestampMixin = self._TimestampMixin(builder)

        class _TimestampMixin:
            def __init__(self, builder):
                self.builder = builder

            def updated_at(self, time) -> MockBuilder:
                p = patch.object(TimestampMixin, "updated_at", new_callable=PropertyMock, return_value=time)
                self.builder.patches["updated_at"].append(p)
                return self.builder

    async def __aenter__(self):
        self._stack = AsyncExitStack()  # NOQA
        for name, patch_list in self.patches.items():
            mocks = []
            for patcher in patch_list:
                mock_obj = self._stack.enter_context(patcher)
                mocks.append(mock_obj)
            setattr(self.patched, name, mocks[0] if len(mocks) == 1 else mocks)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._stack:
            await self._stack.aclose()
