import datetime

import pytest
import pytest_asyncio

from bot.cogs.interactive.command.interactive import InteractiveCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return InteractiveCmd(bot=mock_bot)


async def run_decorator_test(interact, mock_context: MockContext, cmd_class_translation, lang, helper, usage):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(cmd_class_translation.deco_usage("+"), expected=usage, strict=True)
    mock_context.Asserter.assert_string(cmd_class_translation.deco_helper("+"), expected=helper, strict=True)


async def run_interactive_test(
    interact, mock_context: MockContext, command_name, lang, content, expected, success=False
):
    await mock_context.prepare_context(lang, interact=interact)
    cmd = getattr(interact, command_name)
    response = await cmd._callback(interact, mock_context, arg=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, strict=True)
    mock_context.Asserter.assert_boolean(response.success, success)


# --- HUG TESTS ---
@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.Hug.decorators)
async def test_hug_decorators(interact, mock_context, lang, helper, usage):
    await run_decorator_test(interact, mock_context, interact.translations.Hug, lang, helper, usage)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Hug.yourself)
async def test_hug_yourself(interact, mock_context: MockContext, lang: str, expected: str):
    await run_interactive_test(interact, mock_context, "hug", lang, "username", expected, False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Hug.bot_nick)
async def test_hug_bot_nick(interact, mock_context: MockContext, lang: str, expected: str):
    await run_interactive_test(interact, mock_context, "hug", lang, "bot_name", expected, True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Hug.another_name)
async def test_hug_another_name(interact, mock_context: MockContext, lang: str, expected: str):
    await run_interactive_test(interact, mock_context, "hug", lang, "another_name", expected, True)


# --- KISS TESTS ---
@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.Kiss.decorators)
async def test_kiss_decorators(interact, mock_context, lang, helper, usage):
    await run_decorator_test(interact, mock_context, interact.translations.Kiss, lang, helper, usage)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Kiss.yourself)
async def test_kiss_yourself(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "kiss", lang, "username", expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Kiss.bot_nick)
async def test_kiss_bot(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "kiss", lang, "bot_name", expected, True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Kiss.another_name)
async def test_kiss_another(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "kiss", lang, "another_name", expected, True)


# --- SHIP TESTS ---
@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.Ship.decorators)
async def test_ship_decorators(interact, mock_context, lang, helper, usage):
    await run_decorator_test(interact, mock_context, interact.translations.Ship, lang, helper, usage)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Ship.yourself)
async def test_ship_yourself(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "ship", lang, "username username", expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Ship.bot_nick)
async def test_ship_bot(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "ship", lang, "bot_name user2", expected, True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Ship.another_name)
async def test_ship_another(interact, mock_context, lang, expected):
    now = datetime.datetime(year=2222, month=11, day=11)
    async with mock_context.MockBuilder.Default.Datetime.now(now):
        await run_interactive_test(interact, mock_context, "ship", lang, "another_name user2", expected, True)


# --- PAT TESTS ---
@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.Pat.decorators)
async def test_pat_decorators(interact, mock_context, lang, helper, usage):
    await run_decorator_test(interact, mock_context, interact.translations.Pat, lang, helper, usage)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Pat.yourself)
async def test_pat_yourself(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "pat", lang, "username", expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Pat.bot_nick)
async def test_pat_bot(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "pat", lang, "bot_name", expected, True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Pat.another_name)
async def test_pat_another(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "pat", lang, "another_name", expected, True)


# --- PENIS TESTS ---
@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.Penis.decorators)
async def test_penis_decorators(interact, mock_context, lang, helper, usage):
    await run_decorator_test(interact, mock_context, interact.translations.Penis, lang, helper, usage)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Penis.yourself)
async def test_penis_yourself(interact, mock_context, lang, expected):
    now = datetime.datetime(year=2222, month=11, day=11)
    async with mock_context.MockBuilder.Default.Datetime.now(now):
        await run_interactive_test(interact, mock_context, "penis", lang, "username", expected, True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Penis.bot_nick)
async def test_penis_bot(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "penis", lang, "bot_name", expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Penis.another_name)
async def test_penis_another(interact, mock_context, lang, expected):
    now = datetime.datetime(year=2222, month=11, day=11)
    async with mock_context.MockBuilder.Default.Datetime.now(now):
        await run_interactive_test(interact, mock_context, "penis", lang, "another_name", expected, True)


# --- SLAP TESTS ---
@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.Slap.decorators)
async def test_slap_decorators(interact, mock_context, lang, helper, usage):
    await run_decorator_test(interact, mock_context, interact.translations.Slap, lang, helper, usage)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Slap.yourself)
async def test_slap_yourself(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "slap", lang, "username", expected, True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Slap.bot_nick)
async def test_slap_bot(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "slap", lang, "bot_name", expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Slap.another_name)
async def test_slap_another(interact, mock_context, lang, expected):
    now = datetime.datetime(year=2222, month=11, day=11)
    async with mock_context.MockBuilder.Default.Datetime.now(now):
        await run_interactive_test(interact, mock_context, "slap", lang, "another_name", expected, True)


# --- TUCK TESTS ---
@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.Tuck.decorators)
async def test_tuck_decorators(interact, mock_context, lang, helper, usage):
    await run_decorator_test(interact, mock_context, interact.translations.Tuck, lang, helper, usage)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Tuck.yourself)
async def test_tuck_yourself(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "tuck", lang, "username", expected, True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Tuck.bot_nick)
async def test_tuck_bot(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "tuck", lang, "bot_name", expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.Tuck.another_name)
async def test_tuck_another(interact, mock_context, lang, expected):
    await run_interactive_test(interact, mock_context, "tuck", lang, "another_name", expected, True)
