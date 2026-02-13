from __future__ import annotations

import random
from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .interactive import InteractiveCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: InteractiveCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: InteractiveCmd = parent
        self.populate_subclasses(parent=self)

    class Fight(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Fight"

        def bot_nick(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def yourself(self, action: str) -> Response:
            text = self.get_text(self._cname, action=action)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def start(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def refused(self, user: str, target: str) -> Response:
            text = self.get_text(self._cname, user=user, target=target)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def timeout(self, target: str) -> Response:
            text = self.get_text(self._cname, target=target)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def options(self, user1: str, user2: str) -> Response:
            shuffled_names = random.sample([user1, user2], k=2)
            lines = self.get_text(self._cname, name1=shuffled_names[0], name2=shuffled_names[1]).splitlines()
            text = random.choice([line.strip() for line in lines if line.strip()])
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Fight: Fight

    class Hug(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Hug"

        def bot_nick(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def yourself(self, action: str) -> Response:
            text = self.get_text(self._cname, action=action)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def options(self, user: str, emote: str) -> Response:
            lines = self.get_text(self._cname, user=user, emote=emote).splitlines()
            text = random.choice([line.strip() for line in lines if line.strip()])
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Hug: Hug

    class Kiss(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Kiss"

        def bot_nick(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def yourself(self, action: str) -> Response:
            text = self.get_text(self._cname, action=action)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def options(self, user: str, emote: str) -> Response:
            lines = self.get_text(self._cname, user=user, emote=emote).splitlines()
            text = random.choice([line.strip() for line in lines if line.strip()])
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Kiss: Kiss

    class Ship(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Ship"

        def bot_nick(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def yourself(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        async def options(self, user1: str, user2: str, ship: str, percentage: int, emoji: str) -> Response:
            text = self.get_text(self._cname, user1=user1, user2=user2, ship=ship, percentage=percentage, emoji=emoji)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Ship: Ship

    class Pat(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Pat"

        def bot_nick(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def yourself(self, _=None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        async def options(self, user: str, emote: str) -> Response:
            lines = self.get_text(self._cname, user=user, emote=emote).splitlines()
            text = random.choice([line.strip() for line in lines if line.strip()])
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Pat: Pat

    class Penis(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Penis"

        def bot_nick(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def yourself(self, _=None) -> str:
            return self.ctx_get().author.name

        async def options(self, user: str, length: int, emoji: str) -> Response:
            lines = self.get_text(self._cname, user=user, length=length, emoji=emoji).splitlines()
            text = random.choice([line.strip() for line in lines if line.strip()])
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Penis: Penis

    class Slap(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Slap"

        def bot_nick(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def yourself(self, _=None) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        async def options(self, user1: str, percentage: int, emoji: str) -> Response:
            lines = self.get_text(self._cname, user1=user1, percentage=percentage, emoji=emoji).splitlines()
            text = random.choice([line.strip() for line in lines if line.strip()])
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Slap: Slap

    class Tuck(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Tuck"

        def bot_nick(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def yourself(self, emote: str) -> Response:
            text = self.get_text(self._cname, emote=emote)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        async def options(self, user1: str, emoji1: str, emoji2: str) -> Response:
            lines = self.get_text(self._cname, user1=user1, emoji1=emoji1, emoji2=emoji2).splitlines()
            text = random.choice([line.strip() for line in lines if line.strip()])
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    Tuck: Tuck
