from __future__ import annotations

import random
from typing import TYPE_CHECKING

from bot.ext import Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .interactive import InteractiveCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: InteractiveCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.Fight: Fight = Fight(self)
        self.Hug: Hug = Hug(self)
        self.Kiss: Kiss = Kiss(self)
        self.Ship: Ship = Ship(self)
        self.Pat: Pat = Pat(self)
        self.Penis: Penis = Penis(self)
        self.Slap: Slap = Slap(self)
        self.Tuck: Tuck = Tuck(self)


class TranslationTyping(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Typing"
        super().__init__(parent, __file__)

    def bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def yourself(self, action: str) -> Response:
        text = self.get_text(self._cname, action=action)
        return Response(ctx=self.ctx_get(), success=False, response=text)


class Fight(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Fight"
        super().__init__(parent, __file__)

    def bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def yourself(self, action: str) -> Response:
        text = self.get_text(self._cname, action=action)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def start(self, name: str) -> Response:
        text = self.get_text(self._cname, name=name)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def refused(self, user: str, target: str) -> Response:
        text = self.get_text(self._cname, user=user, target=target)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def timeout(self, target: str) -> Response:
        text = self.get_text(self._cname, target=target)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def options(self, user1: str, user2: str) -> Response:
        shuffled_names = random.sample([user1, user2], k=2)
        lines = self.get_text(self._cname, name1=shuffled_names[0], name2=shuffled_names[1]).splitlines()
        text = random.choice([line.strip() for line in lines if line.strip()])
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class Hug(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Hug"
        super().__init__(parent, __file__)

    def bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def yourself(self, action: str) -> Response:
        text = self.get_text(self._cname, action=action)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def options(self, user: str, emote: str) -> Response:
        lines = self.get_text(self._cname, user=user, emote=emote).splitlines()
        text = random.choice([line.strip() for line in lines if line.strip()])
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class Kiss(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Kiss"
        super().__init__(parent, __file__)

    def bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def yourself(self, action: str) -> Response:
        text = self.get_text(self._cname, action=action)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def options(self, user: str, emote: str) -> Response:
        lines = self.get_text(self._cname, user=user, emote=emote).splitlines()
        text = random.choice([line.strip() for line in lines if line.strip()])
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class Ship(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Ship"
        super().__init__(parent, __file__)

    def bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def yourself(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    async def options(self, user1: str, user2: str, ship: str, percentage: int, emoji: str) -> Response:
        text = self.get_text(self._cname, user1=user1, user2=user2, ship=ship, percentage=percentage, emoji=emoji)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def forgot_option1(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def forgot_option2(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class Pat(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Pat"
        super().__init__(parent, __file__)

    def bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def yourself(self, _=None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    async def options(self, user: str, emote: str) -> Response:
        lines = self.get_text(self._cname, user=user, emote=emote).splitlines()
        text = random.choice([line.strip() for line in lines if line.strip()])
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class Penis(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Penis"
        super().__init__(parent, __file__)

    def bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def yourself(self, _=None) -> str:
        return self.ctx_get().author.name or ""

    async def options(self, user: str, length: int, emoji: str) -> Response:
        lines = self.get_text(self._cname, user=user, length=length, emoji=emoji).splitlines()
        text = random.choice([line.strip() for line in lines if line.strip()])
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class Slap(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Slap"
        super().__init__(parent, __file__)

    def bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def yourself(self, _=None) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    async def options(self, user1: str, percentage: int, emoji: str) -> Response:
        lines = self.get_text(self._cname, user1=user1, percentage=percentage, emoji=emoji).splitlines()
        text = random.choice([line.strip() for line in lines if line.strip()])
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class Tuck(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Tuck"
        super().__init__(parent, __file__)

    def bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def yourself(self, emote: str) -> Response:
        text = self.get_text(self._cname, emote=emote)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    async def options(self, user1: str, emoji1: str, emoji2: str) -> Response:
        lines = self.get_text(self._cname, user1=user1, emoji1=emoji1, emoji2=emoji2).splitlines()
        text = random.choice([line.strip() for line in lines if line.strip()])
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

