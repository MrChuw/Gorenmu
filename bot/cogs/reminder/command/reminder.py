from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from re import Match
from typing import TYPE_CHECKING

from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from bot.ext import Context, Response, commands, routine
from bot.models import Reminder, User
from bot.utils import SessionsCaches, StringTools, TimeTools
from bot.utils.ratelimiter import RateLimiter
from bot.utils.timelength import DateParserConfig

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ReminderCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, parent=self)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.TimeTools: TimeTools = TimeTools()
        self.bot.RoutineHandler.add_routine_sync("remind", self.routine)
        self.in_flight_reminders: set[int] = set()
        self.limiter = RateLimiter()
        self.limiter.configure(bucket_path="irc:remind", max_calls=10, period=0.5)

    @commands.command(name="remind", aliases=["remindme", "reminder", "reminderme"])
    async def reminder(self, ctx: Context, *, content: str) -> Response:
        if not content or not content.strip():
            return self.translations.Exceptions.no_content_provided(ctx)

        invoke_by = (ctx.content.partition(" ")[0][len(ctx.prefix) :].lower()).replace(ctx.prefix, "")
        name = content.strip().split(" ", maxsplit=1)[0]
        name: str = ctx.author_name if name == "me" else self.StringTools.str2name_or(name)

        if name.lower() == ctx.bot_name.lower():
            return self.translations.Reminder.bot_nick()

        user = None
        if invoke_by in ["remindme", "reminderme"] or name == "me":
            user = ctx.user
            name = ctx.author_name
        if name == "in":
            name = ctx.author_name

        content_part = ctx.message.text.partition(" ")[2]
        if all(ext not in name for ext in [",", " ", "."]):
            content_part = content_part.replace(name, "").lstrip()

        future = bool(content_part.startswith(("in ", "on ")))
        if future:
            content_part = content_part[3:]

        extract = self.StringTools.extract_and_remove_all_fields
        rest, user_ = extract(content_part, "user", [])
        rest, users_ = extract(rest, "users", [])

        if name and any(ext in name for ext in (",", " ", ".")):
            users_.append(name)
            rest = rest.replace(name, "").lstrip()
            future = rest.startswith(("in ", "on "))
            if future:
                rest = rest[3:]
            name = ""

        users: list[User] = []
        if user_ or users_:
            names_to_fetch = {
                n for name_ in set(users_ + user_) for n in self.StringTools.multi_split(name_, [",", " ", "."])
            }
            for name_ in names_to_fetch:
                if name_.lower() == ctx.bot_name.lower():
                    continue
                user_obj = await User.get_user(ctx, self.translations, name=name_, is_none=True)
                if not user_obj:
                    return self.translations.Exceptions.user_not_found_name(name_)
                if isinstance(user_obj, Response):
                    return user_obj
                if user_obj.mention:
                    users.append(user_obj)

        if (not user and name) or not users:
            user = await User.get_user(ctx, self.translations, name=name, is_none=True)
        if not user and not users:
            return self.translations.Exceptions.user_not_found_name(name)
        if not user and users and not name:
            user, name = users[0], users[0].name

        if isinstance(user, Response):
            return user
        if not user:
            return self.translations.Exceptions.user_not_found_name(name)

        if user.mention is False and ctx.author.name != user.name:
            return self.translations.Exceptions.user_opt_out(user.nickname or user.name)
        if users:
            mention = self.translations.SupportTools.LanguageContext.multi_mention([user_.name for user_ in users])
        else:
            mention = self.translations.SupportTools.LanguageContext.mention(ctx.user.name, name)
        reminder = await Reminder.filter(from_user=ctx.user, sent=False).count()
        reminder_to = await Reminder.filter(to_user=(ctx.user if name == ctx.author.name else user), sent=False).count()

        if reminder > 50 and ctx.author.name != "mr_chuw":
            return self.translations.Reminder.author_too_much_reminds()
        if reminder_to > 50 and ctx.author.name != "mr_chuw":
            return self.translations.Reminder.user_too_much_reminds(mention)

        rest, lang = extract(rest, "lang", ["english"])
        rest, after = self.StringTools.extract_quotation(rest, "after", None)
        rest, on_ = self.StringTools.extract_quotation(rest, "on", None)
        rest, at_ = self.StringTools.extract_quotation(rest, "at", None)
        rest, in_ = self.StringTools.extract_quotation(rest, "in", None)
        lang = self.translations.Reminder.get_lang(
            lang[0].lower() != "english", lang[0].lower() != "english", ctx.user.language
        )
        timezone = await ctx.user.tz(self.bot)
        dateconfig = DateParserConfig(allow_past=any(past in rest for past in lang().past.terms), timezone=timezone)
        rest, to_remove = self.find_time(rest)
        lang = lang(dateconfig=dateconfig)
        rest = rest if in_ else self.StringTools.remove_numeric_underscores(in_[0] if in_ else rest)
        tl_outer = self.TimeTools.TimeConvert
        tl = tl_outer.convert_text(in_[0] if in_ else rest, lang, timezone=timezone)
        _after_time = None
        scheduled_for_original: datetime | None = None
        is_self = user.name.lower() == name.lower()

        if not tl.result.success and future:
            return self.translations.Reminder.date_not_valid(rest)

        if after or on_ or at_:
            date = after[0] if after else (on_[0] if on_ else at_[0])
            tl_inner = self.TimeTools.TimeConvert
            tl_bonus = tl_inner.convert_text(date, lang, timezone=timezone)
            if tl_bonus.result.invalid:
                return self.translations.Reminder.date_not_valid(date)
            _after_time, _ = tl_inner.to_time("mode", timezone)
            if tl.result.success:
                scheduled_for, _ = tl_outer.to_hence(tl.locale.future.terms[0], _after_time, timezone)
            else:
                scheduled_for = None
        elif tl.result.success:
            scheduled_for, _ = tl_outer.to_time(tl.locale.now.terms[0], timezone)
        else:
            scheduled_for = None
        content = rest.replace(to_remove.group(0), "") if not in_ and to_remove else rest

        all_users = set(users)
        all_users.add(user)
        created_reminders = []
        humanize = self.translations.SupportTools.TimeTools.Humanize(ctx.user.language)
        humanize.set_tz(timezone)

        if scheduled_for is None:
            after_precise: str = ""
            _after_dt: datetime | None = None

            if _after_time:
                now = datetime.now(timezone)
                _after_dt = now + _after_time if isinstance(_after_time, timedelta) else _after_time

                if _after_dt < now:
                    return self.translations.Reminder.dont_have_time_machine()
                if (_after_dt - now) < timedelta(seconds=59):
                    return self.translations.Reminder.minimum_time()

                after_precise: str = humanize.precisedelta((_after_dt - now).total_seconds(), format=f"%0.{2}f")

            async with in_transaction():
                for u in all_users:
                    remind = await Reminder.create(
                        from_user=ctx.user,
                        to_user=u,
                        content=content,
                        scheduled_for=_after_dt or None,
                        for_after=_after_dt or None,
                    )
                    created_reminders.append(remind)

            await self._cache_pending_reminders(created_reminders, all_users)

            remind_id = ",".join([str(remind.id) for remind in created_reminders])

            if _after_dt:
                return self.translations.Reminder.remind_after(mention, after_precise, is_self, remind_id)

            return self.translations.Reminder.remind(mention, is_self, remind_id)

        now = datetime.now(timezone)

        if isinstance(scheduled_for, datetime):
            if scheduled_for < now:
                return self.translations.Reminder.dont_have_time_machine()
            if (scheduled_for - now) < timedelta(seconds=59):
                return self.translations.Reminder.minimum_time()
        elif isinstance(scheduled_for, timedelta):
            if scheduled_for < timedelta(seconds=59):
                if scheduled_for < timedelta(0):
                    return self.translations.Reminder.dont_have_time_machine()
                return self.translations.Reminder.minimum_time()

        _after_time: datetime | timedelta | None

        created_reminders = []

        scheduled_for_precise = humanize.precisedelta((scheduled_for_original or scheduled_for), format=f"%0.{2}f")

        after_precise = None

        if after and _after_time:
            now = datetime.now(timezone)

            if isinstance(_after_time, datetime):
                if _after_time < now:
                    return self.translations.Reminder.dont_have_time_machine()
                remaining = _after_time - now
            else:
                if _after_time < timedelta(0):
                    return self.translations.Reminder.dont_have_time_machine()
                remaining = _after_time

            if remaining < timedelta(seconds=59):
                return self.translations.Reminder.minimum_time()

            after_precise = humanize.precisedelta(remaining.total_seconds(), format=f"%0.{2}f")

        async with in_transaction():
            for u in all_users:
                remind = await Reminder.create(
                    from_user=ctx.user,
                    to_user=u,
                    content=content,
                    scheduled_for=((scheduled_for_original or scheduled_for) if tl.result.success else None),
                    for_after=_after_time if after and _after_time else None,
                )

                created_reminders.append(remind)

        await self._cache_pending_reminders(created_reminders, all_users)

        remind_id = ",".join([str(remind.id) for remind in created_reminders])

        if after and tl.result.success and _after_time:
            if isinstance(_after_time, timedelta):
                after_str = humanize.precisedelta(_after_time.total_seconds(), format=f"%0.{2}f")
            else:
                after_str = _after_time.strftime(self.translations.SupportTools.TimeTools.strftime())

            wait_delta = tl.result.delta or timedelta(0)
            wait_precise = humanize.precisedelta(wait_delta.total_seconds(), format=f"%0.{2}f")

            return self.translations.Reminder.remind_after_in(
                mention, scheduled_for_precise, wait_precise, after_str, is_self, remind_id
            )

        if after and _after_time:
            return self.translations.Reminder.remind_after(mention, after_precise or "", is_self, remind_id)

        if tl.result.success:
            return self.translations.Reminder.remind_timed(mention, scheduled_for_precise, is_self, remind_id)

        return self.translations.Reminder.remind(mention, is_self, remind_id)

    def find_time(self, content: str) -> tuple[str, Match[str] | None]:
        match_dict = {}
        patterns = [
            self.translations.SupportTools.TimeTools.Humanize().generate_time_regex(),
            self.translations.SupportTools.TimeTools.Humanize("en").generate_time_regex(),
        ]

        to_remove = None

        for pattern in patterns:
            for match in pattern.finditer(content):
                for k, v in match.groupdict().items():
                    if v:
                        match_dict[k] = int(v)
            if not to_remove:
                m = pattern.match(content)
                if m and any(m.groups()):
                    to_remove = m

        return content, to_remove

    @routine(
        delta=timedelta(seconds=30),
        wait_first=True,
        wait_remainder=True,
    )
    async def routine(self) -> None:
        now = datetime.now(UTC)
        threshold = now + timedelta(seconds=30)

        filters = (
            Q(scheduled_for__not_isnull=True)
            & Q(scheduled_for__lte=threshold)
            & Q(sent=False)
            & (Q(for_after__isnull=True) | Q(for_after__lte=now))
        )

        if self.in_flight_reminders:
            filters &= Q(id__not_in=self.in_flight_reminders)

        reminds = await Reminder.filter(filters).select_related("from_user", "to_user").order_by("scheduled_for")

        if not reminds:
            return

        for remind in reminds:
            self.in_flight_reminders.add(remind.id)
            asyncio.create_task(self.dispatch_reminder(self.bot, remind))

    def _build_dispatch_text(self, remind: Reminder) -> str:
        """Build the text of a reminder, used both by the routine and by the on message delivery."""
        to_user = remind.to_user
        from_user = remind.from_user

        created_at = remind.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)

        elapsed_seconds = (datetime.now(UTC) - created_at).total_seconds()
        time_diff = self.translations.SupportTools.TimeTools.Humanize(to_user.language or "pt").precisedelta(
            elapsed_seconds, format="%0.0f"
        )

        # mention(author, target) returns the mention of the target, or "you" when both are the same person
        mention = self.translations.SupportTools.LanguageContext.mention(to_user.name, from_user.name)
        target_name = to_user.nickname or to_user.name

        if remind.content:
            return self.translations.Reminder.dispatched_message(
                target=target_name,
                mention=mention,
                content=remind.content,
                time_diff=time_diff,
            )
        return self.translations.Reminder.dispatched_blank_message(
            target=target_name,
            mention=mention,
            time_diff=time_diff,
        )

    async def dispatch_reminder(self, bot: Gorenmu, remind: Reminder) -> None:
        try:
            now = datetime.now(UTC)
            target = remind.scheduled_for
            if target.tzinfo is None:
                target = target.replace(tzinfo=UTC)

            delta = (target - now).total_seconds()
            if delta > 0:
                await asyncio.sleep(delta)

            channel_name = getattr(remind.to_user, "channel", None) or remind.to_user.name
            chan_cfg = bot.channels.get_channel_by_name(channel_name)

            if not chan_cfg or "remind" in chan_cfg.disabled or not chan_cfg.online:
                return

            channel = await bot.fetch_user(login=channel_name)
            if not channel:
                return

            fake_ctx = Context.fake_ctx(
                bot=self.bot,
                user=remind.to_user,
                channel_user=channel,
                channel_name=channel_name,
                content=f"+remind #{remind.id!s}: {remind.content or ''}",
            )
            self.translations.ctx_set(fake_ctx)
            message_text = self._build_dispatch_text(remind)
            try:
                async with self.limiter.throttle(f"irc:mod:remind:{channel_name}"):
                    await channel.send_message(message_text, self.bot.bot_user)
            except Exception as exception:
                fake_ctx._command = self.bot.get_command("remind")  # noqa  # ty: ignore[invalid-assignment]
                fake_ctx.message.text = (
                    f"[Automated Dispatch] Remind #{remind.id!s} -> "
                    f"{remind.to_user.nickname or remind.to_user.name}: {remind.content}"
                )
                await self.bot.CommandHandler.send_bug(fake_ctx, exception)
                return

            remind.sent = True
            await remind.save(update_fields=["sent"])

        finally:
            self.in_flight_reminders.discard(remind.id)

    async def _cache_pending_reminders(self, reminds: list[Reminder], users: set[User]) -> None:
        """Flag the users that will be reminded the next time they type in chat."""
        if not reminds or reminds[0].scheduled_for is not None:
            return
        for user in users:
            await self.bot.memcache.Reminder.set(user)

    async def _sync_cache_flag(self, user: User) -> None:
        """Keep the cache flag in sync with the pending on message reminders of the user."""
        pending = await Reminder.filter(to_user=user, sent=False, scheduled_for__isnull=True).exists()
        if pending:
            await self.bot.memcache.Reminder.set(user)
        else:
            await self.bot.memcache.Reminder.delete(user)

    async def populate_cache(self) -> None:
        """Flag every user that already has a reminder waiting for their next chat message."""
        try:
            reminds = await Reminder.filter(sent=False, scheduled_for__isnull=True).select_related("to_user")
            for remind in reminds:
                await self.bot.memcache.Reminder.set(remind.to_user)
        except Exception as exception:
            self.bot.log.warning(f"Could not populate the reminder cache: {exception}")

    @commands.event_handler("event_message")
    async def on_message(self, ctx: Context) -> Response | None:
        if ctx.chatter.id == str(self.bot.bot_id) or ctx.source_broadcaster is not None:
            return None
        if ctx.broadcaster.name not in self.bot.channels:
            return None

        if not await ctx.is_online():
            return None
        if not await self.bot.CommandHandler.is_enabled(ctx, "remind"):
            return None
        ctx.message.text = ctx.message.text.replace("\U000e0000", "")
        if ctx.command:
            return None

        # Fast path, only the users flagged on the cache reach the database
        if not await self.bot.memcache.Reminder.get(ctx.user.id):
            return None

        now = datetime.now(UTC)

        filters = Q(sent=False) & Q(scheduled_for__isnull=True) & (Q(for_after__isnull=True) | Q(for_after__lte=now))

        reminds: list[Reminder] = (
            await ctx.user.reminder_to.filter(filters).select_related("from_user", "to_user").order_by("created_at")
        )
        if not reminds:
            await self._sync_cache_flag(ctx.user)
            return None

        response_list: list[str] = []
        for remind in reminds:
            if remind.id in self.in_flight_reminders:
                continue
            self.in_flight_reminders.add(remind.id)
            try:
                # Claim the reminder atomically, so two messages in a row do not deliver it twice
                claimed = await Reminder.filter(id=remind.id, sent=False).update(sent=True)
                if not claimed:
                    continue
                response_list.append(self._build_dispatch_text(remind))
            finally:
                self.in_flight_reminders.discard(remind.id)

        await self._sync_cache_flag(ctx.user)

        if not response_list:
            return None

        return Response(ctx=ctx, response_list=response_list)


async def setup(bot: Gorenmu) -> None:
    component = ReminderCmd(bot)
    await bot.add_component(component)
    await component.populate_cache()


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
