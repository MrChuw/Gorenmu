from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .set import SetCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: SetCmd) -> None:
        super().__init__(bot=bot, file=__file__, upper=parent)
        self.Set: Set = Set(self)
        self.Mention: Mention = Mention(self)
        self.City: City = City(self)
        self.Nick: Nick = Nick(self)
        self.Color: Color = Color(self)
        self.Reminder: Reminder = Reminder(self)
        self.Banword: Banword = Banword(self)
        self.Enable: Enable = Enable(self)
        self.Prefix: Prefix = Prefix(self)
        self.StartStop: StartStop = StartStop(self)


class Set(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Set"
        super().__init__(parent, __file__)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class Mention(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Set-Mention"
        super().__init__(parent, __file__)

    def on_off_wrong_option(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def mention_on(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def mention_off(self) -> Response:
        text = self.get_text(self._cname)
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
                {
                    "prefix": self.get_text("cmd_on_prefix"),
                    "args": "mention on",
                    "response": self.get_text("mention_on"),
                },
                {
                    "prefix": self.get_text("cmd_off_prefix"),
                    "args": "mention off",
                    "response": self.get_text("mention_off"),
                },
            ]
        )


class City(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Set-City"
        super().__init__(parent, __file__)

    def city_added(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def city_removed(self) -> Response:
        text = self.get_text(self._cname)
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
                {
                    "prefix": self.get_text("cmd_set_prefix"),
                    "args": "city Fortaleza, Ce",
                    "response": self.get_text("city_added"),
                },
                {
                    "prefix": self.get_text("cmd_hide_prefix"),
                    "args": "city Fortaleza, Ce hidden:true",
                    "response": self.get_text("city_added"),
                },
                {
                    "prefix": self.get_text("cmd_latlong_prefix"),
                    "args": "city -27.12 -109.35 hidden:true",
                    "response": self.get_text("city_added"),
                },
                {
                    "prefix": self.get_text("cmd_remove_prefix"),
                    "args": "city remove",
                    "response": self.get_text("city_removed"),
                },
            ]
        )

    def deco_admonitions(self, *args, **kwargs) -> Admonitions:
        return Admonitions(
            [
                {
                    "admonition_type": "warning",
                    "position": "top",
                    "title": self.get_text("adm_hide_title"),
                    "message": self.get_text("adm_hide_msg"),
                }
            ]
        )


class Nick(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Set-Nick"
        super().__init__(parent, __file__)

    def nick_too_large(self, limit: int | str) -> Response:
        text = self.get_text(self._cname, limit=str(limit))
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def nick_removed(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def nick_changed(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    # region Hide.

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_commands(self, *args, **kwargs) -> CommandExemples:
        return CommandExemples(
            [
                {
                    "prefix": self.get_text("cmd_set_prefix"),
                    "args": "nick xXCoolNickNameXx",
                    "response": self.get_text("nick_changed"),
                },
                {
                    "prefix": self.get_text("cmd_remove_prefix"),
                    "args": "nick remove",
                    "response": self.get_text("nick_removed"),
                },
            ]
        )

    def deco_admonitions(self, *args, **kwargs) -> Admonitions:
        return Admonitions(
            [
                {
                    "admonition_type": "warning",
                    "position": "top",
                    "title": self.get_text("adm_short_title"),
                    "message": self.get_text("adm_short_msg"),
                }
            ]
        )


class Color(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Set-Color"
        super().__init__(parent, __file__)

    def color_removed(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def color_changed(self, color: str) -> Response:
        text = self.get_text(self._cname, color=color)
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
                {
                    "prefix": self.get_text("cmd_set_prefix"),
                    "args": "color #000000",
                    "response": self.get_text("color_changed"),
                },
                {
                    "prefix": self.get_text("cmd_remove_prefix"),
                    "args": "color remove",
                    "response": self.get_text("color_removed"),
                },
            ]
        )


class Reminder(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Set-Reminder"
        super().__init__(parent, __file__)

    def reminder_on(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def reminder_off(self) -> Response:
        text = self.get_text(self._cname)
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
                {
                    "prefix": self.get_text("cmd_on_prefix"),
                    "args": "reminder on",
                    "response": self.get_text("reminder_on"),
                },
                {
                    "prefix": self.get_text("cmd_off_prefix"),
                    "args": "reminder off",
                    "response": self.get_text("reminder_off"),
                },
            ]
        )


class Banword(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Set-Banword"
        super().__init__(parent, __file__)

    def add_remove(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def add_remove_lang(self) -> dict[str, list[str]]:
        return {
            "add": [self.get_text("map_add")],
            "remove": [self.get_text("map_remove")],
            "clean": [self.get_text("map_clean")],
        }

    def who(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def added(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def removed(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def cleaned(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def what(self, option: str) -> Response:
        text = self.get_text(self._cname, option=option)
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
                {"args": f"{self.get_text('map_add')} blablabla", "response": self.get_text("added")},
                {"args": f"{self.get_text('map_remove')} blablabla", "response": self.get_text("removed")},
            ]
        )


class Enable(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Set-Enable"
        super().__init__(parent, __file__)

    def why(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def no_command(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def command_already_enabled(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def command_enabled(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def command_disabled(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def command_already_disabled(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def options(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def all_enabled(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def all_disabled(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class Prefix(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Set-Prefix"
        super().__init__(parent, __file__)

    def too_long(self, arg: str, size: int | str) -> Response:
        text = self.get_text(self._cname, arg=arg, size=str(size))
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def prefix_changed(self, args: str) -> Response:
        text = self.get_text(self._cname, args=args)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)


class StartStop(TBase):
    def __init__(self, parent: Translations):
        self.prefix = "Set-StartStop"
        super().__init__(parent, __file__)

    def started(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def already_on(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def stopped(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=True, response=text)

    def already_off(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def shrug(self) -> Response:
        text = self.get_text(self._cname)
        return Response(ctx=self.ctx_get(), success=False, response=text)

    def deco_helper(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)

    def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
        return self.get_text(self._cname, prefix=prefix)

    def deco_description(self, *args, **kwargs) -> str:
        return self.get_text(self._cname)
