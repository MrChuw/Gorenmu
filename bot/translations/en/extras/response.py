from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from bot.ext.commands import Context


class Response:
    def __init__(self, data: dict):
        self.ctx: Optional[Context] = data.get("ctx")
        self.success: Optional[bool] = data.get("success")
        self.response: Optional[str] = data.get("response")
        self.response_list: Optional[List[str]] = data.get("response_list")
        self.object: Optional[object] = data.get("object")
        self.handle: Optional[str] = data.get("handle")
        self.pipe: bool = data.get("pipe", True)
        self.response_string: str = ""

    def format_response(self, ctx: Context, *args: Any, **kwargs: Any) -> Response:
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


class CommandExemples:
    def __init__(self, data):
        self.items = [CommandExemplesItem(**item) for item in data] if data else False

    def __iter__(self):
        return iter(self.items) if self.items else iter([])


class CommandExemplesItem:
    def __init__(self, args, response):
        self.args = args
        self.response = response


class Admonitions:
    def __init__(self, admonitions):
        self.items = [AdmonitionItem(**item) for item in admonitions] if admonitions else False

    def __iter__(self):
        return iter(self.items) if self.items else iter([])


class AdmonitionItem:
    def __init__(self, admonition_type, title, message, position = "bottom"):
        if position not in {"top", "middle", "bottom"}:
            position = "bottom"
        self.type = admonition_type
        self.title = title
        self.message = message
        self.position = position




