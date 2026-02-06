from __future__ import annotations

import asyncio
import json
import random
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING

from bot.utils.singleton import Singleton

if TYPE_CHECKING:
    from aiohttp_client_cache import CachedSession

    from bot.bot import Gorenmu
    from bot.ext import Context


class Error(BaseException): ...


class Emotes(metaclass=Singleton):
    def __init__(self, bot: Gorenmu, session: CachedSession):
        self.bot = bot
        self.session: CachedSession = session
        self.cached_emotes = {}
        self.sad_emotes = []
        self.happy_emotes = []
        self.pog_emotes = []
        self.love_emotes = []
        self.hug_emotes = []
        self.pat_emotes = []
        self.hit_emotes = []
        self.okay_emotes = []
        self.bed_emotes = []
        self.kiss_emotes = []

        self._load_emote_sets()

    def _load_emote_sets(self):
        current_dir = Path(__file__).parent
        file_path = current_dir / "emotes.json"

        if not file_path.exists():
            print(f"Warning: {file_path} not found.")
            return

        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)

        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    async def fetch_json(self, url) -> dict:
        try:
            response = await self.session.get(url)
            return None if response.status != 200 else await response.json()
        except Exception as e:
            raise e

    async def get_7tv(self, channel_id):
        try:
            url = f"https://7tv.io/v3/users/twitch/{channel_id}"
            data = await self.fetch_json(url)
            if data is None:  # Status != 200
                raise Error("7TV API Error or User Not Found")
            if not data.get("emote_set"):
                return []
            return [emote["name"] for emote in data["emote_set"]["emotes"]]
        except Exception as e:
            self.bot.log.error(f"Error fetching 7tv emotes for {channel_id}: {e}")
            return []

    async def get_bttv(self, channel_id):
        try:
            url = f"https://api.betterttv.net/3/cached/users/twitch/{channel_id}"
            data = await self.fetch_json(url)
            if data is None or data.get("message"):
                raise Error("BTTV API Error or User Not Found")  # NOQA

            return [emote["code"] for emote in data.get("channelEmotes", []) + data.get("sharedEmotes", [])]
        except Exception as e:
            self.bot.log.error(f"Error fetching bttv emotes for {channel_id}: {e}")
            return []

    async def get_ffz(self, channel_id):
        try:
            url = f"https://api.frankerfacez.com/v1/room/id/{channel_id}"
            data = await self.fetch_json(url)
            if data is None or data.get("status") == 404:
                raise Error("FFZ API Error or User Not Found")

            if set_id := data.get("room", {}).get("set"):
                return [emote["name"] for emote in data["sets"][str(set_id)]["emoticons"]]
            else:
                return []
        except Exception as e:
            self.bot.log.error(f"Error fetching ffz emotes for {channel_id}: {e}")
            return []

    async def fetch_emotes(self, channel_id) -> list[str]:
        namespace_main = f"{self.bot.config.CacheConfig.namespace}-emotes"
        namespace_fallback = f"{namespace_main}-fallback"
        sources = ["7tv", "bttv", "ffz"]
        tasks = [self.get_7tv(channel_id), self.get_bttv(channel_id), self.get_ffz(channel_id)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        fallback_map = await self.bot.cache.get(channel_id, namespace=namespace_fallback) or {}

        final_emotes = set()
        new_fallback_map = fallback_map.copy()

        for i, res in enumerate(results):
            service = sources[i]

            if isinstance(res, list):
                final_emotes.update(res)
                new_fallback_map[service] = res
            else:
                self.bot.log.warning(f"API {service} failed for {channel_id}. Using fallback.")
                old_service_emotes = fallback_map.get(service, [])
                final_emotes.update(old_service_emotes)
        all_emotes_list = list(final_emotes)
        data_to_cache = all_emotes_list or "EMPTY_CACHE"
        await self.bot.cache.set(
            channel_id, data_to_cache, namespace=namespace_main, ttl=timedelta(minutes=10).total_seconds()
        )
        await self.bot.cache.set(channel_id, new_fallback_map, namespace=namespace_fallback, ttl=None)
        return all_emotes_list

    async def get_emotes(self, channel_id: int) -> list[str]:
        namespace = f"{self.bot.config.CacheConfig.namespace}-emotes"
        cached = await self.bot.cache.get(channel_id, namespace=namespace)
        if cached == "EMPTY_CACHE":
            return []
        emotes = await self.fetch_emotes(channel_id=channel_id)
        return [] if emotes == "EMPTY_CACHE" else emotes

    async def _get_filtered_emotes(self, ctx: Context, base_emotes: list[str], fallback: str, amount: int) -> list[str]:
        channel_emotes = await self.get_emotes(channel_id=ctx.channel.id)
        emotes_set = {e.lower() for e in base_emotes}
        matching = [e for e in channel_emotes if e.lower() in emotes_set]
        if matching:
            return random.sample(matching, k=min(amount, len(matching)))
        return [fallback]

    async def _get_dynamic_emotion(self, ctx: Context, category: str, fallback: str, amount: int) -> list[str]:
        attr_name = f"{category}_emotes"
        base_emotes = getattr(self, attr_name, [])
        return await self._get_filtered_emotes(ctx, base_emotes, fallback, amount)

    async def get_happy(self, ctx: Context, amount: int = 1) -> list[str]:
        return await self._get_dynamic_emotion(ctx, "happy", "peepoHappy", amount)

    async def get_pog(self, ctx: Context, amount: int = 1) -> list[str]:
        return await self._get_dynamic_emotion(ctx, "pog", "PogChamp", amount)

    async def get_sad(self, ctx: Context, amount: int = 1) -> list[str]:
        return await self._get_dynamic_emotion(ctx, "sad", "peepoSad", amount)

    async def get_love(self, ctx: Context, amount: int = 1) -> list[str]:
        return await self._get_dynamic_emotion(ctx, "love", "WideLove", amount)

    async def get_hug(self, ctx: Context, amount: int = 1) -> list[str]:
        return await self._get_dynamic_emotion(ctx, "hug", "VirtualHug", amount)

    async def get_pat(self, ctx: Context, amount: int = 1) -> list[str]:
        return await self._get_dynamic_emotion(ctx, "pat", "nanaAYAYA", amount)

    async def get_hit(self, ctx: Context, amount: int = 1) -> list[str]:
        return await self._get_dynamic_emotion(ctx, "hit", "BOP", amount)

    async def get_okay(self, ctx: Context, amount: int = 1) -> list[str]:
        return await self._get_dynamic_emotion(ctx, "okay", "FeelsOkayMan", amount)

    async def get_bed(self, ctx: Context, amount: int = 1) -> list[str]:
        return await self._get_dynamic_emotion(ctx, "bed", "🛏", amount)

    async def get_kiss(self, ctx: Context, amount: int = 1) -> list[str]:
        return await self._get_dynamic_emotion(ctx, "kiss", "😚", amount)

    async def get_random_emote_by(self, emotion: str, ctx: Context, amount: int = 1) -> list[str]:
        fallbacks = {
            "happy": "peepoHappy",
            "pog": "PogChamp",
            "sad": "peepoSad",
            "love": "WideLove",
            "hug": "VirtualHug",
            "pat": "nanaAYAYA",
            "hit": "BOP",
            "okay": "FeelsOkayMan",
            "bed": "🛏",
            "kiss": "😚",
        }

        if emotion in fallbacks:
            return await self._get_dynamic_emotion(ctx, emotion, fallbacks[emotion], amount)
        return await self.get_emotes(channel_id=ctx.channel.id)

    async def get_random_by_amount(self, channel_id: int, amount: int = 1) -> list[str]:
        emotes = await self.get_emotes(channel_id=channel_id)
        return random.sample(emotes, k=min(amount, len(emotes)))
