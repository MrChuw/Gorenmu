from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, TYPE_CHECKING


from aiohttp_client_cache import CachedSession, SQLiteBackend
import aiohttp








class BotAPIRequestCache:
    def __init__(self, user_agent: str = "Gorenmu/2.0"):
        self.urls_expire_after = {}
        self.allowed_methods = ("GET", "HEAD", "POST")
        self.allowed_codes = (200,)
        self.headers = {'User-Agent': user_agent}

        self.cache: SQLiteBackend = SQLiteBackend(
                cache_name=".cache/bot-api-requests.db",
                allowed_methods=self.allowed_methods,
                include_headers=True,
                allowed_codes=self.allowed_codes
        )
        timeout = aiohttp.ClientTimeout(total=240)
        self.session: CachedSession = CachedSession(cache=self.cache, headers=self.headers, timeout=timeout)