from __future__ import annotations

import datetime
from types import SimpleNamespace

import pytest
import pytest_asyncio

from bot.cogs.reminder.command.reminder import ReminderCmd
from bot.ext import Response
from bot.models import Reminder as ReminderModel
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ReminderCmd(bot=mock_bot)


async def prepare_message(interact, mock_context: MockContext, lang: str) -> None:
    """Prepare a context that looks like a regular chat message."""
    await mock_context.prepare_context(lang, interact=interact)
    # The mock context keeps the language in memory only, the reminders read it from the database
    mock_context.user.language = lang
    await mock_context.user.save()
    mock_context.command = None
    mock_context.source_broadcaster = None
    mock_context.message.source_broadcaster = None
    mock_context.message.text = "Some random chat message"


async def create_reminder(mock_context: MockContext, *, content: str = "buy milk", scheduled_for=None) -> ReminderModel:
    remind: ReminderModel = await ReminderModel.create(
        from_user=mock_context.user,
        to_user=mock_context.user,
        content=content,
        scheduled_for=scheduled_for,
        for_after=None,
    )
    # Pin the creation time so the elapsed time on the message is predictable
    remind.created_at = datetime.datetime.now(datetime.UTC) - datetime.timedelta(seconds=90)
    await remind.save(update_fields=["created_at"])
    await mock_context.bot.memcache.Reminder.set(mock_context.user)
    return remind


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", ["en", "pt_BR"])
async def test_on_message_without_pending_reminder(interact, mock_context: MockContext, lang: str):
    await prepare_message(interact, mock_context, lang)

    response = await interact.on_message(mock_context)
    assert response is None


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.dispatched)
async def test_on_message_delivers_the_pending_reminder(interact, mock_context: MockContext, lang: str, expected: str):
    await prepare_message(interact, mock_context, lang)
    await create_reminder(mock_context)

    response: Response = await interact.on_message(mock_context)
    assert response is not None
    assert len(response.response_list) == 1
    mock_context.Asserter.assert_string(response.response_list[0], re_expected=expected)

    remind: ReminderModel = await ReminderModel.filter().select_related("from_user", "to_user").first()
    assert remind is not None
    assert remind.sent is True

    # The flag is dropped once there is nothing pending anymore
    assert await mock_context.bot.memcache.Reminder.get(mock_context.user.id) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", ["en", "pt_BR"])
async def test_on_message_delivers_only_once(interact, mock_context: MockContext, lang: str):
    await prepare_message(interact, mock_context, lang)
    await create_reminder(mock_context)

    first = await interact.on_message(mock_context)
    assert first is not None

    second = await interact.on_message(mock_context)
    assert second is None


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", ["en", "pt_BR"])
async def test_on_message_ignores_scheduled_reminders(interact, mock_context: MockContext, lang: str):
    await prepare_message(interact, mock_context, lang)
    await create_reminder(mock_context, scheduled_for=datetime.datetime.now(datetime.UTC))

    response = await interact.on_message(mock_context)
    assert response is None

    remind: ReminderModel = await ReminderModel.filter().first()
    assert remind is not None
    assert remind.sent is False


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", ["en", "pt_BR"])
async def test_on_message_ignores_commands(interact, mock_context: MockContext, lang: str):
    await prepare_message(interact, mock_context, lang)
    await create_reminder(mock_context)
    mock_context.command = SimpleNamespace(name="remind")

    response = await interact.on_message(mock_context)
    assert response is None


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", ["en", "pt_BR"])
async def test_on_message_mentions_the_author(interact, mock_context: MockContext, lang: str):
    await prepare_message(interact, mock_context, lang)

    other_context = MockContext("some_user_1", 1, "channelname", 123456, mock_context.bot)
    await prepare_message(interact, other_context, lang)

    await ReminderModel.create(
        from_user=mock_context.user,
        to_user=other_context.user,
        content="buy milk",
        scheduled_for=None,
        for_after=None,
    )
    await mock_context.bot.memcache.Reminder.set(other_context.user)

    response: Response = await interact.on_message(other_context)
    assert response is not None
    assert len(response.response_list) == 1
    assert "@username" in response.response_list[0]
    assert "some_user_1" in response.response_list[0]
