from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import CommandExemples, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class ProfilePicture(TBase):
        def __init__(self):
            super().__init__()

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Shows a user's Twitch profile image.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Mostra a imagem de perfil de um usuário da Twitch.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}profilepicture (username)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}profilepicture (nome_de_usuário)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "This command fetches the profile picture of the specified Twitch user "
                    "in high resolution. If no username is given, it uses the command author. "
                    "The image is uploaded and returned with a short link.",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Este comando obtém a imagem de perfil do usuário da Twitch especificado "
                    "em alta resolução. Se nenhum nome for informado, usa o autor do comando. "
                    "A imagem é enviada e retornada com um link encurtado.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"response": "https://twitch-cdn.example.com/profile.png https://short.url/pic"},
                            {
                                "args": "some_user",
                                "response": "https://twitch-cdn.example.com/profile.png https://short.url/pic",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"response": "https://twitch-cdn.example.com/profile.png https://short.url/pic"},
                            {
                                "args": "some_user",
                                "response": "https://twitch-cdn.example.com/profile.png https://short.url/pic",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    ProfilePicture: ProfilePicture
