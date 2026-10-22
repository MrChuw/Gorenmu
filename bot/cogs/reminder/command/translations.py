from __future__ import annotations

from typing import TYPE_CHECKING

from bot.cogs.time.command.translations import _get_cached_lang_logic
from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase, TranslationEntry
from bot.utils.timelength import English, Guess, Locale, Portuguese, Spanish

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .reminder import ReminderCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: ReminderCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.upper: ReminderCmd = parent
        self.Reminder: Reminder = Reminder(self)


class Reminder(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Reminder"
        super().__init__(parent, __file__)

    def bot_nick(self, **kwargs) -> Response:
        text = self.get_text(self._cname, **kwargs)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def author_too_much_reminds(self, **kwargs) -> Response:
        text = self.get_text(self._cname, **kwargs)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def user_too_much_reminds(self, mention: str) -> Response:
        text = self.get_text(self._cname, mention=mention)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def date_not_valid(self, date: str) -> Response:
        text = self.get_text(self._cname, date=date)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def remind_on_back(self, mention: str, remind_id: int) -> Response:
        text = self.get_text(self._cname, mention=mention, remind_id=remind_id)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def dont_have_time_machine(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def minimum_time(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def remind(self, mention: str, is_self: bool, remind_id: str) -> Response:
        text = self.get_text(self._cname, mention=mention, is_self=is_self, remind_id=remind_id)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def remind_after(self, mention: str, after: str, is_self: bool, remind_id: str) -> Response:
        text = self.get_text(self._cname, mention=mention, after=after, is_self=is_self, remind_id=remind_id)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def remind_after_in(
        self, mention: str, time: str, wait: str, after: str, is_self: bool, remind_id: str
    ) -> Response:
        text = self.get_text(
            self._cname, mention=mention, time=time, wait=wait, after=after, is_self=is_self, remind_id=remind_id
        )
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def remind_timed(self, mention, time: str, is_self: bool, remind_id: str) -> Response:
        text = self.get_text(self._cname, mention=mention, time=time, is_self=is_self, remind_id=remind_id)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def dispatched_message(self, target: str, mention: str, content: str, time_diff: str) -> str:
        return self.get_text(key=self._cname, target=target, mention=mention, content=content, time_diff=time_diff)

    def dispatched_blank_message(self, target: str, mention: str, time_diff: str) -> str:
        return self.get_text(key=self._cname, target=target, mention=mention, time_diff=time_diff)

    def get_lang(self, lang: bool, guess: bool = False, lang_hash=None) -> type[Locale]:
        result = _get_cached_lang_logic(self._cname, lang, guess, self, lang_hash)
        if isinstance(result, type) and issubclass(result, Guess):
            return English
        return result

    # --- Help Methods ---

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples(
            [
                {
                    "prefix": self.get_text("cmd_ex1_prefix"),
                    "args": "exemplo_arg",
                    "response": self.get_text("cmd_ex1_res"),
                }
            ]
        )

    def deco_admonitions(self, *args, **kwargs) -> Admonitions:
        return Admonitions(
            [
                {
                    "admonition_type": "info",
                    "position": "top",
                    "title": self.get_text("adm_title"),
                    "message": self.get_text("adm_msg"),
                }
            ]
        )
