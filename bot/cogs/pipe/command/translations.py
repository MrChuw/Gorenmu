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

    class Pipe(TBase):
        def __init__(self):
            super().__init__()

        def pipe(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Pipe is not really a command. For more information, visit this link: {}",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Pipe não é realmente um comando. Para mais informações, visite este link: {}",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Pipe is not really a command. For more information, visit the website.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Pipe não é realmente um comando. Para mais informações, visite o site.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Pipe is not really a command. For more information, visit the website.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Pipe não é realmente um comando. Para mais informações, visite o site.",
                )
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        # TODO: fix this site description.
        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Pipe is not really a command. For more information, visit the website.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Pipe não é realmente um comando. Para mais informações, visite o site.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "{}example_command_1 <command options> | example_command_2"},
                            {
                                "args": "{}example_command_1 <command options> | example_command_2 "
                                "<command 2 options> {output from command 1} <remaining command 2 options>"
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"args": "{}comando_exemplo_1 <command options> | comando_exemplo_2"},
                            {
                                "args": "{}comando_exemplo_1 <command options> | comando_exemplo_2 "
                                "<opções para o comando 2> {output do comando 1 } "
                                "<opções restantes do comando 2>"
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
                                "type": "warning",
                                "title": "Cooldown!",
                                "position": "top",
                                "message": "The cooldown for the pipe will be the same as the cooldown of the "
                                "commands used.",
                            },
                            {
                                "type": "info",
                                "title": "Pipe",
                                "position": "bottom",
                                "message": "The Pipe is represented by the character '|' (vertical bar), and it "
                                "is used to forward the output of one command to another.",
                            },
                            {
                                "type": "info",
                                "title": "How pipe works:",
                                "position": "bottom",
                                "message": "## The bot's step-by-step will be:  \\n"
                                "- Execute `example_command_1` with `<command options>` if any.  \\n"
                                "- Then it will execute `example_command_2` with the response from "
                                "`example_command_1` added as an argument.  \\n"
                                "- If you use `{output}`, it will place the response from "
                                "`example_command_1` in the specified position.\n",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "type": "warning",
                                "title": "Cooldown!",
                                "position": "top",
                                "message": "O cooldown para o pipe será o mesmo que o cooldown dos comandos usados.",
                            },
                            {
                                "title": "Pipe",
                                "position": "bottom",
                                "type": "info",
                                "message": "O Pipe é representado pelo caractere '|' (barra vertical), e é usado "
                                "para encaminhar a saída de um comando para outro.",
                            },
                            {
                                "type": "info",
                                "title": "Como o pipe funciona:",
                                "message": "## O passo-a-passo do bot será:  \\n"
                                "- Executar `example_command_1` com `<opções de comando>` se houver.  \\n"
                                "- Em seguida, ele executará `example_command_2` com a resposta de "
                                "`example_command_1` adicionada como argumento.  \\n"
                                "- Se você usar `{output}`, ele colocará a resposta de `example_command_1` "
                                "na posição especificada.\n",
                                "position": "bottom",
                            },
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Pipe: Pipe
