# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TranslationBase
from bot.ext.translations.extras import TBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Nada(TBase):
        def __init__(self):
            super().__init__()

        def nada(self, ctx: Context, args: str, success: bool = True, handle: str = None) -> Response:
            response = Response(ctx=ctx, success=success, handle=handle, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "The command was executed successfully. {}")
                self.lang_dict.add_with(["pt_br", "pt"], "O comando foi executado com sucesso. {}")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        nada: Response = nada

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This command is used for testing.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando é usado para testes.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}nada (text)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}nada (text)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This command is used for testing.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando é usado para testes.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:  # NOQA
            return CommandExemples([])

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:  # NOQA
            return Admonitions([])

    Nada: Nada

    class Restart(TBase):
        def __init__(self):
            super().__init__()

        def unexpected_error(self, ctx: Context, exception: Exception, success: bool = False, handle: str = None):
            response = Response(ctx=ctx, success=success, handle=handle, response_list=None)
            with self.lang_dict.once("unexpected_error"):
                self.lang_dict.add_with("en", "There was an error restarting the bot: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Um erro aconteceu ao reiniciar o bot: {}")
            return response.format_response(self._untangle_str(ctx, "unexpected_error"), exception)

        unexpected_error: Response = unexpected_error

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("helper"):
                self.lang_dict.add_with("en", "Restarts the bot.")
                self.lang_dict.add_with(["pt_br", "pt"], "Reinicia o bot.")
            return self._untangle_str(ctx, "helper")

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once("usage"):
                self.lang_dict.add_with("en", "To use: {}restart")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}restart")
            return self._untangle_str(ctx, "usage").format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("description"):
                self.lang_dict.add_with("en", "Restarts the bot.")
                self.lang_dict.add_with(["pt_br", "pt"], "Reinicia o bot.")
            return self._untangle_str(ctx, "description")

    Restart: Restart

    class Reload(TBase):
        def __init__(self):
            super().__init__()

        def commands_reloaded(self, ctx: Context):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "The commands were successfully reloaded.")
                self.lang_dict.add_with(["pt_br", "pt"], "Os comandos foram recarregados com sucesso.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        commands_reloaded: Response = commands_reloaded

        def command_not_found(self, ctx: Context, command: str):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("command_not_found"):
                self.lang_dict.add_with("en", "Command with name {} not found.")
                self.lang_dict.add_with(["pt_br", "pt"], "Comando com nome {} não encontrado.")
            return response.format_response(self._untangle_str(ctx, "command_not_found"), command)

        command_not_found: Response = command_not_found

        def command_reloaded(self, ctx: Context, command: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("command_reloaded"):
                self.lang_dict.add_with("en", "Command {} successfully reloaded.")
                self.lang_dict.add_with(["pt_br", "pt"], "Comando {} recarregado com sucesso.")
            return response.format_response(self._untangle_str(ctx, "command_reloaded"), command)

        command_reloaded: Response = command_reloaded

        def command_reloaded_error(self, ctx: Context, attr: str, exception: Exception):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("command_reloaded_error"):
                self.lang_dict.add_with("en", "Command {} had an error while reloading: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "O comando {} teve um erro ao recarregar: {}")
            return response.format_response(self._untangle_str(ctx, "command_reloaded_error"), attr, exception)

        command_reloaded_error: Response = command_reloaded_error

        def module_reloaded(self, ctx: Context, attr: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("module_reloaded"):
                self.lang_dict.add_with("en", "{} were successfully reloaded.")
                self.lang_dict.add_with(["pt_br", "pt"], "{} foram recarregadas com sucesso.")
            return response.format_response(self._untangle_str(ctx, "module_reloaded"), attr)

        module_reloaded: Response = module_reloaded

        def module_reloaded_error(self, ctx: Context, attr: str, exception: Exception):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("module_reloaded_error"):
                self.lang_dict.add_with("en", "{} had an error while reloading: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{} tiveram um erro ao recarregar: {}")
            return response.format_response(self._untangle_str(ctx, "module_reloaded_error"), attr, exception)

        module_reloaded_error: Response = module_reloaded_error

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("helper"):
                self.lang_dict.add_with("en", "Reloads the commands using all or command name.")
                self.lang_dict.add_with(["pt_br", "pt"], "Recarregar os comandos usando all ou nome do comando.")
            return self._untangle_str(ctx, "helper")

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once("usage"):
                self.lang_dict.add_with("en", f"How to use: {prefix}reload (all) or (command_name)")
                self.lang_dict.add_with(["pt_br", "pt"], f"Como usar: {prefix}reload (all) ou (command_name)")
            return self._untangle_str(ctx, "usage")

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("description"):
                self.lang_dict.add_with(
                    "en",
                    "This command is used to reload all bot commands. "
                    "If any have been updated and don't require a full restart.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando é usado para recarregar todos os comandos bot. "
                    "Se algum tiver sido atualizado e não precisar de um reinício completo.",
                )
            return self._untangle_str(ctx, "description")

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once("commands"):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "commands", "response": "the commands have been successfully reloaded."},
                            {"args": "emotes", "response": "Emotes were successfully reloaded."},
                            {"args": "translations", "response": "TranslationManager were successfully reloaded."},
                            {"args": "tokens_handler", "response": "TokensHandler were successfully reloaded."},
                            {"args": "channel_handler", "response": "ChannelHandler were successfully reloaded."},
                            {"args": "lifecycle_handler", "response": "LifecycleHandler were successfully reloaded."},
                            {"args": "command_handler", "response": "CommandHandler were successfully reloaded."},
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"args": "commands", "response": "Os comandos foram recarregados com sucesso."},
                            {"args": "emotes", "response": "Emotes foram recarregadas com sucesso."},
                            {"args": "translations", "response": "TranslationManager foram recarregadas com sucesso."},
                            {"args": "tokens_handler", "response": "TokensHandler foram recarregadas com sucesso."},
                            {"args": "channel_handler", "response": "ChannelHandler foram recarregadas com sucesso."},
                            {
                                "args": "lifecycle_handler",
                                "response": "LifecycleHandler foram recarregadas com sucesso.",
                            },
                            {"args": "command_handler", "response": "CommandHandler foram recarregadas com sucesso."},
                        ]
                    ),
                )
            return self._untangle_commands(ctx, "commands")

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once("admonitions"):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, "admonitions")

    Reload: Reload
