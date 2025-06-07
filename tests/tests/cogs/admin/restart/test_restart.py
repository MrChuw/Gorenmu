# -*- coding: utf-8 -*-
import os
from unittest.mock import patch

import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.admin.restart.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.success)
async def test_success(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    with patch("os.execv") as mock_execv:
        response: Response = await interact.restart._callback(self=interact, ctx=mock_context)
    mock_execv.assert_called_once(), "Expected os.execv to be called once, but it wasn't"
    called_args = mock_execv.call_args[0]
    exec_path = called_args[0]
    exec_basename = os.path.basename(exec_path)
    assert exec_basename.startswith("python"), f"Expected execv path to be a python executable, got: {exec_path!r}"
    assert exec_path in called_args[1], f"Expected {exec_path!r} to be in args list {called_args[1]!r}"
    assert response is None or (
        isinstance(response, Response) and response.response_string == ""
    ), f"Expected response to be None or empty Response, got: {response!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.failure)
async def test_failure(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    with patch("os.execv", side_effect=OSError("exec failed")):  # NOQA
        response: Response = await interact.restart._callback(self=interact, ctx=mock_context)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
