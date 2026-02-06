from __future__ import annotations

import random
from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .interactive import InteractiveCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, command: InteractiveCmd) -> None:
        super().__init__(bot)
        self.command: InteractiveCmd = command
        self.populate_subclasses(parent=self)

    class Fight(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)

        def bot_nick(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You would never be able to defeat me in a fight.")
                self.lang_dict.add_with(["pt_br", "pt"], "Você jamais seria capaz de me derrotar numa luta.")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        def yourself(self, action: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Please seek help.")
                self.lang_dict.add_with(["pt_br", "pt"], "Por favor, procure ajuda.")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), action)

        def start(self, name) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "@{} Do you accept the fight? (yes/no in chat)")
                self.lang_dict.add_with(["pt_br", "pt"], "@{} Você aceita a luta? (sim/não no chat)")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), name)

        def refused(self, user: str, target: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "@{} refused to fight {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "@{} recusou-se a lutar contra {}.")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), target, user)

        def timeout(self, target) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "10s passed and @{} decided not to accept the fight.")
                self.lang_dict.add_with(["pt_br", "pt"], "Passaram-se 10s e @{} decidiu não aceitar a luta.")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), target)

        def options(self, user1: str, user2) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    [
                        "@{} finishes @{}!",
                        "@{} knocks @{} unconscious!",
                        "@{} defeats @{} easily!",
                        "@{} beats @{} mercilessly!",
                        "@{} leaves no chance for @{} and wins!",
                        "@{} almost loses, but takes @{} down!",
                        "@{} wins the fight against @{}!",
                        "@{} defeats @{} with difficulty!",
                        "@{} wins against @{} in a close fight!",
                        "@{} easily beats @{}!",
                    ],
                )

                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    [
                        "@{} acaba com @{}!",
                        "@{} deixa @{} desacordado!",
                        "@{} derrota @{} facilmente!",
                        "@{} espanca @{} sem piedade!",
                        "@{} não dá chances para @{} e vence!",
                        "@{} quase perde, mas derruba @{}!",
                        "@{} vence a luta contra @{}!",
                        "@{} vence @{} com dificuldades!",
                        "@{} vence @{} em uma luta acirrada!",
                        "@{} vence @{} facilmente!",
                    ],
                )
            shuffled_names = random.sample([user1, user2], k=2)
            return response.format_response(
                random.choice(self._untangle_any(self.ctx_get(), self._cname)), shuffled_names[0], shuffled_names[1]
            )

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "fight someone.")
                self.lang_dict.add_with(["pt_br", "pt"], "Lute com alguém.")
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}fight (username)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}fight (username)")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "fight someone.")
                self.lang_dict.add_with(["pt_br", "pt"], "Lute com alguém.")
            return self._untangle_str(self.ctx_get(), self._cname)

    Fight: Fight

    class Hug(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)

        def bot_nick(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["en", "pt_br", "pt"], "🤗")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        def yourself(self, action: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you tried to hug yourself...")
                self.lang_dict.add_with(["pt_br", "pt"], "você tentou se abraçar...")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), action)

        def options(self, user: str, emote: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", ["gives @{} a big warm hug! {}", "hugged @{}! So sweet! {}"])

                self.lang_dict.add_with(
                    ["pt_br", "pt"], ["deu um abraço bem apertado em @{}! {}", "abraçou @{}! Que fofura! {}"]
                )
            return response.format_response(random.choice(self._untangle_any(self.ctx_get(), self._cname)), user, emote)

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "hug someone.")
                self.lang_dict.add_with(["pt_br", "pt"], "De um abraço em alguém.")
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}hug (username)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}hug (username)")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "hug someone.")
                self.lang_dict.add_with(["pt_br", "pt"], "De um abraço em alguém.")
            return self._untangle_str(self.ctx_get(), self._cname)

    Hug: Hug

    class Kiss(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)

        def bot_nick(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["en", "pt_br", "pt"], "😳")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        def yourself(self, action: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you tried to kiss yourself...")
                self.lang_dict.add_with(["pt_br", "pt"], "você tentou se beijar...")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), action)

        def options(self, user: str, emote: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", ["You gave @{} a little kiss {}"])
                self.lang_dict.add_with(["pt_br", "pt"], ["você deu um beijinho em @{} {}"])
            return response.format_response(random.choice(self._untangle_any(self.ctx_get(), self._cname)), user, emote)

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "kiss someone.")
                self.lang_dict.add_with(["pt_br", "pt"], "De um beijinho em alguém.")
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}kiss (username)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}kiss (username)")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "kiss someone.")
                self.lang_dict.add_with(["pt_br", "pt"], "De um beijinho em alguém.")
            return self._untangle_str(self.ctx_get(), self._cname)

    Kiss: Kiss

    class Ship(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.command: InteractiveCmd = parent.command

        def bot_nick(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["en", "pt_br", "pt"], "😳")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        def yourself(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "a person can't be shipped with themselves.")
                self.lang_dict.add_with(["pt_br", "pt"], "uma pessoa não pode ser shippada com ela mesma...")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        async def options(
            self,
            user1: str,
            user2: str,
            ship: str,
            percentage: int,
            emoji: str,
        ) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", ["@{} & @{}: {} with {}% love {}"])
                self.lang_dict.add_with(["pt_br", "pt"], ["@{} & @{}: {} com {}% de amor {}"])
            return response.format_response(
                random.choice(self._untangle_any(self.ctx_get(), self._cname)),
                user1,
                user2,
                ship,
                percentage,
                emoji,
            )

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Ship someone with someone else.")
                self.lang_dict.add_with(["pt_br", "pt"], "De um shippe alguém com outra pessoa.")
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}Ship (username1) (username2)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}Ship (username1) (username2)")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Ship someone with someone else.")
                self.lang_dict.add_with(["pt_br", "pt"], "De um shippe alguém com outra pessoa.")
            return self._untangle_str(self.ctx_get(), self._cname)

    Ship: Ship

    class Pat(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.command: InteractiveCmd = parent.command

        def bot_nick(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["en", "pt_br", "pt"], "😊")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        def yourself(self, _=None) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You tried to pat yourself...")
                self.lang_dict.add_with(["pt_br", "pt"], "você tentou fazer cafuné em si mesmo...")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        async def options(self, user: str, emote) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", ["you gave a pat to @{} {}"])
                self.lang_dict.add_with(["pt_br", "pt"], ["você fez cafuné em @{} {}"])
            return response.format_response(random.choice(self._untangle_any(self.ctx_get(), self._cname)), user, emote)

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Pat someone.")
                self.lang_dict.add_with(["pt_br", "pt"], "De um cafuné em alguém.")
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}Pat (username)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}Pat (username)")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Pat someone.")
                self.lang_dict.add_with(["pt_br", "pt"], "De um cafuné em alguém.")
            return self._untangle_str(self.ctx_get(), self._cname)

    Pat: Pat

    class Penis(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.command: InteractiveCmd = parent.command

        def bot_nick(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["en"], "I only have a pen drive")
                self.lang_dict.add_with(["pt_br", "pt"], "eu só tenho pen drive")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        def yourself(self, _=None) -> str:
            return self.ctx_get().author.name

        async def options(self, user: str, length: int, emoji: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", ["{} has {}cm {}"])
                self.lang_dict.add_with(["pt_br", "pt"], ["{} tem {}cm {}"])
            return response.format_response(
                random.choice(self._untangle_any(self.ctx_get(), self._cname)), user, length, emoji
            )

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["en", "pt_br", "pt"], "FeelsWeirdMan")
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}penis (username)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}penis (username)")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["en", "pt_br", "pt"], "FeelsWeirdMan ")
            return self._untangle_str(self.ctx_get(), self._cname)

    Penis: Penis

    class Slap(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.command: InteractiveCmd = parent.command

        def bot_nick(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["en"], "go hit your mom 😠")
                self.lang_dict.add_with(["pt_br", "pt"], "vai bater na mãe 😠")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        def yourself(self, _=None) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you slapped yourself... 😕")
                self.lang_dict.add_with(["pt_br", "pt"], "você se deu um tapa... 😕")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        async def options(self, user1: str, percentage: int, emoji: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", ["you slapped @{} with {}% force {}"])
                self.lang_dict.add_with(["pt_br", "pt"], ["você deu um tapa em @{} com {}% força {}"])

            return response.format_response(
                random.choice(self._untangle_any(self.ctx_get(), self._cname)), user1, percentage, emoji
            )

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Slap someone.")
                self.lang_dict.add_with(["pt_br", "pt"], "De um tapa em alguém.")
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}slap (username)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}slap (username)")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Slap someone.")
                self.lang_dict.add_with(["pt_br", "pt"], "De um tapa em alguém.")
            return self._untangle_str(self.ctx_get(), self._cname)

    Slap: Slap

    class Tuck(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.command: InteractiveCmd = parent.command

        def bot_nick(self) -> Response:
            response = Response(ctx=self.ctx_get(), success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["en"], "I can't sleep right now...")
                self.lang_dict.add_with(["pt_br", "pt"], "eu não posso dormir agora...")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname))

        def yourself(self, emote: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You went to bed. 🛏")
                self.lang_dict.add_with(["pt_br", "pt"], "você foi para a cama. 🛏")
            return response.format_response(self._untangle_str(self.ctx_get(), self._cname), emote)

        async def options(self, user1: str, emoji1: str, emoji2: str) -> Response:
            response = Response(ctx=self.ctx_get(), success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", ["You put @{} in bed {}👉{}"])
                self.lang_dict.add_with(["pt_br", "pt"], ["você colocou @{} na cama {}👉{}"])
            return response.format_response(
                random.choice(self._untangle_any(self.ctx_get(), self._cname)), user1, emoji1, emoji2
            )

        def deco_helper(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Send someone to bed.")
                self.lang_dict.add_with(["pt_br", "pt"], "Envie alguém para cama.")
            return self._untangle_str(self.ctx_get(), self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}tuck (username)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}tuck (username)")
            return self._untangle_str(self.ctx_get(), self._cname).format(prefix)

        def deco_description(self, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Send someone to bed.")
                self.lang_dict.add_with(["pt_br", "pt"], "Envie alguém para cama.")
            return self._untangle_str(self.ctx_get(), self._cname)

    Tuck: Tuck
