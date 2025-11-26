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

    class Color(TBase):
        def __init__(self):
            super().__init__()

        def color(self, ctx: Context, res1, res2) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{} {}")
            return response.format_response(self._untangle_str(ctx, self._cname), res1, res2)

        def no_user_hex(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "User not found or valid hex color provided.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Usuário não encontrado ou cor hexadecimal válida fornecida.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname))

        def user_not_color(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Provided user has no color defined on twitch.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "O usuário não tenha nenhuma cor definida no Twitch.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname))

        def user_color(self, ctx: Context, name=None, hex_value=None, hex_name=None) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "@{} color is: #{}. Named: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "@{} a cor é: #{}. Nome: {}")
            if not name or not hex_value or not hex_name:
                return self._untangle_str(ctx, self._cname)
            return self._untangle_str(ctx, self._cname).format(name, hex_value, hex_name)

        def hex_color(self, ctx: Context, hex_value=None, hex_name=None) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "#{} its Named: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "#{} Nome: {}")
            if not hex_value or not hex_name:
                return self._untangle_str(ctx, self._cname)
            return self._untangle_str(ctx, self._cname).format(hex_value, hex_name)

        def saved_color(self, ctx: Context, hex_value=None, hex_name=None) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "And has the following saved color: #{}. Named: {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "E tem a seguinte cor salva: #{}. Nome: {}.")
            if not hex_value or not hex_name:
                return self._untangle_str(ctx, self._cname)
            return self._untangle_str(ctx, self._cname).format(hex_value, hex_name)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Command to get Twitch or hex color info.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Comando para obter informações de cor do Twitch ou hexadecimal.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}color (username | hex)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}color (usuário | hex)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command returns information about a user's Twitch color, "
                    "a saved color, or a given hex color. It includes name lookup and color preview links.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando retorna informações sobre a cor do Twitch de um usuário, "
                    "uma cor salva ou uma cor hexadecimal informada. Inclui busca pelo nome da cor e "
                    "links de visualização.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "prefix": "If a valid twitch user is passed.",
                                "args": "mr_chuw",
                                "response": "@mr_chuw color is: #00FFFF. Named: Cyan / Aqua.",
                            },
                            {
                                "prefix": "If a valid hex code is passed.",
                                "args": "#FF4500",
                                "response": "#FF4500 is named: Vermilion.",
                            },
                            {
                                "prefix": "If the user has a saved color in the database.",
                                "args": "mr_chuw",
                                "response": "@mr_chuw color is: #00FFFF. Named: Cyan / Aqua. "
                                "And has the following saved color: #1E90FF. Named: Dodger Blue.",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "prefix": "Se um usuário válido do Twitch for informado.",
                                "args": "mr_chuw",
                                "response": "A cor de @mr_chuw é: #00FFFF. Nome: Cyan / Aqua.",
                            },
                            {
                                "prefix": "Se um código hexadecimal válido for informado.",
                                "args": "#FF4500",
                                "response": "#FF4500 é chamada de: Vermilion.",
                            },
                            {
                                "prefix": "Se o usuário tiver uma cor salva no banco de dados.",
                                "args": "mr_chuw",
                                "response": "A cor de @mr_chuw é: #00FFFF. Nome: Cyan / Aqua. "
                                "E possui a seguinte cor salva: #1E90FF. Nome: Dodger Blue.",
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
                                "position": "top",
                                "title": "Username or HEX",
                                "message": "You can input a Twitch username or a 6-digit "
                                "hexadecimal color code like #FF00FF.",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "info",
                                "position": "top",
                                "title": "Usuário ou HEX",
                                "message": "Você pode informar um nome de usuário do Twitch "
                                "ou um código hexadecimal de 6 dígitos como #FF00FF.",
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Color: Color
