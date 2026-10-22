from __future__ import annotations

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


async def base_reminder(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
    invoke: str = "remind",
) -> Response:
    await mock_context.prepare_context(lang, interact=interact)
    # The mock context keeps the language in memory only, the reminders read it from the database
    mock_context.user.language = lang
    await mock_context.user.save()
    mock_context.invoke_by = invoke
    mock_context.content = f"+{invoke} {content}"
    mock_context.message.text = f"+{invoke} {content}"
    response: Response = await interact.reminder._callback(interact, mock_context, content=content)  # NOQA
    if expected is not None or re_expected is not None:
        mock_context.Asserter.assert_string(response.response, expected=expected, re_expected=re_expected, strict=True)
    mock_context.Asserter.assert_boolean(response.success, success)
    return response


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Reminder.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Reminder.deco_helper("+"), helper, strict=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_reminder(interact, mock_context, lang=lang, content="", expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.user_not_found)
async def test_user_not_found(interact, mock_context: MockContext, lang: str, expected: str):
    await base_reminder(interact, mock_context, lang=lang, content="buy milk", expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.remind_me)
async def test_remind_me(interact, mock_context: MockContext, lang: str, expected: str):
    await base_reminder(
        interact, mock_context, lang=lang, content="buy milk", expected=expected, success=True, invoke="remindme"
    )

    remind: ReminderModel = await ReminderModel.filter().select_related("from_user", "to_user").first()
    assert remind is not None
    assert remind.content == "buy milk"
    assert remind.scheduled_for is None
    assert remind.for_after is None
    assert remind.sent is False
    assert remind.to_user.name == "username"
    assert remind.from_user.name == "username"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", ["en", "pt_BR"])
async def test_remind_me_flags_the_cache(interact, mock_context: MockContext, lang: str):
    await base_reminder(
        interact, mock_context, lang=lang, content="buy milk", expected=None, success=True, invoke="remindme"
    )

    flagged = await mock_context.bot.memcache.Reminder.get(mock_context.user.id)
    assert flagged is True


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", ["en", "pt_BR"])
async def test_remind_in_time(interact, mock_context: MockContext, lang: str):
    await base_reminder(
        interact, mock_context, lang=lang, content="in 5m buy milk", expected=None, success=True, invoke="remindme"
    )

    remind: ReminderModel = await ReminderModel.filter().select_related("from_user", "to_user").first()
    assert remind is not None
    assert remind.content == "buy milk"
    assert remind.scheduled_for is not None
    assert remind.for_after is None
    assert remind.sent is False

    # A reminder with a schedule is delivered by the routine, so the user is not flagged
    flagged = await mock_context.bot.memcache.Reminder.get(mock_context.user.id)
    assert flagged is None


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", ["en", "pt_BR"])
async def test_remind_to_another_user(interact, mock_context: MockContext, lang: str):
    await base_reminder(interact, mock_context, lang=lang, content="some_user_1 buy milk", expected=None, success=True)

    remind: ReminderModel = await ReminderModel.filter().select_related("from_user", "to_user").first()
    assert remind is not None
    assert remind.to_user.name == "some_user_1"
    assert remind.from_user.name == "username"

    # The flag belongs to the user that will be reminded
    assert await mock_context.bot.memcache.Reminder.get(mock_context.user.id) is None
    assert await mock_context.bot.memcache.Reminder.get_by_name("some_user_1") is True
