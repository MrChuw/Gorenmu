import pytest

from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.set.reminder.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Reminder.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Reminder.deco_helper(mock_context, "+"), helper)


async def base_reminder(
    interact,
    mock_context: MockContext,
    lang: str,
    args: str,
    expected: str,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response = await interact.set_reminder._callback(self=interact, ctx=mock_context, args=args)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected, strict=True)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.enable)
async def test_enable(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_reminder(interact, mock_context, lang, args, expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.disable)
async def test_disable(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_reminder(interact, mock_context, lang, args, expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.invalid)
async def test_invalid(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_reminder(interact, mock_context, lang, args, expected, success=False)
