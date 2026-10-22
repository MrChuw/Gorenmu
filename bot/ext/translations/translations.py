from __future__ import annotations

import asyncio
from contextvars import ContextVar
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

from bot.ext import Command, Context, commands
from bot.ext.translations.extras import GenericWait, LangDict, SupportTools, TBase
from bot.utils.singleton import Singleton

if TYPE_CHECKING:
    from bot.bot import Gorenmu

T_Comp = TypeVar("T_Comp")
current_ctx: ContextVar[Context] = ContextVar("current_ctx")


class Response:
    def __init__(
        self,
        ctx: Context,
        response: str = "",
        success: bool = True,
        response_list: list[str] | None = None,
        handle: str | None = None,
        response_string: str = "",
    ):
        if response_list is None:
            response_list = []
        if handle is None:
            handle = ""
        self.ctx: Context = ctx
        self.success: bool = success
        self.response: str = response
        self.response_list: list[str] = response_list
        self.handle: str | None = handle
        self.response_string: str = response_string

    def format_response(self, response: str, *args: Any, **kwargs: Any) -> Response:
        self.response = response
        if args:
            self.response = self.response.format(*args, **kwargs)
        else:
            self.response = self.response
        return self

    def __str__(self) -> str:
        return self.response


class AdmonitionItem:
    def __init__(self, admonition_type, title, message, position="bottom"):
        if position not in {"top", "middle", "bottom"}:
            position = "bottom"
        self.type = admonition_type
        self.title = title
        self.message = message
        self.position = position


class CommandExemplesItem:
    def __init__(self, data: dict):
        self.prefix = data.get("prefix", "")
        self.args = data.get("args", "")
        self.response = data.get("response", "")
        self.suffix = data.get("suffix", "")


class Admonitions:
    def __init__(self, admonitions):
        if admonitions:
            self.items = [AdmonitionItem(*item) for item in admonitions]
        else:
            self.items = []


class CommandExemples:
    def __init__(self, data):
        if not data:
            self.items = []
            return
        self.items = [CommandExemplesItem(item) for item in data]

    def __iter__(self):
        return iter(self.items)


class Exceptions(TBase):
    def __init__(self, parent: TranslationBase):
        self.prefix = "Exceptions"
        super().__init__(parent, __file__, is_base=True)
        self._started = True
        self.parent.register_locale(self.prefix, is_base=True)

    def empty(self, ctx: Context | None = None, success: bool = True) -> Response:
        return Response(ctx=ctx or self.ctx_get(), success=success, response="")

    def echo(
        self, args: str, ctx: Context | None = None, success: bool = True, handle: str | None = None
    ) -> Response:
        return Response(ctx=ctx or self.ctx_get(), success=success, handle=handle, response=f"{args}")

    def user_not_found_id(self, arg: str | int, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, id=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def user_not_found_name(self, name: str) -> Response:
        text = self.get_text(self._cname, name=name)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def time_expired(self, arg: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, time=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def time_limit_s(self, arg: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, time=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def no_content_provided(self, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def too_much_characters(self, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def message_too_long(self, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def no_id_provided(self, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def id_not_valid(self, arg: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, id=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def user_not_provided(self, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def guard_caught(self, cmd: str, reason, contact: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, cmd=cmd, reason=str(reason), contact=contact)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def unexpected_error(self, exception: Exception | str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, exception=str(exception))
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def error(self) -> Response:
        text = self.get_text(self._cname, dev=self.ctx_get().bot.dev_user.display_name or "")
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def timeout(self, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def never_seen(self, arg: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, name=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def channel_not_found(self, arg: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, name=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def dev_required(self, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def owner_required(self, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def command_on_cooldown(self, arg: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, time=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def disabled(self, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def not_implemented(self, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def error_not_registered(self, dev: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, dev=dev)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def command_not_pipeble(self, arg: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, cmd=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def pipe_response_error(self, arg: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, error=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def pipe_response(self, arg: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, response=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def lottery_seed(self, arg: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, contact=arg)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def user_opt_out(self, name: str, ctx: Context | None = None) -> Response:
        text = self.get_text(self._cname, name=name)
        return Response(ctx=ctx or self.ctx_get(), success=False, response=text)

    def translation_error(self, translation_name: str, language: str, dev_name: str) -> Response:
        text = self.get_text(self._cname, translation_name=translation_name, language=language, dev_name=dev_name)
        return Response(ctx=self.ctx_get(), success=False, response=text)


class TranslationBase[T_Comp](metaclass=Singleton):
    upper: T_Comp | None

    def __init__(self, bot: Gorenmu, file: str | None = None, upper: T_Comp | None = None):
        super().__init__()
        self.bot = bot
        self.upper: T_Comp | None = upper
        self.command = None
        self.lang_dict: LangDict = bot.CommandHandler.lang_dict
        self.locales_dir_base = Path(__file__).resolve().parent / "locales"
        self.locales_dir: Path | None = None
        if file:
            self.locales_dir = Path(file).resolve().parent / "locales"

        self.Exceptions: Exceptions = Exceptions(parent=self)
        self.SupportTools: SupportTools = SupportTools(parent=self)
        self.GenericWait: GenericWait = GenericWait(parent=self)

    def register_locale(self, prefix: str, is_base: bool = False) -> None:
        """Registra a pasta base ou a pasta do cog associada ao prefixo."""
        target_dir = self.locales_dir_base if is_base else self.locales_dir
        if target_dir and target_dir.exists():
            self.lang_dict.register_domain(prefix=prefix, folder=target_dir)

    @classmethod
    def ctx_get(cls):
        return current_ctx.get()

    @staticmethod
    def ctx_set(ctx: Context):
        return current_ctx.set(ctx)

    def get_decorator(self, ctx: Context | Command) -> TBase | None:
        decorators = None
        command_name = ctx.command.name if isinstance(ctx, Context) else ctx.name
        for name in self.__dict__:
            if name.lower() == command_name:
                decorators = getattr(self, name)
        return decorators
