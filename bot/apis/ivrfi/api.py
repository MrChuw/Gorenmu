# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp_client_cache import CachedSession
from yarl import URL

from bot.utils import Singleton

from .parsers.user import UserElement

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class Base:
    def __init__(self, bot: Gorenmu, session: CachedSession, url: str = None):
        self.bot = bot
        self.session = session
        self.url: URL = URL(url)


class ApiIvrFi(metaclass=Singleton):
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        self.session: CachedSession = bot.SessionsCaches.IvrFi.session

        for name, cls in vars(self.__class__).items():
            if isinstance(cls, type) and issubclass(cls, Base):
                setattr(self, name, cls(bot, self.session))

    class User(Base):
        def __init__(self, bot: Gorenmu, session: CachedSession, url: str = "https://api.ivr.fi/v2/twitch/user"):
            super().__init__(bot, session, url)

        async def fetch_user(self, name: str = None, user_id: int = None):
            base_url = self.url
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
