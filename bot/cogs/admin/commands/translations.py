from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot, __file__)
        self.populate_subclasses(parent=self)

    class Nada(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Nada"

        def nada(self, args: str, success: bool = True) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=success, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Nada: Nada

    class Restart(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Restart"

        def unexpected_error(self, exception: Exception) -> Response:
            text = self.get_text(self._cname, exception=str(exception))
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Restart: Restart

    class Reload(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Reload"

        def commands_reloaded(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def command_not_found(self, command: str) -> Response:
            text = self.get_text(self._cname, command=command)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def command_reloaded(self, command: str) -> Response:
            text = self.get_text(self._cname, command=command)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def command_reloaded_error(self, attr: str, exception: Exception) -> Response:
            text = self.get_text(self._cname, attr=attr, exception=str(exception))
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def module_reloaded(self, attr: str) -> Response:
            text = self.get_text(self._cname, attr=attr)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def module_reloaded_error(self, attr: str, exception: Exception) -> Response:
            text = self.get_text(self._cname, attr=attr, exception=str(exception))
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {"args": self.get_text("cmd_ex1_args"), "response": self.get_text("cmd_ex1_res")},
                    {"args": self.get_text("cmd_ex2_args"), "response": self.get_text("cmd_ex2_res")},
                    {"args": self.get_text("cmd_ex3_args"), "response": self.get_text("cmd_ex3_res")},
                ]
            )

    Reload: Reload
