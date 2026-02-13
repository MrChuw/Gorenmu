from __future__ import annotations

import inspect
import types
from contextvars import ContextVar
from pathlib import Path
from typing import TYPE_CHECKING, Any

from bot.ext import Command, Context
from bot.ext.translations.extras import ClassBase, LangDict, OtherTools, TBase
from bot.utils.singleton import Singleton

if TYPE_CHECKING:
    from bot.bot import Gorenmu

current_ctx: ContextVar[Context] = ContextVar("current_ctx")


"""
Criar uma forma de dumpar todas as traducoes para um json/xml/txt em ingles, onde esse json seria usado como base para
o weblate ou qualquer outro usar para traduzir.

def strftime(self, ctx: Context) -> str:
    with self.lang_dict.once("strftime"):
        self.lang_dict.add_with("en", "%m/%d/%Y in %I:%M %p")
        self.lang_dict.add_with(["pt_br", "pt"], "%d/%m/%Y às %H:%M:%S")
        self.lang_dict.add_translation_with("SupportTools.TimeTools.strftime_str")
    return self._untangle_str(ctx, "strftime")

e então ele adicionaria todas as traducoes para as linguas

talvez ter um
{
"SupportedLangs": ["es", "es-ES", "es-MX"]
}

que seria refente ao ["pt_br", "pt"] no add_with

"""  # NOQA


class Response:
    def __init__(
        self,
        ctx: Context,
        response: str | None = None,
        success: bool = True,
        response_list: list[str] | None = None,
        handle: str | None = None,
        response_string: str | None = None,
    ):
        self.ctx: Context = ctx
        self.success: bool = success
        self.response: str = response
        self.response_list: list[str] = response_list
        self.handle: str = handle
        self.response_string: str = response_string

    def format_response(self, response: str, *args: Any, **kwargs: Any) -> Response:
        self.response = response
        if args:
            self.response_string = self.response.format(*args, **kwargs)
        else:
            self.response_string = self.response
        return self


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
        self.items = [CommandExemplesItem(item) for item in data] if data else False

    def __iter__(self):
        return iter(self.items) if self.items else iter([])


class TranslationBase(ClassBase, metaclass=Singleton):
    def __init__(self, bot: Gorenmu, file):
        self.bot = bot
        self.command = None
        self.lang_dict: LangDict = LangDict()
        self.lang_dict.load_fluent_locales(Path(file).parent / "locales")

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

    class Exceptions(TBase):
        def __init__(self, parent: TranslationBase | None = None):
            super().__init__(parent, __file__)
            self._started = True
            self.prefix = "Exceptions"

        def empty(self, ctx: Context | None = None, success: bool = True) -> Response:
            return Response(ctx=ctx or self.ctx_get(), success=success, response_string="")

        def echo(
            self, args: str, ctx: Context | None = None, success: bool = True, handle: str | None = None
        ) -> Response:
            return Response(ctx=ctx or self.ctx_get(), success=success, handle=handle, response_string=f"{args}")

        def user_not_found_id(self, arg: str | int, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, id=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def user_not_found_name(self, name: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def time_expired(self, arg: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, time=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def no_content_provided(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def too_much_characters(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def message_too_long(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def no_id_provided(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def id_not_valid(self, arg: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, id=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def user_not_provided(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def guard_caught(self, cmd: str, reason, contact: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, cmd=cmd, reason=str(reason), contact=contact)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def unexpected_error(self, exception: Exception | str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, exception=str(exception))
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def error(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, dev=self.ctx_get().bot.dev_user.display_name)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def timeout(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def never_seen(self, arg: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, name=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def channel_not_found(self, arg: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, name=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def dev_required(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def owner_required(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def command_on_cooldown(self, arg: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, time=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def disabled(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def not_implemented(self, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def error_not_registered(self, arg: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, dev=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def command_not_pipeble(self, arg: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, cmd=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def pipe_response_error(self, arg: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, error=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def pipe_response(self, arg: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, response=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

        def lottery_seed(self, arg: str, ctx: Context | None = None) -> Response:
            text = self.get_text(self._cname, contact=arg)
            return Response(ctx=ctx or self.ctx_get(), success=False, response_string=text)

    Exceptions: Exceptions

    class SupportTools(OtherTools.SupportTools):
        def __init__(self, parent: TranslationBase | None = None) -> None:
            super().__init__(parent)

        @staticmethod
        def fake_stacktrace(message: str) -> Exception | None:
            exc = Exception(message)
            tb = types.TracebackType(tb_next=None, tb_frame=inspect.currentframe().f_back, tb_lasti=0, tb_lineno=1)
            exc.__traceback__ = tb
            return exc

    SupportTools: OtherTools.SupportTools

    class GenericWait(OtherTools.GenericWait):
        def __init__(self, parent: TranslationBase | None = None) -> None:
            super().__init__(parent)

    GenericWait: GenericWait
