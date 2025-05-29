# -*- coding: utf-8 -*-

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

import bot.cogs.randomscp.command.randomscp as randomscp_module
from bot.cogs.randomscp.command.randomscp import RandomSCPCmd, Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.randomscp.randomscp.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RandomSCPCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.two_hundred)
async def test_two_hundred(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    with patch.object(randomscp_module, "get_scp", new_callable=AsyncMock) as mock_get_scp:
        mock_url = MagicMock(human_repr=MagicMock(return_value="www.some_url.com"))
        mock_get_scp.return_value = MagicMock(status=200, url=mock_url)
        response: Response = await interact.randomscp._callback(interact, mock_context)  # NOQA
        mock_context.assert_response(response, expected=expected, re_expected=None)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.timeout)
async def test_timeout(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)

    async def always_404(session):  # NOQA
        mock_resp = MagicMock()
        mock_resp.status = 404
        return mock_resp

    with (
        patch.object(randomscp_module, "get_scp", new_callable=AsyncMock, side_effect=always_404),
        patch("asyncio.sleep", new_callable=AsyncMock),
        patch("asyncio.get_event_loop") as mock_loop,
    ):
        mock_loop.return_value.time.side_effect = [0] + list(range(1, 35))
        response: Response = await interact.randomscp._callback(interact, mock_context)  # NOQA
        mock_context.assert_response(response, expected=expected, re_expected=None)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.exception)  # idem, precisa no seu Params
async def test_unexpected_exception(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    with patch.object(randomscp_module, "get_scp", new_callable=AsyncMock, side_effect=Exception("fail")):
        response: Response = await interact.randomscp._callback(interact, mock_context)  # NOQA
        mock_context.assert_response(response, expected=expected, re_expected=None)
