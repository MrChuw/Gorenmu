import datetime

import pytest
import pytest_asyncio

from bot.cogs.time.command.time import TimeCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return TimeCmd(bot=mock_bot)


@pytest_asyncio.fixture(autouse=True)
async def fixed_now(mock_context):
    date = datetime.datetime(2020, 12, 25, 17, 5, 55, tzinfo=datetime.UTC)
    async with mock_context.MockBuilder.Default.Datetime.now(date):
        yield


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Time.deco_usage(mock_context, "+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Time.deco_helper(mock_context, "+"), helper, strict=True)


async def base_time(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    unit, args = content.split(" ", 1)
    response = await interact.time._callback(interact, mock_context, unit, args=args)  # NOQA
    mock_context.Asserter.assert_string(
        response.response_string, expected=expected, re_expected=re_expected, strict=True
    )
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected, content", Params.time_dates)
async def test_time_dates(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
    unit = {"en": "time", "pt_br": "tempo"}.get(lang.lower())
    await base_time(interact, mock_context, lang=lang, content=f"{unit} {content}", expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected, content", Params.time)
async def test_time(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
    unit = {"en": "time", "pt_br": "tempo"}.get(lang.lower())
    await base_time(interact, mock_context, lang=lang, content=f"{unit} {content}", expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_date)
async def test_only_date(interact, mock_context: MockContext, lang: str, expected: str):
    unit = {"en": "time", "pt_br": "tempo"}.get(lang.lower())
    await base_time(
        interact, mock_context, lang=lang, content=f"{unit} 12:12:12 3500/06/25", expected=expected, success=True
    )


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.microsecond)
# async def test_time_microsecond(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.millisecond)
# async def test_millisecond(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.second)
# async def test_second(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.minute)
# async def test_minute(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.hour)
# async def test_hour(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.day)
# async def test_day(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.week)
# async def test_week(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)
#

# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.month)
# async def test_month(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.year)
# async def test_year(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.decade)
# async def test_decade(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected, content", Params.century)
# async def test_century(interact, mock_context: MockContext, lang: str, expected: str, content: str) -> None:
#     await base_time(interact, mock_context, lang=lang, content=content, expected=expected, success=True)
