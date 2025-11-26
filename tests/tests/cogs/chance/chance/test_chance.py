import pytest
import pytest_asyncio

from bot.cogs.chance.command.chance import ChanceCmd
from bot.ext import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.chance.chance.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ChanceCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Chance.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Chance.deco_helper(mock_context, "+"), helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.chance)
async def test_chance(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.chance._callback(self=interact, ctx=mock_context)
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, True)
