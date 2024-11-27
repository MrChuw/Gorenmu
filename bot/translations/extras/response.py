from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from bot.ext import Context


class Response:
    def __init__(self, data: dict = None, response: str = None):
        if data is None:
            data = {}
        if response is not None:
            data["response"] = response
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
        if not data:
            self.items = []
            return
        self.items = [CommandExemplesItem(item) for item in data] if data else False

    def __iter__(self):
        return iter(self.items) if self.items else iter([])



class CommandExemplesItem:
    def __init__(self, data: dict):
        self.args = data.get("args", "")
        self.response = data.get("response", "")


class Admonitions:
    def __init__(self, admonitions):
        self.items = [AdmonitionItem(**item) for item in admonitions] if admonitions else False

    def __iter__(self):
        return iter(self.items) if self.items else iter([])


class AdmonitionItem:
    def __init__(self, admonition_type, title, message, position='bottom'):
        if position not in {"top", "middle", "bottom"}:
            position = "bottom"
        self.type = admonition_type
        self.title = title
        self.message = message
        self.position = position


class BaseFunctions:
    ctx: Context

    def __init__(self, obj, fallback):
        if type(obj) is dict:
            self.obj = obj
            self.fallback = obj if fallback is None else fallback
        if type(obj) is tuple:
            self.obj = obj[0]
            self.fallback = obj[1]

    def get_object(self, key: str) -> [dict, dict]:
        if key in self.obj:
            return self.obj[key]
        elif key in self.fallback:
            return self.fallback[key]
        else:
            raise KeyError(f"Key '{key}' not found in either base or fallback.")

    def get_object_or_none(self, key: str) -> [dict, dict]:
        if key in self.obj:
            return self.obj[key]
        elif key in self.fallback:
            return self.fallback[key]
        else:
            return None

    def get_base(self, key: str) -> [dict, dict]:
        if key in self.obj:
            return self.obj[key], self.fallback[key]
        elif key in self.fallback:
            return self.fallback[key], self.fallback[key]
        else:
            raise KeyError(f"Key '{key}' not found in either base or fallback.")

    def __iter__(self):
        unique_keys = set(self.obj.keys()).union(self.fallback.keys())
        return iter(unique_keys)

    def initialize_objects(self, names, cls):
        for name, args in names:
            base = self.get_object(name)
            translation_class = getattr(cls, name)
            setattr(self, name, translation_class(base, **args))

    def initialize_bases(self, names, cls):
        for name, args in names:
            base = self.get_base(name)
            translation_class = getattr(cls, name)
            setattr(self, name, translation_class(base, **args))

    def initialize_responses(self, names):
        for name, args in names:
            base = self.get_object(name)
            setattr(self, name, Response(response=base, **args))







