from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class AFK(TBase):
        def __init__(self):
            super().__init__()

        def afk(self, ctx: Context, status: str, emoji: str) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("afk"):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{} {}")
            return response.format_response(self._untangle_str(ctx, "afk"), status, emoji)

        afk: Response = afk

        def content(self, ctx: Context, status: str, emoji: str, content: str) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("content"):
                self.lang_dict.add_with("en", "{} {} and left a note with: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{} {} e deixou uma nota com: {}")
            return response.format_response(self._untangle_str(ctx, "content"), status, emoji, content)

        content: Response = content

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("helper"):
                self.lang_dict.add_with("en", "Command to set your status.")
                self.lang_dict.add_with(["pt_br", "pt"], "Comando para definir seu status.")
            return self._untangle_str(ctx, "helper")

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once("usage"):
                self.lang_dict.add_with("en", "How to use: {}Afk (message)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}Afk (mensagem)")
            return self._untangle_str(ctx, "usage").format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("description"):
                self.lang_dict.add_with("en", "This command sets your status to AFK.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando define seu status para AFK.")
            return self._untangle_str(ctx, "description")

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once("commands"):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"response": "you went AFK: 🏃 ⌨️"},
                            {
                                "args": "Nice message.",
                                "response": "you went AFK: 🏃 ⌨️ and left a note with: Nice message.",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"response": "você foi AFK: 🏃 ⌨️"},
                            {
                                "args": "Mensagem legal.",
                                "response": "você ficou AFK: 🏃 ️ e deixou um bilhete com: Mensagem legal.",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, "commands")

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once("admonitions"):
                self.lang_dict.add_with(
                    "en",
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "title": "Maximum length!",
                                "message": "The message could not be longer than 450 characters.",
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
                                "title": "Tamanho máximo!",
                                "message": "A mensagem não poderia ser mais de 450 caracteres.",
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, "admonitions")

        def afks(self, ctx) -> dict[str, Activity.Status]:
            with self.lang_dict.once("afks"):
                self.lang_dict.add_with(
                    "en",
                    Activity(
                        {
                            "property": {
                                "current": "it's",
                                "leave": "you",
                                "leave_again": "you continued",
                                "returned": "you",
                            },
                            "afks": {
                                "afk": [
                                    "afk",
                                    "🏃⌨",
                                    "went afk",
                                    "afk",
                                    "came back",
                                    "afk",
                                ],
                                "read": [
                                    "read",
                                    "📖",
                                    "went to read",
                                    "reading",
                                    "read",
                                    "reading",
                                ],
                                "brb": [
                                    "brb",
                                    "🏃⌨",
                                    "coming back soon",
                                    "away",
                                    "came back",
                                    "away",
                                ],
                                "eat": [
                                    "food",
                                    "🍽",
                                    "went to eat",
                                    "eating",
                                    "ate",
                                    "eating",
                                ],
                                "food": [
                                    "food",
                                    "🍽",
                                    "went to eat",
                                    "eating",
                                    "ate",
                                    "eating",
                                ],
                                "play": [
                                    "game",
                                    "🎮",
                                    "went to play",
                                    "playing",
                                    "played",
                                    "playing",
                                ],
                                "game": [
                                    "game",
                                    "🎮",
                                    "went to play",
                                    "playing",
                                    "played",
                                    "playing",
                                ],
                                "sleep": [
                                    "gn",
                                    "💤",
                                    "went to sleep",
                                    "sleeping",
                                    "woke up",
                                    "sleeping",
                                ],
                                "night": [
                                    "gn",
                                    "💤",
                                    "went to sleep",
                                    "sleeping",
                                    "woke up",
                                    "sleeping",
                                ],
                                "study": [
                                    "study",
                                    "📚",
                                    "went to study",
                                    "studying",
                                    "studied",
                                    "studying",
                                ],
                                "art": [
                                    "art",
                                    "🎨",
                                    "went to draw",
                                    "drawing",
                                    "drew",
                                    "drawing",
                                ],
                                "watch": [
                                    "watch",
                                    "📺",
                                    "went to watch",
                                    "watching",
                                    "watched",
                                    "watching",
                                ],
                                "shower": [
                                    "shower",
                                    "🚿",
                                    "went to shower",
                                    "in the shower",
                                    "took a shower",
                                    "the shower",
                                ],
                                "code": [
                                    "code",
                                    "💻",
                                    "went to code",
                                    "coding",
                                    "coded",
                                    "coding",
                                ],
                                "work": [
                                    "work",
                                    "💼",
                                    "went to work",
                                    "working",
                                    "worked",
                                    "working",
                                ],
                            },
                        }
                    ).afks,
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Activity(
                        {
                            "property": {
                                "current": "está",
                                "leave": "você",
                                "leave_again": "você continuou",
                                "returned": "você",
                            },
                            "afks": {
                                "afk": [
                                    "afk",
                                    "🏃⌨",
                                    "ficou ausente",
                                    "ausente",
                                    "voltou",
                                    "ausente",
                                ],
                                "read": [
                                    "read",
                                    "📖",
                                    "foi ler",
                                    "lendo",
                                    "leu",
                                    "lendo",
                                ],
                                "brb": [
                                    "brb",
                                    "🏃⌨",
                                    "volta logo",
                                    "ausente",
                                    "voltou",
                                    "ausente",
                                ],
                                "eat": [
                                    "food",
                                    "🍽",
                                    "foi comer",
                                    "comendo",
                                    "comeu",
                                    "comendo",
                                ],
                                "food": [
                                    "food",
                                    "🍽",
                                    "foi comer",
                                    "comendo",
                                    "comeu",
                                    "comendo",
                                ],
                                "play": [
                                    "game",
                                    "🎮",
                                    "foi jogar",
                                    "jogando",
                                    "jogou",
                                    "jogando",
                                ],
                                "game": [
                                    "game",
                                    "🎮",
                                    "foi jogar",
                                    "jogando",
                                    "jogou",
                                    "jogando",
                                ],
                                "sleep": [
                                    "gn",
                                    "💤",
                                    "foi dormir",
                                    "dormindo",
                                    "acordou",
                                    "dormindo",
                                ],
                                "night": [
                                    "gn",
                                    "💤",
                                    "foi dormir",
                                    "dormindo",
                                    "acordou",
                                    "dormindo",
                                ],
                                "study": [
                                    "study",
                                    "📚",
                                    "foi estudar",
                                    "estudando",
                                    "estudou",
                                    "estudando",
                                ],
                                "art": [
                                    "art",
                                    "🎨",
                                    "foi desenhar",
                                    "desenhando",
                                    "desenhou",
                                    "desenhando",
                                ],
                                "watch": [
                                    "watch",
                                    "📺",
                                    "foi assistir",
                                    "assistindo",
                                    "assistiu",
                                    "assistindo",
                                ],
                                "shower": [
                                    "shower",
                                    "🚿",
                                    "foi tomar banho",
                                    "no banho",
                                    "tomou banho",
                                    "no banho",
                                ],
                                "code": [
                                    "code",
                                    "💻",
                                    "foi programar",
                                    "programando",
                                    "programou",
                                    "programando",
                                ],
                                "work": [
                                    "work",
                                    "💼",
                                    "foi trabalhar",
                                    "trabalhando",
                                    "trabalhou",
                                    "trabalhando",
                                ],
                            },
                        }
                    ).afks,
                )
            return self._untangle_any(ctx, "afks")

        def _get_afks(self, lang="en") -> dict[str, Activity.Status]:
            return self.lang_dict.get_lang(lang, "afks")  # NOQA

    AFK: AFK

    class IsAFK(TBase):
        def __init__(self):
            super().__init__()

        def bot(self, ctx: Context):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)  # NOQA
            with self.lang_dict.once("bot"):
                self.lang_dict.add_with("en", "I'm always here… watching.")
                self.lang_dict.add_with(["pt_br", "pt"], "Estou sempre aqui... assistindo.")
            return response.format_response(self._untangle_str(ctx, "bot"))

        bot: Response = bot

        def author(self, ctx: Context):
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once("author"):
                self.lang_dict.add_with("en", "you're not afk… obviously.")
                self.lang_dict.add_with(["pt_br", "pt"], "você não está afk... obviamente.")
            return response.format_response(self._untangle_str(ctx, "author"))

        author: Response = author

        def is_afk(self, ctx: Context, name: str, status: str, emoji: str, time: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("is_afk"):
                self.lang_dict.add_with("en", "@{} {} {} (for {})")
                self.lang_dict.add_with(["pt_br", "pt"], "@{} {} {} (há {})")
            return response.format_response(self._untangle_str(ctx, "is_afk"), name, status, emoji, time)

        is_afk: Response = is_afk

        def is_afk_content(
            self,
            ctx: Context,
            name: str,
            status: str,
            emoji: str,
            message: str,
            time: str,
        ):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("is_afk_content"):
                self.lang_dict.add_with("en", "@{} {} {} and left a note: {} (for {})")
                self.lang_dict.add_with(["pt_br", "pt"], "@{} {} {} e deixou uma nota: {} (há {})")
            return response.format_response(
                self._untangle_str(ctx, "is_afk_content"),
                name,
                status,
                emoji,
                message,
                time,
            )

        is_afk_content: Response = is_afk_content

        def is_not_afk(self, ctx: Context, name: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("is_not_afk"):
                self.lang_dict.add_with("en", "@{} is not AFK.")
                self.lang_dict.add_with(["pt_br", "pt"], "@{} não é AFK.")
            return response.format_response(self._untangle_str(ctx, "is_not_afk"), name)

        is_not_afk: Response = is_not_afk

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("helper"):
                self.lang_dict.add_with("en", "Type the command and the user's name to see if they are AFK.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Digite o comando e o nome do usuário para ver se eles são AFK.",
                )
            return self._untangle_str(ctx, "helper")

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once("usage"):
                self.lang_dict.add_with("en", "How to use: {}IsAfk (username)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}IsAfk (nome de usuário)")
            return self._untangle_str(ctx, "usage").format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("description"):
                self.lang_dict.add_with("en", "This command checks if a user is AFK or not.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando verifica se um usuário é AFK ou não.")
            return self._untangle_str(ctx, "description")

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once("commands"):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "user2", "response": "@user2 is not AFK."},
                            {"args": "user3", "response": "@user3 is AFK."},
                            {
                                "args": "user4",
                                "response": "@user4 is AFK and left a note: <message>",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"response": "@usuário2 não está AFK.", "args": "usuário2"},
                            {"args": "usuário3", "response": "@usuário3 está AFK."},
                            {
                                "args": "usuário4",
                                "response": "@usuário4 está AFK e deixou uma nota: <message>",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, "commands")

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once("admonitions"):
                self.lang_dict.add_with("en", Admonitions([]))
                self.lang_dict.add_with(["pt_br", "pt"], Admonitions([]))
            return self._untangle_admonitions(ctx, "admonitions")

    IsAFK: IsAFK

    class RAFK(TBase):
        def __init__(self):
            super().__init__()

        def return_expired(self, ctx: Context):
            with self.lang_dict.once("return_expired"):
                self.lang_dict.add_with("en", "to return AFK")
                self.lang_dict.add_with(["pt_br", "pt"], "para retornar AFK")
            return self._untangle_str(ctx, "return_expired")

        return_expired: Response = return_expired

        def afk(self, ctx: Context, status: str, emoji: str) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("afk"):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{} {}")
            return response.format_response(self._untangle_str(ctx, "afk"), status, emoji)

        afk: Response = afk

        def content(self, ctx: Context, status: str, emoji: str, content: str) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("content"):
                self.lang_dict.add_with("en", "{} {} and left a note with: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{} {} e deixou uma nota com: {}")
            return response.format_response(self._untangle_str(ctx, "content"), status, emoji, content)

        content: Response = content

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("helper"):
                self.lang_dict.add_with("en", "Return to AFK status.")
                self.lang_dict.add_with(["pt_br", "pt"], "Retornar ao status AFK.")
            return self._untangle_str(ctx, "helper")

        def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once("usage"):
                self.lang_dict.add_with("en", "To use: {}rafk")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}rafk")
            return self._untangle_str(ctx, "usage").format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once("description"):
                self.lang_dict.add_with("en", "This command is used to return to AFK status.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando é usado para retornar ao status AFK.")
            return self._untangle_str(ctx, "description")

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once("commands"):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"response": "@user2 you remained AFK: 🏃 ⌨️"},
                            {
                                "args": "(message)",
                                "response": "@user2 you remained AFK: 🏃 ⌨️ and left a note: (message)",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"response": "@usuário2 você permaneceu AFK: 🏃 ⌨️"},
                            {
                                "args": "(mensagem)",
                                "response": "@usuário2 você permaneceu AFK: 🏃 ⌨️ e deixou uma nota: (mensagem)",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, "commands")

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once("admonitions"):
                self.lang_dict.add_with(
                    "en",
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "title": "Maximum Time!",
                                "message": "From the moment you send a message in the chat, "
                                "you have 2 minutes to return to AFK status. ",
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
                                "title": "Tempo máximo!",
                                "message": "A partir do momento em que você envia uma mensagem no chat, "
                                "você tem 2 minutos para retornar ao status AFK. ",
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, "admonitions")

    RAFK: RAFK

    class AFKReturn(TBase):
        def __init__(self):
            super().__init__()

        def afk(self, ctx: Context, status: str, emoji: str, a_time: str, clock: str):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("afk"):
                self.lang_dict.add_with("en", "{} {} (was away for {} {})")
                self.lang_dict.add_with(["pt_br", "pt"], "{} {} (estava ausente por {} {})")
            return response.format_response(self._untangle_str(ctx, "afk"), status, emoji, a_time, clock)

        afk: Response = afk

        def content(
            self,
            ctx: Context,
            status: str,
            emoji: str,
            message: str,
            a_time: str,
            clock: str,
        ):
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once("content"):
                self.lang_dict.add_with("en", "{} {} and left a note: {} (was away for {} {})")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "{} {} e deixou uma nota: {} (estava ausente por {} {})",
                )
            return response.format_response(
                self._untangle_str(ctx, "content"),
                status,
                emoji,
                message,
                a_time,
                clock,
            )

        content: Response = content


class Activity:
    @dataclass
    class Status:
        _name: str
        _emoji: str
        _leave: str
        _current: str
        _returned: str
        _leave_again: str
        _property: dict

        @property
        def current(self) -> str:
            return f"{self._property['current']} {self._current}"

        @property
        def leave(self) -> str:
            return f"{self._property['leave']} {self._leave}"

        @property
        def leave_again(self) -> str:
            return f"{self._property['leave_again']} {self._leave_again}"

        @property
        def returned(self) -> str:
            return f"{self._property['returned']} {self._returned}"

        @property
        def emoji(self) -> str:
            return self._emoji

        @property
        def name(self) -> str:
            return self._name

    def __init__(self, data: dict[str, dict]):
        self.property: dict = data.get("property")
        self.afks = {}
        for key, value in data.get("afks").items():
            self.afks[key] = Activity.Status(*value, _property=self.property)
