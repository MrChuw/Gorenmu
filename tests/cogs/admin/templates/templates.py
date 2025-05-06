# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest
import pytest_asyncio

from bot.cogs.admin.commands.admin import AdminSmallCmds
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AdminSmallCmds(bot=mock_bot)


@pytest.mark.template
@pytest.mark.asyncio
async def test_nada(interact, mock_context: MockContext, lang: str, content: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.nada._callback(self=interact, ctx=mock_context, args=content)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_restart_success(interact, mock_context: MockContext, lang: str):
    await mock_context.prepare_context(lang)
    with patch("os.execv") as mock_execv:
        response: Response = await interact.restart._callback(self=interact, ctx=mock_context)

    mock_execv.assert_called_once(), "Expected os.execv to be called once, but it wasn't"

    called_args = mock_execv.call_args[0]
    assert called_args[0].endswith(
        "bin/python"
    ), f"Expected execv path to end with 'bin/python', got: {called_args[0]!r}"
    assert called_args[0] in called_args[1], f"Expected {called_args[0]!r} to be in args list {called_args[1]!r}"
    assert response is None or (
        isinstance(response, Response) and response.response_string == ""
    ), f"Expected response to be None or empty Response, got: {response!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_restart_failure(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    with patch("os.execv", side_effect=OSError("exec failed")):  # NOQA
        response: Response = await interact.restart._callback(self=interact, ctx=mock_context)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_reload_commands(interact, mock_context: MockContext, lang: str, command: str, expected: str):
    await mock_context.prepare_context(lang)
    response: Response = await interact.reload._callback(self=interact, ctx=mock_context, command=command)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.template
@pytest.mark.asyncio
async def test_reload_importlib_error(interact, mock_context: MockContext, lang: str, command: str, expected: str):
    with patch("importlib.import_module", side_effect=ImportError("Error")):
        await mock_context.prepare_context(lang)
        response: Response = await interact.reload._callback(self=interact, ctx=mock_context, command=command)
        assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
