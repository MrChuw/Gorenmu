# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp_client_cache import CachedSession
from yarl import URL

from bot.utils.singleton import Singleton

from .parsers.subage import SubAge
from .parsers.user import UserElement

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class Base:
    def __init__(self, bot: Gorenmu, session: CachedSession, url: URL = None):
        self.bot = bot
        self.session = session
        self.base_url: URL = url


class ApiIvrFi(metaclass=Singleton):
    def __init__(self, bot: Gorenmu, session: CachedSession):
        self.bot = bot
        self.session: CachedSession = session
        self.base_url: URL = URL("https://api.ivr.fi/v2/")

        for name, cls in vars(self.__class__).items():
            if isinstance(cls, type) and issubclass(cls, Base):
                setattr(self, name, cls(bot, self.session, self.base_url))

    class Twitch(Base):
        def __init__(self, bot: Gorenmu, session: CachedSession, base_url: URL):
            self.bot = bot
            self.session: CachedSession = session
            self.base_url: URL = base_url / "twitch"

            for name, cls in vars(self.__class__).items():
                if isinstance(cls, type) and issubclass(cls, Base):
                    setattr(self, name, cls(bot, self.session, self.base_url))
            super().__init__(bot, session, self.base_url)

        class User(Base):
            def __init__(self, bot: Gorenmu, session: CachedSession, url):
                super().__init__(bot, session, url / "user")

            async def fetch_user(self, name: str = None, user_id: int = None) -> UserElement:
                base_url = self.base_url
                if name:
                    full_url = base_url.update_query(login=name)
                elif user_id:
                    full_url = base_url.update_query(id=user_id)
                else:
                    raise RuntimeError("No user name or user id provided.")
                response = await self.session.get(full_url)
                json_response = await response.json()
                return UserElement.from_dict(json_response[0]) if json_response else None

        User: User

        class Channel(Base):
            def __init__(self, bot: Gorenmu, session: CachedSession, url):
                super().__init__(bot, session, url / "subage")

            async def fetch_followage(self, channel: str, user: str) -> SubAge:
                base_url = self.base_url
                full_url = base_url / user / channel
                response = await self.session.get(full_url)
                json_response = await response.json()
                return SubAge.from_dict(json_response) if json_response else None

        Channel: Channel

    Twitch: Twitch
