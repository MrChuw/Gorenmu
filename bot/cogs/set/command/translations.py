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

    class Set(TBase):
        def __init__(self):
            super().__init__()

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Main command to customize your user settings.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Comando principal para personalizar suas configurações de usuário."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Usage: {}set (subcommand) [arguments]")
                self.lang_dict.add_with(["pt_br", "pt"], "Uso: {}set (subcomando) [argumentos]")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Main command to customize your user settings.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Comando principal para personalizar suas configurações de usuário."
                )
            return self._untangle_str(ctx, self._cname)

        # endregion

    Set: Set

    class Mention(TBase):
        def __init__(self):
            super().__init__()

        def on_off_wrong_option(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", '{} its not a valid option, choose between "on" or "off"')
                self.lang_dict.add_with(["pt_br", "pt"], '{} não é uma opção válida, escolha entre "on" ou "off"')
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def mention_on(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You will start receiving pings from the bot on commands again.")
                self.lang_dict.add_with(["pt_br", "pt"], "Você voltará a receber menções do bot nos comandos.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def mention_off(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "Every time the bot says your nick it will place an invisible character to prevent ping."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Sempre que o bot disser seu nick, ele colocará um caractere invisível para evitar o ping.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Enable or disable bot mentions.")
                self.lang_dict.add_with(["pt_br", "pt"], "Ativar ou desativar menções do bot.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Usage: {}set mention <on/off>")
                self.lang_dict.add_with(["pt_br", "pt"], "Uso: {}set mention <on/off>")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "Allows you to enable or disable whether the bot will directly mention you when replying."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Permite ativar ou desativar se o bot irá mencionar você diretamente ao responder."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "Enable mentions:",
                                "args": "mention on",
                                "response": "You will start receiving pings from the bot on commands again.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Disable mentions:",
                                "args": "mention off",
                                "response": "Every time the bot says your nick it will place an invisible "
                                "character to prevent ping.",
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
                                "prefix": "Ativar menções:",
                                "args": "mention on",
                                "response": "Você voltará a receber menções do bot nos comandos.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Desativar menções:",
                                "args": "mention off",
                                "response": "Sempre que o bot disser seu nick, ele colocará um caractere "
                                "invisível para evitar o ping.",
                                "suffix": "",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Mention: Mention

    class City(TBase):
        def __init__(self):
            super().__init__()

        def city_added(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "City added successfully.")
                self.lang_dict.add_with(["pt_br", "pt"], "Cidade adicionada com sucesso.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def city_removed(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "City removed successfully.")
                self.lang_dict.add_with(["pt_br", "pt"], "Cidade removida com sucesso.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Set or remove your saved city.")
                self.lang_dict.add_with(["pt_br", "pt"], "Definir ou remover sua cidade salva.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Usage: {}set city (name or remove) [hidden:true]")
                self.lang_dict.add_with(["pt_br", "pt"], "Uso: {}set city (nome ou remove) [hidden:true]")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Saves a city name to your profile, optionally hidden from public view.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Salva o nome de uma cidade no seu perfil, opcionalmente oculto da visualização pública.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "Set a city:",
                                "args": "city Fortaleza, Ce",
                                "response": "City added successfully.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Set a city and hidden:",
                                "args": "city Fortaleza, Ce hidden:true",
                                "response": "City added successfully.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Set a location with lat and long and hidden:",
                                "args": "city -27.12 -109.35 hidden:true",
                                "response": "City added successfully.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Remove city:",
                                "args": "city remove",
                                "response": "City removed successfully.",
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
                                "prefix": "Definir cidade:",
                                "args": "city Fortaleza, Ce",
                                "response": "Cidade adicionada com sucesso.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Definir cidade e ocultar:",
                                "args": "city Fortaleza, Ce hidden:true",
                                "response": "Cidade adicionada com sucesso.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Definir a localização com lat e long e hidden:",
                                "args": "city -27.12 -109.35 hidden:true",
                                "response": "City added successfully.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Remover cidade:",
                                "args": "city remove",
                                "response": "Cidade removida com sucesso.",
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
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Hide it",
                                "message": "Use the `hidden` flag to hide your city from messages.",
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
                                "position": "top",
                                "title": "Ocultar",
                                "message": "Use a flag `hidden` para ocultar sua cidade nas mensagens.",
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    City: City

    class Nick(TBase):
        def __init__(self):
            super().__init__()

        def nick_too_large(self, ctx: Context, args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Nick must be max 32 characters long not {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "O apelido deve ter no máximo 32 caracteres, e não {}.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def nick_removed(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Nick removed successfully.")
                self.lang_dict.add_with(["pt_br", "pt"], "Apelido removido com sucesso.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def nick_changed(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Nick changed successfully.")
                self.lang_dict.add_with(["pt_br", "pt"], "Apelido alterado com sucesso.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Set or remove a custom nickname.")
                self.lang_dict.add_with(["pt_br", "pt"], "Definir ou remover um apelido personalizado.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Usage: {}set nick <nickname or remove>")
                self.lang_dict.add_with(["pt_br", "pt"], "Uso: {}set nick <apelido ou remove>")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Lets you define a nickname that the bot will use when addressing you.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Permite definir um apelido que o bot usará ao se referir a você."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "Set nickname:",
                                "args": "nick xXCoolNickNameXx",
                                "response": "Nick changed successfully.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Remove nickname:",
                                "args": "nick remove",
                                "response": "Nick removed successfully.",
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
                                "prefix": "Definir apelido:",
                                "args": "nick xXNickLegalXx",
                                "response": "Apelido alterado com sucesso.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Remover apelido:",
                                "args": "nick remove",
                                "response": "Apelido removido com sucesso.",
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
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Keep it short!",
                                "message": "Nick must be max 32 characters long.",
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
                                "position": "top",
                                "title": "Mantenha curto!",
                                "message": "O apelido deve ter no máximo 32 caracteres.",
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Nick: Nick

    class Color(TBase):
        def __init__(self):
            super().__init__()

        def color_removed(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Saved color removed successfully.")
                self.lang_dict.add_with(["pt_br", "pt"], "Cor salva removida com sucesso.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def color_changed(self, ctx: Context, color) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Saved color changed successfully.")
                self.lang_dict.add_with(["pt_br", "pt"], "Cor salva alterada com sucesso.")
            return response.format_response(self._untangle_str(ctx, self._cname), color)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Save or remove a custom color.")
                self.lang_dict.add_with(["pt_br", "pt"], "Salvar ou remover uma cor personalizada.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Usage: {}set color (#hex or remove)")
                self.lang_dict.add_with(["pt_br", "pt"], "Uso: {}set color (#hex ou remove)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Sets a custom hex color that may be used in future visualizations.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Define uma cor hexadecimal personalizada que pode ser usada em visualizações futuras.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "Set color:",
                                "args": "color #000000",
                                "response": "Saved color changed successfully.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Remove color:",
                                "args": "color remove",
                                "response": "Saved color removed successfully.",
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
                                "prefix": "Definir cor:",
                                "args": "color #000000",
                                "response": "Cor salva com sucesso.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Remover cor:",
                                "args": "color remove",
                                "response": "Cor salva removida com sucesso.",
                                "suffix": "",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Color: Color

    class Reminder(TBase):
        def __init__(self):
            super().__init__()

        def reminder_on(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Reminder successfully turned on.")
                self.lang_dict.add_with(["pt_br", "pt"], "Lembrete ativado com sucesso.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def reminder_off(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Reminder successfully turned off.")
                self.lang_dict.add_with(["pt_br", "pt"], "Lembrete desativado com sucesso.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Enable or disable reminders.")
                self.lang_dict.add_with(["pt_br", "pt"], "Ativar ou desativar lembretes.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Usage: {}set reminder (on/off)")
                self.lang_dict.add_with(["pt_br", "pt"], "Uso: {}set reminder (on/off)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "Toggles whether the system will send mark you in reminders form other people."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Alterna se o sistema irá marcar você em lembretes de outras pessoas."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "Enable reminders:",
                                "args": "reminder on",
                                "response": "Reminder successfully turned on.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Disable reminders:",
                                "args": "reminder off",
                                "response": "Reminder successfully turned off.",
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
                                "prefix": "Ativar lembretes:",
                                "args": "reminder on",
                                "response": "Lembrete ativado com sucesso.",
                                "suffix": "",
                            },
                            {
                                "prefix": "Desativar lembretes:",
                                "args": "reminder off",
                                "response": "Lembrete desativado com sucesso.",
                                "suffix": "",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Reminder: Reminder
