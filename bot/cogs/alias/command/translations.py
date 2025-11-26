from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context
# TODO: The template generator for Alias


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Table(TBase):
        def __init__(self):
            super().__init__()

        def alias_table_headers(self, ctx: Context) -> list[str]:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", ["Alias Name", "Description", "Invokes", "Arguments", "Links to", "Updated", "Created"]
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    ["Nome de Alias", "Descrição", "Invocação", "Argumentos", "Links para", "Atualizado", "Criado"],
                )
            return self._untangle_any(ctx, self._cname)

        alias_table_headers: Callable[[Context], list[str]] = alias_table_headers

        def alias_table_replaces(self, ctx: Context) -> list[str]:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", ["No description", "No arguments", "None"])
                self.lang_dict.add_with(["pt_br", "pt"], ["Nenhuma descrição", "Sem argumentos", "Nada"])
            return self._untangle_any(ctx, self._cname)

        alias_table_replaces: Callable[[Context], list[str]] = alias_table_replaces

        def alias_table_name(self, ctx: Context, name: str) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{} aliases")
            return self._untangle_str(ctx, self._cname).format(name)

        alias_table_name: Callable[[Context, str], list[str]] = alias_table_name

    class Alias(TBase):
        def __init__(self):
            super().__init__()

        def dont_have_alias(self, ctx: Context, name: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'You don\'t have the "{}" alias!')
                self.lang_dict.add_with(["pt_br", "pt"], 'Você não tem o alias "{}"!')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def alias_invalid_name(self, ctx: Context):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "Your alias name is not valid! Your alias should only contain letters, "
                    "numbers and be 2-30 characters long.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Seu nome de alias não é válido! Seu alias deve conter apenas letras, "
                    "números e ter entre 2-30 caracteres de comprimento.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname))

        def user_has_no_alias(self, ctx: Context, name: str):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "User {} has no registered aliases.")
                self.lang_dict.add_with(["pt_br", "pt"], "O usuário {} não possui aliases registrados.")
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("helper"):
                self.lang_dict.add_with("en", "Command used to manage aliases.")
                self.lang_dict.add_with(["pt_br", "pt"], "Comando usado para gerir aliases.")
            return self._untangle_str(ctx, "helper")

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once("usage"):
                self.lang_dict.add_with(
                    "en", "To use: {}alias add|check|copy|describe|edit|link|remove|rename (options)"
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Para usar: {}alias add|check|copy|describe|edit|link|remove|rename (opções)"
                )
            return self._untangle_str(ctx, "usage")

    Alias: Alias

    class Add(TBase):
        def __init__(self):
            super().__init__()

        def no_command_to_add(self, ctx: Context, prefix: str):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "You didn't send a command! Usage: {}alias add (name) (command) (…arguments)"
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Você não enviou um comando! Use: {}alias add (nome) (comando) (…argumentos)"
                )
            return response.format_response(self._untangle_str(ctx, self._cname), prefix)

        def alias_name_conflict(self, ctx: Context, name: str):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    'Cannot add alias "{}" - you already have one! '
                    'You can either "edit" its definition, "rename" it or "remove" it.',
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    'Não é possível adicionar o alias "{}" - você já possui um! '
                    "Você pode “editar” sua definição, “renomear” ou “removê-la”.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def alias_created(self, ctx: Context, name: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'Your alias "{}" has been created successfully.')
                self.lang_dict.add_with(["pt_br", "pt"], 'Seu alias "{}" foi criado com sucesso.')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def command_dont_exist(self, ctx: Context, name: str):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'Cannot create alias! The command "{}" does not exist.')
                self.lang_dict.add_with(["pt_br", "pt"], 'Não é possível criar um alias! O comando "{}" não existe.')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to add an alias.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para adicionar um alias.")
            return self._untangle_str(ctx, self._cname)

        # region Hide.

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}alias add (name) (command) (…arguments)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}alias add (nome) (comando) (…argumentos)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to add aliases.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para adicionar um alias.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "## How to create an alias:\n\n- The following example uses "
                                "[pipe](pipe.md) to pass the response of one command to another.",
                                "args": "add cool_name choice 1234 123456 | count",
                                "response": 'your alias "cool_name" has been successfully created.',
                                "suffix": "In the example above, we created an alias named `cool_name`. "
                                'The alias will invoke the `choice` command with the arguments "1234" and "123456", '
                                "and the result from `choice` will be sent to the `count` command.,",
                            },
                            {
                                "prefix": "## How to use the alias:",
                                "args": "{prefix}{prefix}cool_name",
                                "response": "There are a total of 4 characters. Among them, 0 are punctuation marks, "
                                "0 are uppercase letters, and 0 are special characters.",
                                "suffix": "To use the alias, just use `{prefix}{prefix}` followed by the alias name "
                                "(`{prefix}` is the default bot prefix; if the chat prefix is different, "
                                "just repeat it twice and then the alias name).",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "## Como criar um alias:\n - O exemplo a seguir usa [pipe](pipe.md) "
                                "para passar a resposta de um comando para outro.",
                                "args": "add cool_name choice 1234 123456 | count",
                                "response": 'seu alias "cool_name" foi criado com sucesso.',
                                "suffix": "No exemplo acima, criamos um alias chamado `cool_name`. "
                                'O alias invocará o comando `choice` com os argumentos "1234" e '
                                '\\"123456\\", e o resultado de `choice` será enviado para o comando `count`.',
                            },
                            {
                                "prefix": "## Para usar o alias:",
                                "args": "{prefix}{prefix}cool_name",
                                "response": "há um total de 4 caracteres. Entre eles, 0 são "
                                "marcas de pontuação, 0 são letras maiúsculas, e 0 são caracteres especiais.",
                                "suffix": "Para usar o alias, basta usar `{prefix}{prefix}` "
                                "seguido pelo nome do alias ({prefix} é o prefixo padrão do bot, se o "
                                "prefixo do chat é diferente, basta repeti-lo 2 (dois) vezes e então o nome do alias).",
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
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Restrictions for alias names!",
                                "message": "- Must be between 2 and 30 characters long.\n"
                                "- Can contain letters, numbers, dashes (-), underscores (_), and a "
                                "wide range of Unicode characters (©), including emojis (🔥).\n",
                            },
                            {
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Cooldown for created aliases!",
                                "message": "When creating an alias, the alias cooldown will be the cooldown of "
                                "the commands used in the alias. Therefore, if one command can be used 1x every "
                                "5 seconds and another 3x every 10 seconds, the alias cooldown will be 1x every "
                                "5 seconds.",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Restrições para nomes de aliases!",
                                "message": "- Deve ter entre 2 e 30 caracteres. - "
                                "Pode conter letras, números, hífens (-), underscores (_), e uma ampla gama "
                                "de caracteres Unicode (©), incluindo emojis (🔥).",
                            },
                            {
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Cooldown para aliases criados!",
                                "message": "Ao criar um alias, o tempo de espera (cooldown) do alias será o maior "
                                "tempo de espera entre os comandos utilizados no alias. Portanto, se um comando "
                                "pode ser usado 1x a cada 5 segundos e outro 3x a cada 10 segundos, o tempo de "
                                "espera do alias será 1x a cada 5 segundos.",
                            },
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Add: Add

    class Check(TBase):
        def __init__(self):
            super().__init__()

        def user_alias_list(self, ctx: Context, names: str, url: str):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "List of your aliases: {} | Detailed list: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Lista dos seus aliases: {} | Lista detalhada: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), names, url)

        def no_alias_found(self, ctx: Context, success: bool = False, handle: str | None = None, *args):
            response = Response(ctx=ctx, success=success, handle=handle, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Could not find {} in {} aliases or any of your aliases!")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Não foi possível encontrar {} em {} aliases ou em qualquer um dos seus aliases!"
                )
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def list_of_alias_of(self, ctx: Context, mention, url):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "List of {} aliases: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Lista de aliases de {}: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), mention, url)

        def list_of_special_case(self, ctx: Context, name: str, url1: str, url2: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'Special case!\n Your alias "{0}": {1}\n List of {0}\'s aliases: {2}')
                self.lang_dict.add_with(
                    ["pt_br", "pt"], 'Caso especial!\nSeu alias "{0}": {1}\nLista dos aliases de {0}: {2}'
                )
            return response.format_response(self._untangle_str(ctx, self._cname), name, url1, url2)

        def alias_not_found(self, ctx: Context, mention: str, alias: str):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", '{} don\'t have the "{}" alias!')
                self.lang_dict.add_with(["pt_br", "pt"], '{} não tem o alias "{}"!')
            return response.format_response(self._untangle_str(ctx, self._cname), mention, alias)

        def alias_deleted(self, ctx: Context, alias: str):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "{} alias is a link to a different alias, but the original has been deleted."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "{} alias é um link para um alias diferente, mas o original foi excluído."
                )
            return response.format_response(self._untangle_str(ctx, self._cname), alias)

        def normal_message(self, ctx: Context, name: str, invocation: str, url: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{} || Invoke: {} || Link: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{} || Invoca: {} || Link: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), name, invocation, url)

        def appendix_message(self, ctx: Context, parent: str, original: str, invocation: str, url: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", 'This alias is a link to "{}" made by {}. The alias has the arguments: {} || Link: {} '
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    'Este alias é um link para "{}" criado por {}. O alias tem os argumentos: {} || Link: {} ',
                )
            return response.format_response(self._untangle_str(ctx, self._cname), parent, original, invocation, url)

        def appendix(self, ctx: Context):
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'This alias is a link to "{}" made by {}.')
                self.lang_dict.add_with(["pt_br", "pt"], 'Este alias é um link para "{}" feito por {}.')
            return self._untangle_str(ctx, self._cname).format()

        def message(self, ctx: Context):
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", '{} alias "{}" have the arguments: {} {}')
                self.lang_dict.add_with(["pt_br", "pt"], '{} alias "{}" tem os argumentos: {} {}')
            return self._untangle_str(ctx, self._cname).format()

        # region Hide.

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to check infos for an alias.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Este subcomando é usado para verificar informações de um alias."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}alias check cool_name")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}alias check cool_name")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to check infos for an aliases.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Este subcomando é usado para verificar informações de um alias."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "## How to check an alias:",
                                "args": "check cool_name",
                                "response": 'User, the alias "cool_name" has the arguments: '
                                "choice 1234 123456 | count || Link: (URL)",
                                "suffix": "",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "## Como verificar um alias:",
                                "args": "check cool_name",
                                "response": 'Usuário, o alias "cool_name" tem os argumentos: '
                                "choice 1234 123456 | count || Link: (URL)",
                                "suffix": "",
                            }
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Check: Check

    class Copy(TBase):
        def __init__(self):
            super().__init__()

        def alias_not_provided(self, ctx: Context):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "No target alias provided!")
                self.lang_dict.add_with(["pt_br", "pt"], "Nenhum alias de destino fornecido!")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def target_alias_invalid_name(self, ctx: Context, *args):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "The copied alias's name is not valid and therefore can't be copied!")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "O nome do alias copiado não é válido e portanto não pode ser copiado!"
                )
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def no_alias_found(self, ctx: Context, alias: str, name: str):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "I couldn't find {} in user {}!")
                self.lang_dict.add_with(["pt_br", "pt"], "Não consegui encontrar {} no usuário {}!")
            return response.format_response(self._untangle_str(ctx, self._cname), alias, name)

        def link_to_a_link(self, ctx: Context, prefix: str, user: str, target: str):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You cannot copy links to other aliases. Instead, use {}alias copy {} {}")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Você não pode copiar links para outros aliases. Em vez disso, use {}alias copy {} {}",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), prefix, user, target)

        def copy_success(self, ctx: Context, name: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'Alias "{}" copied successfully.')
                self.lang_dict.add_with(["pt_br", "pt"], 'Alias "{}" copiado com sucesso.')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def copy_with_name_of(self, ctx: Context, target: str, name: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'Alias "{}" copied successfully. With the name "{}".')
                self.lang_dict.add_with(["pt_br", "pt"], 'Alias "{}" copiado com sucesso. Com o nome "{}".')
            return response.format_response(self._untangle_str(ctx, self._cname), target, name)

        # region Hide.

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to copy an alias.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para copiar um alias.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}alias copy (user) (alias) (…arguments)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}alias copy (usuário) (alias) (…argumentos)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to copy an alias.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para copiar um alias.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "## How to copy an alias:",
                                "args": "copy <username> cool_name",
                                "response": 'User, alias "cool_name" copied successfully.',
                                "suffix": "To copy an alias, you only need the username and the alias name.",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "## Como copiar um alias:",
                                "args": "copy <usuário> cool_name",
                                "response": 'Usuário, alias "cool_name" copiado com sucesso.',
                                "suffix": "Para copiar um alias, você só precisa do nome de "
                                "usuário e do nome do alias.",
                            }
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Copy: Copy

    class Describe(TBase):
        def __init__(self):
            super().__init__()

        def no_args_to_parse(self, ctx: Context, prefix) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "You didn't provide a alias or description! Use: {}alias describe (name) (…description)"
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Você não forneceu um alias ou uma descrição! Use: {}alias describe (nome) (…descrição)",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), prefix)

        def description_updated(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'The description of alias "{}" has been updated successfully.')
                self.lang_dict.add_with(["pt_br", "pt"], 'A descrição do alias "{}" foi atualizada com sucesso.')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def description_reverted(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'The description of alias "{}" has been reset successfully.')
                self.lang_dict.add_with(["pt_br", "pt"], 'A descrição do alias "{}" foi removida com sucesso.')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to check infos for an alias.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Este subcomando é usado para adicionar ou verificar a descrição de um alias."
                )
            return self._untangle_str(ctx, self._cname)

        # region Hide.

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}alias description cool_name (new description)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}alias description cool_name (nova descrição)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to check info for an aliases.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Este subcomando é usado para adicionar ou verificar a descrição de um alias."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "## How to add a description to an alias:",
                                "args": "description cool_name (new description)",
                                "response": 'User, the description for alias "cool_name" '
                                "has been successfully updated.",
                                "suffix": "",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "## Como adicionar uma descrição a um alias:",
                                "args": "description cool_name (nova descrição)",
                                "response": 'Usuário, a descrição para o alias "cool_name" foi atualizada com sucesso.',
                                "suffix": "",
                            }
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Describe: Describe

    class Edit(TBase):
        def __init__(self):
            super().__init__()

        def no_args_provided(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "No alias or command name provided!")
                self.lang_dict.add_with(["pt_br", "pt"], "Nenhum alias ou nome de comando fornecido!")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def edit_link(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You cannot edit links to other aliases!")
                self.lang_dict.add_with(["pt_br", "pt"], "Você não pode editar links para outros aliases!")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def edit_success(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'Your alias "{}" has been successfully edited.')
                self.lang_dict.add_with(["pt_br", "pt"], 'Seu alias "{}" foi editado com sucesso.')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def command_dont_exist(self, ctx: Context, command) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'Cannot edit alias! The command "{}" does not exist.')
                self.lang_dict.add_with(["pt_br", "pt"], 'Não é possível editar o alias! O comando "{}" não existe.')
            return response.format_response(self._untangle_str(ctx, self._cname), command)

        # region Hide.

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to edit the command and arguments for an alias.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Este subcomando é usado para editar o comando e os argumentos de um alias."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}alias edit (alias) (command) (…arguments)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}alias edit (alias) (comando) (…argumentos)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to edit the command and arguments for an alias.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Este subcomando é usado para editar o comando e os argumentos de um alias."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "## How to edit an alias:",
                                "args": "edit cool_name count bla bla bla bla",
                                "response": 'Your alias "cool_name" has been successfully edited.',
                                "suffix": "",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "## Como editar um alias:",
                                "args": "edit cool_name count bla bla bla bla",
                                "response": 'Usuário, o alias "cool_name" foi editado com sucesso.',
                                "suffix": "",
                            }
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
                                "admonition_type": "warning",
                                "position": "bottom",
                                "title": "Linked alias.",
                                "message": "- Because linked alias are only a pointer to other "
                                "user alias, editing then is impossible.",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "position": "bottom",
                                "title": "Alias vinculado.",
                                "message": "- Como aliases vinculados são apenas um ponteiro para o "
                                "alias de outro usuário, não é possível editá-los.",
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Edit: Edit

    class Link(TBase):
        def __init__(self):
            super().__init__()

        def link_no_args(self, ctx: Context, prefix) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "You didn't provide a user or alias name! Use: {}alias link (user) (alias name)"
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Você não forneceu um nome de usuário ou alias! Use: {}alias link (usuário) (nome do alias)",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), prefix)

        def alias_name_already_exists(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Cannot link a new alias - you already have an alias named: {}!")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Não é possível vincular um novo alias - você já possui um alias nomeado: {}!"
                )
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def user_dont_has_alias(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'The provided user does not have the alias "{}"!')
                self.lang_dict.add_with(["pt_br", "pt"], 'O usuário fornecido não possui o alias "{}"!')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def link_to_with_invalid_name(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", 'The original alias has an invalid name "{}"! Please provide a custom name.'
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    'O alias original possui um nome inválido "{}"! Por favor, forneça um nome customizado.',
                )
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def link_custom_name_invalid(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'The custom name "{}" is not valid. Please provide a valid name.')
                self.lang_dict.add_with(
                    ["pt_br", "pt"], 'O nome customizado "{}" não é válido. Por favor, forneça um nome válido.'
                )
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def link_to_link(self, ctx: Context, target_name: str, user_name: str, alias_name: str) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "You tried to create a link from a linked alias (alias {} by {}), "
                    "so I used the original as your template{} When the original changes, yours will too.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Você tentou criar um link a partir de um alias link (alias {} por {}), "
                    "então usei o original como modelo{} Quando o original mudar, o seu também mudará.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), target_name, user_name, alias_name)

        def link_success(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Alias successfully linked{} When the original changes, yours will too.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Alias vinculado com sucesso{} Quando o original for alterado, o seu também será."
                )
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def link_name_string(self, ctx: Context, name) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", ', with a custom name of "{}".')
                self.lang_dict.add_with(["pt_br", "pt"], ', com um nome personalizado de "{}".')
            return self._untangle_str(ctx, self._cname).format(name)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to create link for an alias.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para criar um link para um alias.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}alias link (user) cool_name")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}alias link (usuário) cool_name")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to create link for an alias.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para criar um link para um alias.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "## How to link an alias:",
                                "args": "link (user) cool_name",
                                "response": "User, alias linked successfully. "
                                "When the original changes, yours will also change.",
                                "suffix": "",
                            },
                            {
                                "prefix": "## It is also possible to create a link and change the alias name.",
                                "args": "link (user) cool_name new_cool_name",
                                "response": 'User, alias linked successfully, with a custom name "new_cool_name". '
                                "When the original changes, yours will also change.",
                                "suffix": "",
                            },
                            {
                                "prefix": "## And if it is a link to a link:",
                                "args": "link (user) cool_name",
                                "response": "User, you attempted to create a link from an already linked "
                                "alias (alias cool_name by <user>), so I used the original as your model. "
                                "When the original changes, yours will also change.",
                                "suffix": "",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "## Como linkar um alias:",
                                "args": "link (usuário) cool_name",
                                "response": "Usuário, alias vinculado com sucesso. Quando o original mudar, "
                                "o seu também mudará.",
                                "suffix": "",
                            },
                            {
                                "prefix": "## Também é possível criar um link e alterar o nome do alias:",
                                "args": "link (usuário) cool_name new_cool_name",
                                "response": "Usuário, alias vinculado com sucesso, com um nome personalizado "
                                '"new_cool_name". Quando o original mudar, o seu também mudará.',
                                "suffix": "",
                            },
                            {
                                "prefix": "## E se for um link para um link:",
                                "args": "link (usuário) cool_name",
                                "response": "Usuário, você tentou criar um link de um alias já vinculado "
                                "(alias cool_name de <usuário>), então eu usei o original como "
                                "seu modelo. Quando o original mudar, o seu também mudará.",
                                "suffix": "",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Link: Link

    class Remove(TBase):
        def __init__(self):
            super().__init__()

        def no_alias_name_provided(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "No alias name provided!")
                self.lang_dict.add_with(["pt_br", "pt"], "Nenhum nome de alias fornecido!")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def alias_removed(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'Your alias "{}" has been successfully removed.')
                self.lang_dict.add_with(["pt_br", "pt"], 'Seu alias "{}" foi removido com sucesso.')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to delete an alias.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para excluir um alias.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}alias remove (alias)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}alias remove (alias)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to delete an alias.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para excluir um alias.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "## To remove an alias:",
                                "args": "remove cool_name",
                                "response": 'User, your alias "cool_name" has been successfully removed.',
                                "suffix": "When deleting an alias, the links to this alias will continue "
                                "to exist and function.",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "## Para remover um alias:",
                                "args": "remove cool_name",
                                "response": 'Usuário, seu alias "cool_name" foi removido com sucesso.',
                                "suffix": "Ao excluir um alias, os links para este alias continuarão a "
                                "existir e funcionar normalmente.",
                            }
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Remove: Remove

    class Rename(TBase):
        def __init__(self):
            super().__init__()

        def no_name_provided(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You must provide both the current alias name and the new one!")
                self.lang_dict.add_with(["pt_br", "pt"], "Você deve fornecer o nome alias atual e o novo!")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def alias_already_exists(self, ctx: Context, name: str) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'You already have the "{}" alias!')
                self.lang_dict.add_with(["pt_br", "pt"], 'Você já tem o alias "{}"!')
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def alias_renamed(self, ctx: Context, old: str, new: str) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'Your alias "{}" has been successfully renamed to "{}".')
                self.lang_dict.add_with(["pt_br", "pt"], 'Seu alias "{}" foi renomeado com sucesso para "{}".')
            return response.format_response(self._untangle_str(ctx, self._cname), old, new)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to rename an alias.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para renomear um alias.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}alias rename cool_name new_cool_name")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}alias rename cool_name new_cool_name")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to rename an alias.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para renomear um alias.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "## To rename an alias:",
                                "args": "rename cool_name new_cool_name",
                                "response": 'User, your alias "cool_name" has been successfully renamed '
                                'to "new_cool_name".',
                                "suffix": "",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "## Para renomear um alias:",
                                "args": "rename cool_name new_cool_name",
                                "response": 'Usuário, seu alias "cool_name" foi renomeado '
                                'com sucesso para "new_cool_name".',
                                "suffix": "",
                            }
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Rename: Rename

    class Extras(TBase):
        def __init__(self):
            super().__init__()

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This section is about advanced alias usage.")
                self.lang_dict.add_with(["pt_br", "pt"], "Esta seção aborda o uso avançado de alias.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "## First, let's create an alias:",
                                "args": "add advanced_usage choice 1234 123456 | count {0}",
                                "response": 'User, your alias "advanced_usage" has been successfully created.',
                                "suffix": "",
                            },
                            {
                                "prefix": "## How to use this type of alias:",
                                "args": "{prefix}{prefix}advanced_usage text",
                                "response": "There are a total of 10 characters. Among them, 0 are punctuation marks, "
                                "0 are uppercase letters, and 0 are special characters.",
                                "suffix": "The normal response of the command would be: `There are a total of 4 "
                                "characters. etc` or `There are a total of 6 characters. etc`, as "
                                "`choice` would select between `1234` or `123456`, and then count would "
                                "return the number of characters.\n\nBut, due to the addition of `{0}` "
                                "after count, it will take the content of what was sent when invoking the "
                                "alias and replace `{0}`.\n\nSo the command passed to count it would be "
                                "something like: `text 1234`",
                            },
                            {
                                "prefix": "## An example showing all would be:",
                                "args": "add advanced_usage2 choice 1234 123456 | count {0} {channel} {output} "
                                "{user} {1+}",
                                "response": 'User, your alias "advanced_usage2" has been successfully created.',
                                "suffix": "",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "## Primeiro, vamos criar um alias:",
                                "args": "add advanced_usage choice 1234 123456 | count {0}",
                                "response": 'Usuário, seu alias "advanced_usage" foi criado com sucesso.',
                                "suffix": "",
                            },
                            {
                                "prefix": "## Como usar este tipo de alias:",
                                "args": "{prefix}{prefix}advanced_usage texto",
                                "response": "Há um total de 10 caracteres. Entre eles, 0 são pontuação, "
                                "0 são letras maiúsculas, e 0 são caracteres especiais.",
                                "suffix": "A resposta normal do comando seria algo como: `Há um total "
                                "de 4 caracteres...` ou `Há um total de 6 caracteres...`, "
                                "pois `choice` escolheria entre `1234` ou `123456` e então "
                                "`count` retornaria o número de caracteres.\n\nPorém, devido "
                                "à adição de `{0}` após `count`, ele irá pegar o conteúdo "
                                "enviado na chamada do alias e substituir no lugar de `{0}`."
                                "\n\nEntão o comando passado ao `count` seria algo como: "
                                "`texto 1234`.",
                            },
                            {
                                "prefix": "## Um exemplo mais completo seria:",
                                "args": "add advanced_usage2 choice 1234 123456 | count {0} {channel} "
                                "{output} {user} {1+}",
                                "response": 'Usuário, seu alias "advanced_usage2" foi criado com sucesso.',
                                "suffix": "",
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
                                "title": "The bot's step-by-step process will be:",
                                "message": " - Replace `{0}` with `something_here`.\n - Replace "
                                "`{1+}` with `and in the end`.\n - Replace `{channel}` "
                                "with the channel to which the message was sent, for "
                                "example, `gorenmu`.\n - Replace `{user}` with your "
                                "username, for example, `xXNickOriginalXx`.\n - The full "
                                "command would be `choice 1234 123456 | count something_"
                                "here gorenmu {output} xXNickOriginalXx` which would be "
                                "processed by the pipe handler.\n",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "The pipe handle, will do:",
                                "message": " - Process the first part: `choice 1234 123456` "
                                "(as an example, let's say choice selected `1234`).\n "
                                "- Process the second part: `count something_here gorenmu "
                                "{output} xXNickOriginalXx and in the end`; when processing "
                                "the second part, it will replace `{output}` with `1234`.\n "
                                "- Then, the arguments that will be sent to count will be "
                                "`something_here gorenmu 1234 xXNickOriginalXx and in the "
                                "end.`\n - And the response will be `There are a total of "
                                "50 characters. Among them, 1 is punctuation, 4 are "
                                "uppercase letters, and 0 are special characters.`\n",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "Other options when creating the alias are:",
                                "message": " - `{output}`: it will place the output of the last command "
                                "at the `{output}` position.\n - `{channel}`: it will replace "
                                "with the name of the current channel.\n - `{user}`: it will "
                                "replace with your Twitch username.\n - `{0}`, `{1}`, `{2}` "
                                "etc., you can also use `{3+}`, which will take all text sent "
                                "when invoking the alias and replace.",
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
                                "title": "O passo a passo que o bot seguirá será:",
                                "message": "- Substituir `{0}` por `algo_aqui`.\n- Substituir `{1+}` por "
                                "`e no final`.\n- Substituir `{channel}` pelo nome do canal onde "
                                "o comando foi executado, por exemplo, `gorenmu`.\n- Substituir "
                                "`{user}` pelo seu nome de usuário, por exemplo, `xXNickOriginalXx`"
                                ".\n- O comando completo será `choice 1234 123456 | count "
                                "algo_aqui gorenmu {output} xXNickOriginalXx e no final`, que "
                                "será processado pelo pipe handler.",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "O manipulador de pipe fará:",
                                "message": "- Processar a primeira parte: `choice 1234 123456` (por exemplo, "
                                "suponha que escolha selecionou `1234`).\n- Processar a segunda "
                                "parte: `count algo_aqui gorenmu {output} xXNickOriginalXx e no "
                                "final`. Ao processar, `{output}` será substituído por `1234`."
                                "\n- Assim, os argumentos enviados para `count` serão `algo_aqui "
                                "gorenmu 1234 xXNickOriginalXx e no final`.\n- E a resposta será: "
                                "`Há um total de 50 caracteres. Entre eles, 1 é pontuação, 4 são "
                                "letras maiúsculas, e 0 são caracteres especiais.`",
                            },
                            {
                                "admonition_type": "info",
                                "position": "bottom",
                                "title": "Outras opções ao criar alias são:",
                                "message": "- `{output}`: insere a saída do comando anterior na posição "
                                "`{output}`.\n- `{channel}`: substitui pelo nome do canal atual."
                                "\n- `{user}`: substitui pelo seu nome de usuário da Twitch.\n- "
                                "`{0}`, `{1}`, `{2}`... você também pode usar `{3+}`, que captura "
                                "todo o texto restante enviado na chamada do alias a partir da posição 3.",
                            },
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Extras: Extras


