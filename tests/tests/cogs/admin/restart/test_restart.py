# -*- coding: utf-8 -*-
import os

import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.admin.restart.test_params import Params


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    decorator = mock_context.bot.TranslationManager.get_decorator(interact.restart, mock_context)
    mock_context.Asserter.assert_string(decorator.usage, usage)
    mock_context.Asserter.assert_string(decorator.helper, helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.success)
async def test_success(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    async with mock_context.MockBuilder.Errors.os_execv() as mock_execv:
        response: Response = await interact.restart._callback(self=interact, ctx=mock_context)
    execv = mock_execv.patched.execv
    assert execv.call_count == 1, "Expected os.execv to be called once, but it wasn't"
    called_args = execv.call_args[0]
    exec_path = called_args[0]
    exec_args = called_args[1]
    exec_basename = os.path.basename(exec_path)
    mock_context.Asserter.assert_string(exec_basename, expected="python", strict=False)
    mock_context.Asserter.assert_string(" ".join(exec_args), expected=exec_path, strict=False)
    if response is not None:
        mock_context.Asserter.assert_instance(response, Response)
        mock_context.Asserter.assert_string(response.response_string, expected="", strict=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.failure)
async def test_failure(interact, mock_context: MockContext, lang: str, expected: str):
    await mock_context.prepare_context(lang)
    async with mock_context.MockBuilder.Errors.os_execv(OSError("exec failed")):
        response: Response = await interact.restart._callback(self=interact, ctx=mock_context)
    mock_context.Asserter.assert_string(response.response_string, expected)
