from __future__ import annotations

import random
from pathlib import Path
from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.models import Cookies

    from .cookies import CookieCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: CookieCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.Cookies: TCookies = TCookies(self)
        self.Eat: Eat = Eat(self)
        self.Count: Count = Count(self)
        self.Gift: Gift = Gift(self)
        self.Stock: Stock = Stock(self)
        self.Top: Top = Top(self)
        self.SlotMachine: SlotMachine = SlotMachine(self)

    # region Hide.


class TCookies(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Cookies"
        super().__init__(parent, __file__)

    def invalid_option(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def daily_limit_reached(self, cooldown: str) -> Response:
        text = self.get_text(self._cname, cooldown=cooldown)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def user_not_found(self, name: str) -> Response:
        text = self.get_text(self._cname, name=name)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def cookie_not_found(self, name: str) -> Response:
        text = self.get_text(self._cname, name=name)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def all_string(self) -> list[str]:
        return self.parent.SupportTools.LanguageContext.Verbs.all()

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class Eat(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Cookie-Eat"
        super().__init__(parent, __file__)

    def not_eat(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def negative_eat(self, amount: int | float | str) -> Response:
        text = self.get_text(self._cname, amount=amount)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def multiple_eat(self, amount: int | float | str) -> Response:
        text = self.get_text(self._cname, amount=amount)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def eat(self, text: str) -> Response:
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def random_line(self) -> str:
        path = Path(__file__).parent / "extras" / self.get_text(self._cname)
        lines = path.read_text(encoding="utf-8").splitlines()
        return random.choice(lines) if lines else ""

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples([{"args": "eat", "response": self.get_text("cmd_ex1_res")}])


class Count(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Cookie-Count"
        super().__init__(parent, __file__)

    def cc_bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def format_cookie_count(self, mention: str, cookie: Cookies, verb: str) -> Response:
        text = self.get_text(
            self._cname,
            mention=mention,
            verb=verb,
            consumed=cookie.consumed,
            stocked=cookie.stocked,
            received=cookie.received,
            donated=cookie.donated,
            unredeemed=cookie.not_redeemed(),
            total=cookie.total,
        )
        return Response(ctx=self.ctx_get(), success=True, response=text.strip())

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples(
            [
                {"args": "cc", "response": self.get_text("cmd_ex1_res")},
                {"args": "cc other_user", "response": self.get_text("cmd_ex2_res")},
            ]
        )


class Gift(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Cookie-Gift"
        super().__init__(parent, __file__)

    def gift_bot_nick(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def gift_user_himself(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def gift_no_stock_but_cooldown(self, amount: int | str) -> Response:
        text = self.get_text(self._cname, amount=amount)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def not_gifted(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def negative_gift(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def multiple_gift(self, person: str, amount: int | float) -> Response:
        text = self.get_text(self._cname, person=person, amount=amount)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def gift(self, person: str) -> Response:
        text = self.get_text(self._cname, person=person)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def gift_on_cooldown_no_stock(self, cooldown: str) -> Response:
        text = self.get_text(self._cname, cooldown=cooldown)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples(
            [
                {"args": "gift other_user", "response": self.get_text("cmd_ex1_res")},
                {"args": "gift other_user 2", "response": self.get_text("cmd_ex2_res")},
                {"args": "gift other_user all", "response": self.get_text("cmd_ex3_res")},
            ]
        )

    def deco_admonitions(self, *args, **kwargs) -> Admonitions:
        return Admonitions(
            [
                {
                    "admonition_type": "warning",
                    "position": "top",
                    "title": self.get_text("adm1_title"),
                    "message": self.get_text("adm1_msg"),
                }
            ]
        )


class Stock(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Cookie-Stock"
        super().__init__(parent, __file__)

    def stock(self, amount: int | str) -> Response:
        text = self.get_text(self._cname, amount=amount)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def stock_not_daily(self, amount: int | str) -> Response:
        text = self.get_text(self._cname, amount=amount)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def stock_not_enough_cookies(self, amount: int | str) -> Response:
        text = self.get_text(self._cname, amount=amount)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples(
            [
                {"args": "stock", "response": self.get_text("cmd_ex1_res")},
                {"args": "stock all", "response": self.get_text("cmd_ex2_res")},
            ]
        )


class Top(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Cookie-Top"
        super().__init__(parent, __file__)

    def rank_dict(self) -> dict[str, list[str]]:
        return self.get_attributes_list(self._cname)

    def ranks(self, ranks: str) -> Response:
        text = self.get_text(self._cname, ranks=ranks)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def top10_ish(self, length: int | str, title: str, tops: str, index: int | str, amount: int | str) -> Response:
        text = self.get_text(self._cname, length=length, title=title, tops=tops, index=index, amount=amount)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples(
            [
                {"args": "top", "response": self.get_text("cmd_ex1_res")},
                {"args": "top donated", "response": self.get_text("cmd_ex2_res")},
            ]
        )


# endregion

class SlotMachine(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Cookie-SlotMachine"
        super().__init__(parent, __file__)

    def invalid_amount(self, amount: str, amount_available: int) -> Response:
        text = self.get_text(self._cname, amount=amount, available=amount_available)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def cookie_win_suffix(self, total: int, time_suffix: str) -> str:
        return self.get_text(self._cname, total=total, suffix=time_suffix)

    def cookie_loss_suffix(self, time_suffix: str) -> str:
        return self.get_text(self._cname, suffix=time_suffix)

    def accumulated_message(self, prefix: str, amount: str | int | float, suffix: str, emote: str) -> Response:
        text = self.get_text(self._cname, prefix=prefix, amount=amount, suffix=suffix, emote=emote)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def last_cookie_message(self, prefix: str, suffix: str, emote: str) -> Response:
        text = self.get_text(self._cname, prefix=prefix, suffix=suffix, emote=emote)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def time_suffix(self, time: str) -> str:
        return self.get_text(self._cname, time=time)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples(
            [
                {"args": "slotmachine", "response": self.get_text("cmd_ex1_res")},
                {"args": "slotmachine all", "response": self.get_text("cmd_ex2_res")},
            ]
        )

