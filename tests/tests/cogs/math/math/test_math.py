import pytest
import pytest_asyncio

from bot.cogs.math.command.math import MathCmd, Response
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return MathCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Math.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Math.deco_helper("+"), helper, strict=True)


async def base_math(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    response: Response = await interact.math._callback(interact, mock_context, args=content)
    mock_context.Asserter.assert_string(response.response, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.temp)
# async def test_simple_temp(interact, mock_context: MockContext, lang: str, expected: str):
#     await base_math(
#         interact,
#         mock_context,
#         lang=lang,
#         content="factorial(1000)",
#         expected=expected,
#         success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.error)
async def test_error(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Errors.send_bug():
        await base_math(
            interact,
            mock_context,
            lang=lang,
            content="blablabla",
            expected=expected,
            success=False,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.basic_arithmetic)
async def test_basic_arithmetic(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.math_functions)
async def test_math_functions(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.bignumber)
async def test_bignumber(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.stats)
async def test_stats(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.matrix)
async def test_matrix(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content", Params.large_matrices)
async def test_large_matrices(interact, mock_context: MockContext, lang: str, content: str):
    await base_math(
        interact,
        mock_context,
        lang=lang,
        content=content,
        re_expected=r"^\[\[.*\]\]$",
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.complex)
async def test_complex(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.units)
async def test_units(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.combinatorics)
async def test_combinatorics(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.string)
async def test_string(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.user_defined)
async def test_user_defined(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.logic)
async def test_logic(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.range)
async def test_range(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.complex_expressions)
async def test_complex_expressions(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, content, expected", Params.advanced)
async def test_advanced(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await base_math(interact, mock_context, lang=lang, content=content, expected=expected, success=True)