Templates = {
    "template_part1": "# {command_title}\n\n"
    "## This command can be used {rate} times in succession, "
    "with a cooldown of {per} per {cooldown_type}.\n\n",
    "template_part2": "{description}\n\n{aliases}\n\n",
    "template_part3": "## The way to use this command is:\n\n",
    "alias_template": "## All the alias available for {command_title} are:\n    - {aliases}\n\n",
    "command_template": "```text\n    user: {prefix}{command_name} {args}\n\n    bot: User, {response}\n```\n",
    "admonition_template": '!!! {type} "{title}"\n    \n        {message}\n\n    ',
    "bucket_type": {
        "default": "user",
        "channel": "all user per channel",
        "member": "user per channel",
        "user": "user independent of channel",
        "subscriber": "subscriber",
        "mod": "moderation",
    },
}

Templates2 = {
    "template_part1": "#{command_title}\n\n"
    "## Este comando pode ser usado {rate} vezes seguidas, "
    "com um tempo de espera de {per} por {cooldown_type}.\n\n",
    "template_part2": "{description}\n\n{aliases}\n\n",
    "template_part3": "## A maneira de usar este comando é:\n\n",
    "alias_template": "## Todos os alias disponíveis para {command_title} são:\n    - {aliases}\n\n",
    "command_template": "```text\n    usuário: {prefix}{command_name} {args}\n\n    bot: Usuário, {response}\n```\n",
    "admonition_template": '!!! {type} "{title}"\n    \n        {message}\n\n    ',
    "bucket_type": {
        "channel": "todos os usuários por canal",
        "member": "usuário por canal",
        "user": "usuário independente de canal",
        "mod": "moderação",
        "default": "usuário",
        "subscriber": "subscriber",
    },
}
