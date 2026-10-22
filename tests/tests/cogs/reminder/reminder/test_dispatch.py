from __future__ import annotations

import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from bot.cogs.reminder.command.reminder import ReminderCmd
from bot.models import Reminder as ReminderModel
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ReminderCmd(bot=mock_bot)


@pytest.mark.asyncio
async def test_routine_delivers_the_scheduled_reminder(interact, mock_context: MockContext):
    await mock_context.prepare_context("en", interact=interact)
    mock_context.user.language = "en"
    await mock_context.user.save()

    remind: ReminderModel = await ReminderModel.create(
        from_user=mock_context.user,
        to_user=mock_context.user,
        content="buy milk",
        scheduled_for=datetime.datetime.now(datetime.UTC) - datetime.timedelta(seconds=1),
        for_after=None,
    )

    channel = MagicMock()
    channel.send_message = AsyncMock()
    mock_context.bot.fetch_user = AsyncMock(return_value=channel)

    await interact.dispatch_reminder(mock_context.bot, remind)

    channel.send_message.assert_awaited_once()
    message = channel.send_message.await_args.args[0]
    assert "buy milk" in message
    assert "left a reminder" in message
    assert remind.sent is True


@pytest.mark.asyncio
async def test_routine_keeps_the_reminder_when_the_channel_is_offline(interact, mock_context: MockContext):
    await mock_context.prepare_context("en", interact=interact)

    remind: ReminderModel = await ReminderModel.create(
        from_user=mock_context.user,
        to_user=mock_context.user,
        content="buy milk",
        scheduled_for=datetime.datetime.now(datetime.UTC) - datetime.timedelta(seconds=1),
        for_after=None,
    )

    channel = MagicMock()
    channel.send_message = AsyncMock()
    mock_context.bot.fetch_user = AsyncMock(return_value=channel)
    mock_context.bot.channels.get_channel_by_name("channelname").online = False

    await interact.dispatch_reminder(mock_context.bot, remind)

    channel.send_message.assert_not_awaited()
    assert remind.sent is False


@pytest.mark.asyncio
async def test_populate_cache_flags_the_users_with_a_pending_reminder(interact, mock_context: MockContext):
    await mock_context.prepare_context("en", interact=interact)

    await ReminderModel.create(
        from_user=mock_context.user,
        to_user=mock_context.user,
        content="buy milk",
        scheduled_for=None,
        for_after=None,
    )

    await interact.populate_cache()

    assert await mock_context.bot.memcache.Reminder.get(mock_context.user.id) is True


@pytest.mark.asyncio
async def test_populate_cache_ignores_the_scheduled_reminders(interact, mock_context: MockContext):
    await mock_context.prepare_context("en", interact=interact)

    await ReminderModel.create(
        from_user=mock_context.user,
        to_user=mock_context.user,
        content="buy milk",
        scheduled_for=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5),
        for_after=None,
    )

    await interact.populate_cache()

    assert await mock_context.bot.memcache.Reminder.get(mock_context.user.id) is None
