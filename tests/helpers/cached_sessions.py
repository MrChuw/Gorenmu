from datetime import timedelta

from bot.utils.caches_base import BaseCachedSession


class SessionsCaches:
    def __init__(self, bot):
        self.UserAgent: str = "Mozilla/5.0 (compatible; Gorenmu/2.0; +https://github.com/MrChuw/Gorenmu)"
        for name, cls in vars(self.__class__).items():
            if isinstance(cls, type) and issubclass(cls, BaseCachedSession):
                setattr(self, name, cls(bot, useragent=self.UserAgent))  # NOQA

    async def close_all_sessions(self):
        for session in vars(self).values():
            if isinstance(session, BaseCachedSession):
                await session.close()

    class ColorSession(BaseCachedSession):
        def __init__(self, bot, useragent: str):
            self.allowed_codes = (200,)
            super().__init__(bot=bot, cache_name="Color_requests", useragent=useragent)

        def get_expiry_times(self) -> dict:
            return {"*/*": timedelta(seconds=2)}

    ColorSession: ColorSession
