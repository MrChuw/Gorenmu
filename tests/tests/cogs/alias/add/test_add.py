# -*- coding: utf-8 -*-

import pytest

from bot.models import Alias
from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.add.test_params import Params


async def alias_add(interact, mock_context: MockContext, lang: str, content: list[str], expected: str):
    await mock_context.prepare_context(lang)
    command_ = mock_context.bot.get_command("chance")
    await Alias.save_alias(mock_context, "The_Tests_alias", command_, "chance", None)
    response: Response = await interact.add_command._callback(interact, mock_context, *content)  # NOQA
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_alias_add_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_add(interact, mock_context, lang=lang, content=[""], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.invalid_name)
async def test_alias_add_invalid_name(interact, mock_context: MockContext, lang: str, expected: str):
    rejected = [
        "my alias",
        "hello!",
        "@user",
        "cool#1",
        "good.name",
        "dollar$ign",
        "per cent%",
        "1*alias",
        "alias(name)",
        "name+123",
        "name\nnext",
        "tab\tname",
        "😄",
        "🤖bot",
    ]

    for name in rejected:
        await alias_add(
            interact, mock_context, lang=lang, content=[name, "chance"], expected=expected.format(name=name)
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.valid_name)
async def test_alias_add_valid_name(interact, mock_context: MockContext, lang: str, expected: str):
    accepted = [
        "alpha",
        "user_123",
        "test-name",
        "©name",
        "®brand",
        "   name",
        "名字",
        "hello你好",
        "1234567890",
        "X_Y-Z",
    ]

    for name in accepted:
        await alias_add(
            interact, mock_context, lang=lang, content=[name, "chance"], expected=expected.format(name=name)
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.conflict)
async def test_alias_add_conflict(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_add(interact, mock_context, lang=lang, content=["The_Tests_alias", "chance"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.guard_caught)
async def test_alias_add_guard_caught(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_add(interact, mock_context, lang=lang, content=["The_Tests", "restart"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.success)
async def test_alias_add_success(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_add(interact, mock_context, lang=lang, content=["The_Tests", "choice"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.pipe_guard_caught)
async def test_alias_add_pipe_guard_caught(interact, mock_context: MockContext, lang: str, expected: str):
    await alias_add(interact, mock_context, lang=lang, content=["The_Tests", "choice | restart"], expected=expected)
