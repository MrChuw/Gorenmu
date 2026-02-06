from __future__ import annotations

import inspect
import types
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any

from bot.ext import Command, Context, commands
from bot.ext.translations.extras import ClassBase, OtherTools, TBase
from bot.utils.singleton import Singleton

if TYPE_CHECKING:
    from twitchio.ext.commands import GuardFailure

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
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        self.command = None

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
            super().__init__(parent)

        @staticmethod
        def empty(ctx: commands.Context, success: bool = True) -> Response:
            return Response(ctx=ctx, success=success).format_response("")

        @staticmethod
        def echo(ctx: Context, args: str, success: bool = True, handle: str | None = None) -> Response:
            return Response(ctx=ctx, success=success, handle=handle).format_response(f"{args}")

        def user_not_found_id(self, ctx: Context, arg: str | int) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("user_not_found_id"):
                self.lang_dict.add_with("en", "I couldn't find any user with id {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Não consegui encontrar nenhum usuário com id {}.")
            return response.format_response(self._untangle_str(ctx, "user_not_found_id"), arg)

        def user_not_found_name(self, ctx: Context, name: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("user_not_found_name"):
                self.lang_dict.add_with("en", "I couldn't find any user named @{}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Não consegui encontrar nenhum usuário chamado @{}.")
            return response.format_response(self._untangle_str(ctx, "user_not_found_name"), name)

        def time_expired(self, ctx: Context, arg: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("time_expired"):
                self.lang_dict.add_with("en", "Time {} has already expired.")
                self.lang_dict.add_with(["pt_br", "pt"], "O tempo {} já expirou.")
            return response.format_response(self._untangle_str(ctx, "time_expired"), arg)

        def no_content_provided(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("no_content_provided"):
                self.lang_dict.add_with("en", "You need to provide content for this command.")
                self.lang_dict.add_with(["pt_br", "pt"], "Você precisa fornecer conteúdo para este comando.")
            return response.format_response(self._untangle_str(ctx, "no_content_provided"))

        def too_much_characters(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("too_much_characters"):
                self.lang_dict.add_with("en", "The message must have a maximum of 450 characters.")
                self.lang_dict.add_with(["pt_br", "pt"], "A mensagem deve ter no máximo 450 caracteres.")
            return response.format_response(self._untangle_str(ctx, "too_much_characters"))

        def message_too_long(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("message_too_long"):
                self.lang_dict.add_with("en", "This message is too long.")
                self.lang_dict.add_with(["pt_br", "pt"], "Esta mensagem é muito longa.")
            return response.format_response(self._untangle_str(ctx, "message_too_long"))

        def no_id_provided(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("no_id_provided"):
                self.lang_dict.add_with("en", "You need to provide a valid numeric ID.")
                self.lang_dict.add_with(["pt_br", "pt"], "Você precisa fornecer um ID numérico válido.")
            return response.format_response(self._untangle_str(ctx, "no_id_provided"))

        def id_not_valid(self, ctx: Context, arg: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("id_not_valid"):
                self.lang_dict.add_with("en", "{} is not a valid ID.")
                self.lang_dict.add_with(["pt_br", "pt"], "{} não é um ID valido.")
            return response.format_response(self._untangle_str(ctx, "id_not_valid"), arg)

        def user_not_provided(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("user_not_provided"):
                self.lang_dict.add_with("en", "No target user provided!")
                self.lang_dict.add_with(["pt_br", "pt"], "Nenhum usuário alvo fornecido!")
            return response.format_response(self._untangle_str(ctx, "user_not_provided"))

        def guard_caught(self, ctx: Context, cmd: str, reason: GuardFailure, contact: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("guard_caught"):
                self.lang_dict.add_with(
                    "en",
                    'You are not authorized to use the "{}" command due to "{}". '
                    "If you think this is an error, contact @{}.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    'Você não está autorizado a usar o comando "{}" motivo: "{}". '
                    "Se achar que isso é um erro, entre em contato com @{}.",
                )
            return response.format_response(self._untangle_str(ctx, "guard_caught"), cmd, reason, contact)

        def unexpected_error(self, ctx: Context, exception: Exception | str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("unexpected_error"):
                self.lang_dict.add_with("en", "An error occurred, please try again: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Ocorreu um erro. Tente novamente: {}")
            return response.format_response(self._untangle_str(ctx, "unexpected_error"), exception)

        def error(self, ctx: Context = None) -> Response:
            ctx = ctx or self.ctx_get()
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "An unexpected error occurred. Please report it to @{} on whispers.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Ocorreu um erro inesperado. Por favor, reporte-o para @{} nos whispers.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), ctx.bot.dev_user.display_name)

        def timeout(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("timeout"):
                self.lang_dict.add_with("en", "It's been 30 seconds and I can't find any valid links.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Já se passaram 30 segundos e não consegui encontrar nenhum link válido."
                )
            return response.format_response(self._untangle_str(ctx, "timeout"))

        def never_seen(self, ctx: Context, arg: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("never_seen"):
                self.lang_dict.add_with("en", "I don't remember ever seeing any @{}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Não me lembro de ter visto nenhum @{}.")
            return response.format_response(self._untangle_str(ctx, "never_seen"), arg)

        def channel_not_found(self, ctx: Context, arg: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("channel_not_found"):
                self.lang_dict.add_with("en", "I couldn't find any channel named @{}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Não consegui encontrar nenhum canal chamado @{}.")
            return response.format_response(self._untangle_str(ctx, "channel_not_found"), arg)

        def dev_required(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("dev_required"):
                self.lang_dict.add_with("en", "you need to be my creator to run this command.")
                self.lang_dict.add_with(["pt_br", "pt"], "você precisa ser meu criador para executar este comando.")
            return response.format_response(self._untangle_str(ctx, "dev_required"))

        def owner_required(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("owner_required"):
                self.lang_dict.add_with("en", "commands reserved for the bot owner.")
                self.lang_dict.add_with(["pt_br", "pt"], "comandos reservados para o proprietário do bot.")
            return response.format_response(self._untangle_str(ctx, "owner_required"))

        def command_on_cooldown(self, ctx: Context, arg: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("command_on_cooldown"):
                self.lang_dict.add_with("en", "to use the command again, come back in {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "para usar o comando novamente, volte em {}.")
            return response.format_response(self._untangle_str(ctx, "command_on_cooldown"), arg)

        def not_implemented(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("not_implemented"):
                self.lang_dict.add_with("en", "this command is temporarily disabled.")
                self.lang_dict.add_with(["pt_br", "pt"], "este comando está temporariamente desativado.")
            return response.format_response(self._untangle_str(ctx, "not_implemented"))

        def error_not_registered(self, ctx: Context, arg: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("error_not_registered"):
                self.lang_dict.add_with("en", "an unexpected error occurred, please report the error to @{}.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "um erro inesperado ocorreu, por favor informe o erro para @{}."
                )
            return response.format_response(self._untangle_str(ctx, "error_not_registered"), arg)

        def command_not_pipeble(self, ctx: Context, arg: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("command_not_pipeble"):
                self.lang_dict.add_with("en", "command {} can't be used with the pipe.")
                self.lang_dict.add_with(["pt_br", "pt"], "comando {} não pôde ser utilizado com pipe.")
            return response.format_response(self._untangle_str(ctx, "command_not_pipeble"), arg)

        def pipe_response_error(self, ctx: Context, arg: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("pipe_response_error"):
                self.lang_dict.add_with("en", "an error occurred while executing the previous command: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "ocorreu um erro ao executar o comando anterior: {}")
            return response.format_response(self._untangle_str(ctx, "pipe_response_error"), arg)

        def pipe_response(self, ctx: Context, arg: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("pipe_response"):
                self.lang_dict.add_with("en", "here is the response generated by the previous command: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "aqui está a resposta gerada pelo comando anterior: {}")
            return response.format_response(self._untangle_str(ctx, "pipe_response"), arg)

        def lottery_seed(self, ctx: Context, arg: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", 'something terrible happened, contact "{}" here on Twitch using whispers.'
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], 'algo horrível aconteceu, contate "@{}" aqui na twitch utilizando whispers.'
                )
            return response.format_response(self._untangle_str(ctx, self._cname), arg)

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
