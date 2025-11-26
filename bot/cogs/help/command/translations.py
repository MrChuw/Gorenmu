from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Help(TBase):
        def __init__(self):
            super().__init__()

        def help(self, ctx: Context, prefix, name, helper, cooldown, url, alias) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{}{}: {} - Cooldown: {} {} - Aliases: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{}{}: {} - Cooldown: {} {} - Aliases: {}")
            return response.format_response(
                self._untangle_str(ctx, self._cname),
                prefix,
                name,
                helper,
                cooldown,
                url,
                alias,
            )

        def command_site(self, ctx: Context, url) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Site in construction, here is the list of commands: {}")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Site em construção, aqui está a lista de comandos: {}",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), url)

        def suggested_command(self, ctx: Context, content, suggested) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'I dont have command with name "{}", maybe you meant "{}".')
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    'Não tenho um comando com o nome "{}", talvez você quis dizer "{}".',
                )
            return response.format_response(self._untangle_str(ctx, self._cname), content, suggested)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Command to get information about other commands.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Comando para obter informações sobre outros comandos.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}help (command name)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}help (nome do comando)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command returns detailed information about another command, including its usage, "
                    "cooldown time, and aliases. If no input is given, it returns a general "
                    "site link with command listings.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando retorna informações detalhadas sobre outro comando, incluindo como usá-lo, "
                    "tempo de espera (cooldown) e apelidos (aliases). Se nenhum nome for fornecido, ele retorna o "
                    "site com a lista de comandos.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "When the command exists and has info.",
                                "args": "ping",
                                "response": "{}ping: Command to check if the bot is alive. - "
                                "Cooldown: 5s https://bot.mrchuw.com.br/commands/ping - Aliases: pong",
                            },
                            {
                                "prefix": "When the command doesn't exist but one is suggested.",
                                "args": "pign",
                                "response": 'I dont have command with name "pign", maybe you meant "ping".',
                            },
                            {
                                "prefix": "When no argument is passed.",
                                "args": "",
                                "response": "Site in construction, here is the list of commands: "
                                "https://bot.mrchuw.com.br",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "Quando o comando existe e há informações.",
                                "args": "ping",
                                "response": "{}ping: Comando para verificar se o bot está ativo. - "
                                "Cooldown: 5s https://bot.mrchuw.com.br/commands/ping - Apelidos: pong",
                            },
                            {
                                "prefix": "Quando o comando não existe mas há uma sugestão.",
                                "args": "pign",
                                "response": 'Não encontrei um comando chamado "pign", talvez você quis dizer "ping".',
                            },
                            {
                                "prefix": "Quando nenhum argumento é passado.",
                                "args": "",
                                "response": "Site em construção, aqui está a lista de comandos: "
                                "https://bot.mrchuw.com.br",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    Admonitions(
                        [
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "Command Suggestions",
                                "message": "If a command isn't found, the bot may suggest the closest match.",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "Aliases and Cooldowns",
                                "message": "The help command will also list any aliases and cooldowns "
                                "associated with the command.",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "Sugestões de Comando",
                                "message": "Se um comando não for encontrado, o bot pode sugerir o mais próximo.",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "Aliases e Cooldown",
                                "message": "O comando de ajuda também listará os apelidos e o "
                                "tempo de espera de cada comando.",
                            },
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Help: Help
