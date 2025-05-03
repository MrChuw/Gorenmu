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


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest.mark.asyncio
async def test_nada(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.nada._callback(self=interact, ctx=mock_context, args="")
    assert response.response_string == "O comando foi executado com sucesso.", \
        f"Expected success message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_restart_success(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    with patch("os.execv") as mock_execv:  # NOQA
        response: Response = await interact.restart._callback(self=interact, ctx=mock_context)

    mock_execv.assert_called_once(), "Expected os.execv to be called once, but it wasn't"

    called_args = mock_execv.call_args[0]
    assert called_args[0].endswith("bin/python"), (
            f"Expected execv path to end with 'bin/python', got: {called_args[0]!r}"
    )
    assert called_args[0] in called_args[1], (
            f"Expected {called_args[0]!r} to be in args list {called_args[1]!r}"
    )
    assert response is None or (
            isinstance(response, Response) and response.response_string == ""
    ), (
            f"Expected response to be None or empty Response, got: {response!r}"
    )
    mock_context.reset_mock()


@pytest.mark.asyncio
async def test_restart_failure(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    with patch("os.execv", side_effect=OSError("exec failed")):  # NOQA
        response: Response = await interact.restart._callback(self=interact, ctx=mock_context)

    assert response.response_string == "Um erro aconteceu ao reiniciar o bot: exec failed", \
        f"Expected error message, got: {response.response_string!r}"
    mock_context.reset_mock()


@pytest.mark.asyncio
async def test_reload_translations(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.reload._callback(self=interact, ctx=mock_context, command="translations")
    assert response.response_string == 'As traduções foram recarregadas com sucesso.', \
        f"Expected success message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_reload_emotes(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.reload._callback(self=interact, ctx=mock_context, command="emotes")
    assert response.response_string == 'As traduções foram recarregadas com sucesso.', \
        f"Expected success message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_reload_all(interact, mock_context: MockContext):
    await mock_context.prepare_context('pt_BR')
    response: Response = await interact.reload._callback(self=interact, ctx=mock_context, command="all")
    assert response.response_string == 'Os comando foram recarregados com sucesso.', \
        f"Expected success message, got: {response.response_string!r}"
    mock_context.reset_mock()
    del response


@pytest.mark.asyncio
async def test_reload_error_translations(interact, mock_context: MockContext):
    with patch("importlib.import_module", side_effect=ImportError("Error")):
        await mock_context.prepare_context('pt_BR')
        response: Response = await interact.reload._callback(self=interact, ctx=mock_context, command="translations")
        assert response.response_string == 'As traduções tiveram um erro ao recarregar: Error', \
            f"Expected error message, got: {response.response_string!r}"
        mock_context.reset_mock()
        del response


@pytest.mark.asyncio
async def test_reload_error_emotes(interact, mock_context: MockContext):
    with patch("importlib.import_module", side_effect=ImportError("Error")):
        await mock_context.prepare_context('pt_BR')
        response: Response = await interact.reload._callback(self=interact, ctx=mock_context, command="emotes")
        assert response.response_string == 'As traduções tiveram um erro ao recarregar: Error', \
            f"Expected error message, got: {response.response_string!r}"
        mock_context.reset_mock()
        del response
