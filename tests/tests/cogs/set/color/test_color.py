import pytest

from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.set.color.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Color.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Color.deco_helper(mock_context, "+"), helper)


async def base_color(
    interact,
    mock_context: MockContext,
    lang: str,
    args: str,
    expected: str,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    mock_context.author.color = "#abc123"  # fallback color in case of invalid input
    response = await interact.set_color._callback(self=interact, ctx=mock_context, args=args)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected, strict=True)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.color_set)
async def test_color_set(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_color(interact, mock_context, lang, args, expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.color_set_no_hash)
async def test_color_set_no_hash(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_color(interact, mock_context, lang, args, expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.color_set_short_hex)
async def test_color_set_short_hex(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_color(interact, mock_context, lang, args, expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.color_remove)
async def test_color_remove(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_color(interact, mock_context, lang, args, expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, args, expected", Params.color_invalid)
async def test_color_invalid(interact, mock_context: MockContext, lang: str, args: str, expected: str):
    await base_color(interact, mock_context, lang, args, expected, success=True)
