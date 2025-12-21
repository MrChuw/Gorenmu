from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from bot.ext import Context, Response, commands
from bot.utils import StringTools, TimeTools
from bot.utils.timelength import DateParserConfig, TimeLength

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class TimeCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.StringTools: StringTools = StringTools()
        self.TimeTools: TimeTools = TimeTools()

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="time", aliases=[])
    async def time(self, ctx: Context, unit: str, *, args: str) -> Response:
        if not args.isascii() or not unit.isascii():
            return self.translations.Time.only_latin(ctx)
        extract = self.StringTools.extract_and_remove_all_fields
        rest, tipos = extract(args, "type", ["delta"])
        rest, lang = extract(rest, "lang", ["guess"])
        rest, accu = extract(rest, "accu", ["4"])
        lang = self.translations.Time.get_lang(ctx, lang[0].lower() != "guess", lang[0].lower() != "guess")
        dateconfig = DateParserConfig(allow_past=any(past in rest for past in lang().past.terms))
        lang = lang(dateconfig=dateconfig)
        rest = self.StringTools.remove_numeric_underscores(rest)
        tl = self.TimeTools.TimeConvert.convert_text(rest, lang)
        unit = self.TimeTools.TimeConvert.get_real_unit(unit, lang)
        supress = self.TimeTools.TimeConvert.to_supress(unit)
        minimum = "seconds" if unit in {"raw", "time"} else unit
        tipo = tipos[0]
        if tl.result.invalid or tipo:
            time, mode = self.TimeTools.TimeConvert.to_time(tipo if tipo != "delta" else None, ctx)
        else:
            time, mode = tl.result.delta
        if isinstance(time, datetime):
            time = time.replace(tzinfo=None)

        if not tl.result.delta and not tl.result.date:
            return self.translations.Time.overflow(ctx)

        try:
            precisedelta = await self.to_precise(accu[0], ctx, minimum, supress, time, tl, unit)
        except OverflowError:
            return self.translations.Time.overflow(ctx)
        except Exception as error:
            await self.bot.CommandHandler.send_bug(ctx, error)
            ctx.bot.log.warning(error)
            return self.translations.Exceptions.unexpected_error(ctx, error)

        if mode in tl.locale.past.terms:
            return self.translations.Time.past(ctx, precisedelta)
        elif mode in ("now", "future", *tl.locale.future.terms):
            return self.translations.Time.future(ctx, precisedelta)
        else:
            return self.translations.Time.present(ctx, precisedelta)

    @staticmethod
    def _to_seconds(time: datetime | timedelta) -> float:
        if isinstance(time, timedelta):
            return time.total_seconds()
        elif isinstance(time, datetime):
            return (time - datetime.now()).total_seconds()
        else:
            raise TypeError("time must be datetime or timedelta")

    async def to_precise(
        self,
        accu: str,
        ctx: Context,
        minimum: str | Any,
        supress: list[str],
        time: datetime | timedelta,
        tl: TimeLength,
        unit: str | Any,
    ) -> str:
        seconds = self._to_seconds(time)
        precision = int(accu[0])

        if unit == "weeks":
            precisedelta = (
                f"{round(seconds / tl.locale.week.scale, precision)} "
                f"{tl.locale.week.singular if seconds <= 1 else tl.locale.week.plural}"
            )

        elif unit == "decades":
            precisedelta = (
                f"{round(seconds / tl.locale.decade.scale, precision)} "
                f"{tl.locale.decade.singular if seconds <= 1 else tl.locale.decade.plural}"
            )

        elif unit == "centuries":
            precisedelta = (
                f"{round(seconds / tl.locale.century.scale, precision)} "
                f"{tl.locale.century.singular if seconds <= 1 else tl.locale.century.plural}"
            )
        else:
            precisedelta = self.translations.SupportTools.TimeTools.Humanize(ctx).precisedelta(
                time, suppress=supress, minimum_unit=minimum, format=f"%0.{accu}f"
            )
        return precisedelta


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(TimeCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
