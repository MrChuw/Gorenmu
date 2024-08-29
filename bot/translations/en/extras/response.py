from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from bot.ext.commands import Context


class Response:
    def __init__(self, data: dict):
        self.ctx: Optional[Context] = data.get("ctx", None)
        self.success: Optional[bool] = data.get("success", None)
        self.response: Optional[str] = data.get("response", None)
        self.response_list: Optional[List[str]] = data.get("response_list", None)
        self.object: Optional[object] = data.get("object", None)
        self.handle: Optional[str] = data.get("handle", None)
        self.pipe: bool = data.get("pipe", True)
        self.response_string: str = ""

    def format_response(self, ctx: Context, *args: Any, **kwargs: Any) -> Response:
        if self is ctx.translations.Cookies.CookieCount.cookie:
            return ctx.translations.Cookies.CookieCount.format_cookie(self, ctx, *args, **kwargs)
        if self is ctx.translations.Tools.Weather.weather:
            return ctx.translations.Tools.Weather.format_weather(self, ctx, *args, **kwargs)
        self.ctx = ctx
        self.success = kwargs.pop("success", True)
        self.response_list = kwargs.pop("response_list", None)
        self.handle = kwargs.pop("handle", None)
        self.pipe = kwargs.pop("pipe", True)

        if args:
            self.response_string = self.response.format(*args, **kwargs)
        else:
            self.response_string = self.response
        return self
