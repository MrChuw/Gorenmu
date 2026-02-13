from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .set import SetCmd


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: SetCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: SetCmd = parent
        self.populate_subclasses(parent=self)

    class Set(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Set"

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        # endregion

    Set: Set

    class Mention(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Mention"

        def on_off_wrong_option(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def mention_on(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def mention_off(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

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

        # endregion

    Mention: Mention

    class City(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "City"

        def city_added(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def city_removed(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

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

        # endregion

    City: City

    class Nick(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Nick"

        def nick_too_large(self, limit: int | str) -> Response:
            text = self.get_text(self._cname, limit=str(limit))
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def nick_removed(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def nick_changed(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

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

        # endregion

    Nick: Nick

    class Color(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Color"

        def color_removed(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def color_changed(self, color: str) -> Response:
            text = self.get_text(self._cname, color=color)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

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

        # endregion

    Color: Color

    class Reminder(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Reminder"

        def reminder_on(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def reminder_off(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

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

        # endregion

    Reminder: Reminder

    class Banword(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Banword"

        def add_remove(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def add_remove_lang(self) -> dict[str, list[str]]:
            return {
                "add": [self.get_text("map_add")],
                "remove": [self.get_text("map_remove")],
                "clean": [self.get_text("map_clean")],
            }

        def who(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def added(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def removed(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def cleaned(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def what(self, option: str) -> Response:
            text = self.get_text(self._cname, option=option)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

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
                    {"args": f"{self.get_text('map_add')} blablabla", "response": self.get_text("added")},
                    {"args": f"{self.get_text('map_remove')} blablabla", "response": self.get_text("removed")},
                ]
            )

        # endregion

    Banword: Banword

    class Enable(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Enable"

        def why(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def no_command(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def command_already_enabled(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def command_enabled(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def command_disabled(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def command_already_disabled(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def options(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def all_enabled(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def all_disabled(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        # endregion

    Enable: Enable

    class Prefix(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Prefix"

        def too_long(self, arg: str, size: int | str) -> Response:
            text = self.get_text(self._cname, arg=arg, size=str(size))
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def prefix_changed(self, args: str) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        # endregion

    Prefix: Prefix

    class StartStop(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "StartStop"

        def started(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def already_on(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def stopped(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def already_off(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def shrug(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        # endregion

    StartStop: StartStop
