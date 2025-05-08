# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import random
from datetime import timedelta
from typing import TYPE_CHECKING

from aiohttp_client_cache import CachedSession

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.models import User


class Emotes:
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        self.session: CachedSession = bot.SessionsCaches.EmotesCachedSession.session
        self.cached_emotes = {}
        self.sad_emotes = ['sadge', 'sadgecry', 'sadcat', 'sadchamp']  # NOQA
        self.happy_emotes = ['peepoglad', 'gladge', 'peepohappy', 'peepohappyu', 'happycat']  # NOQA
        self.pog_emotes = ['pog', 'pogu', 'pagbounce', 'pogg', 'pogs', 'noway', 'nowaying', 'nowaycat']  # NOQA

    async def fetch_json(self, url) -> dict:
        try:
            response = await self.session.get(url)
            return None if response.status != 200 else await response.json()
        except Exception as e:
            raise e

    async def get_7tv(self, channel_id):
        try:
            url = f'https://7tv.io/v3/users/twitch/{channel_id}'
            data = await self.fetch_json(url)
            if not data or data.get('error_code') == 404 or data.get('emote_set') is None:
                return []
            return [emote['name'] for emote in data['emote_set']['emotes']]
        except Exception as e:
            self.bot.log.error(f'Error fetching 7tv emotes for {channel_id}: {e}')
            return []

    async def get_bttv(self, channel_id):
        try:
            url = f'https://api.betterttv.net/3/cached/users/twitch/{channel_id}'
            data = await self.fetch_json(url)
            if not data or data.get('message'):
                return []
            return [emote['code'] for emote in data.get('channelEmotes', []) + data.get('sharedEmotes', [])]
        except Exception as e:
            self.bot.log.error(f'Error fetching bttv emotes for {channel_id}: {e}')
            return []

    async def get_ffz(self, channel_id):
        try:
            url = f'https://api.frankerfacez.com/v1/room/id/{channel_id}'
            data = await self.fetch_json(url)
            if not data or data.get('status') == 404:
                return []
            set_id = data['room']['set']
            return [emote['name'] for emote in data['sets'][str(set_id)]['emoticons']]
        except Exception as e:
            self.bot.log.error(f'Error fetching ffz emotes for {channel_id}: {e}')
            return []

    async def fetch_emotes(self, channel_id) -> list[str]:
        ttv, bttv, ffz = await asyncio.gather(
                self.get_7tv(channel_id),
                self.get_bttv(channel_id),
                self.get_ffz(channel_id),
                return_exceptions=True
        )

        all_emotes = []
        for source in (ttv, bttv, ffz):
            if isinstance(source, list):
                all_emotes.extend(source)

        await self.bot.cache.set(channel_id, all_emotes, namespace="emotes", ttl=timedelta(minutes=15).total_seconds())
        return all_emotes

    async def get_emotes(self, channel_id: int) -> list[str]:
        return (await self.bot.cache.get(channel_id, namespace="emotes") or
                await self.fetch_emotes(channel_id=channel_id))

    async def get_happy(self, channel_id: int, user: User, amount: int = 1) -> list[str]:
        emotes_ = self.happy_emotes + user.translations.SupportTools.Emotes.emotions.pog
        emotes_set = {emote.lower() for emote in emotes_}
        emotes = await self.get_emotes(channel_id=channel_id)
        if matching_emotes := [emote for emote in emotes if emote.lower() in emotes_set]:
            return random.sample(matching_emotes, k=min(amount, len(matching_emotes)))
        else:
            return ["peepoHappy"]

    async def get_pog(self, channel_id: int, user: User, amount: int = 1) -> list[str]:
        emotes_ = self.pog_emotes + user.translations.SupportTools.Emotes.emotions.pog
        emotes_set = {emote.lower() for emote in emotes_}
        emotes = await self.get_emotes(channel_id=channel_id)
        if matching_emotes := [emote for emote in emotes if emote.lower() in emotes_set]:
            return random.sample(matching_emotes, k=min(amount, len(matching_emotes)))
        else:
            return ["PogChamp"]

    async def get_sad(self, channel_id: int, user: User, amount: int = 1) -> list[str]:
        emotes_ = self.sad_emotes + user.translations.SupportTools.Emotes.emotions.sad
        emotes_set = {emote.lower() for emote in emotes_}
        emotes = await self.get_emotes(channel_id=channel_id)
        if matching_emotes := [emote for emote in emotes if emote.lower() in emotes_set]:
            return random.sample(matching_emotes, k=min(amount, len(matching_emotes)))
        else:
            return ["PoroSad"]

    async def get_random_emote_by(self, channel_id: int, emotion: str, user: User) -> list[str]:
        if emotion == "happy":
            return await self.get_happy(channel_id=channel_id, user=user)
        elif emotion == "pog":
            return await self.get_pog(channel_id=channel_id, user=user)
        elif emotion == "sad":
            return await self.get_sad(channel_id=channel_id, user=user)
        else:
            return await self.get_emotes(channel_id=channel_id)

    async def get_random_by_amount(self, channel_id: int, amount: int = 1) -> list[str]:
        emotes = await self.get_emotes(channel_id=channel_id)
        return random.sample(emotes, k=min(amount, len(emotes)))
