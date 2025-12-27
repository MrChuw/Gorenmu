import datetime

import pytest
import pytest_asyncio

from bot.cogs.weather.command.weather import WeatherCmd
from tests.helpers.mock_classes import MockContext

from .fake_data import forecast, geocoding
from .test_params import Params

DATE = datetime.datetime(2020, 12, 25, 10, 5, 55, tzinfo=datetime.UTC)


@pytest_asyncio.fixture
async def interact(mock_bot):
    return WeatherCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Weather.deco_usage(mock_context, "+"), usage, strict=True)
    mock_context.Asserter.assert_string(
        interact.translations.Weather.deco_helper(mock_context, "+"), helper, strict=True
    )


async def base_weather(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.weather._callback(interact, mock_context, location=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected=expected, re_expected=re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.location)
async def test_location(interact, mock_context: MockContext, lang: str, expected: str):
    async with (
        mock_context.MockBuilder.Apis.OpenMeteo.geocoding(geocoding)
        .Apis.OpenMeteo.forecast(forecast)
        .Default.Datetime.now(DATE)
    ):
        await base_weather(
            interact,
            mock_context,
            lang=lang,
            content="fortaleza, ceara",
            expected=expected,
            success=True,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_city)
async def test_no_city(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Apis.OpenMeteo.geocoding([]).Apis.OpenMeteo.forecast({}):
        await base_weather(
            interact,
            mock_context,
            lang=lang,
            content="fortaleza, ceara",
            expected=expected,
            success=False,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_forecast)
async def test_no_forecast(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Apis.OpenMeteo.geocoding(geocoding).Apis.OpenMeteo.forecast({}):
        await base_weather(
            interact,
            mock_context,
            lang=lang,
            content="fortaleza, ceara",
            expected=expected,
            success=False,
        )
