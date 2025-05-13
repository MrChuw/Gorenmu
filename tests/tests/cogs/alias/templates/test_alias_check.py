# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from bot.translations import Response
from tests.helpers.mock_classes import MockContext


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.template
@pytest.mark.asyncio
async def test_alias_check(
    interact, mock_context: MockContext, lang: str, content: list[str], expected: str, special_user: bool = False
):
    await mock_context.prepare_context(lang)
    await mock_context.prepare_alias(special_user)
    with (
        patch("bot.utils.UploadThings.upload_alias", return_value="https://alias.mrchuw.com.br/812d49c5415f474b"),
        patch("bot.utils.UploadThings.shortener", return_value="https://shlink.mrchuw.com.br/uQqt5"),
    ):
        response: Response = await interact.check_alias._callback(interact, mock_context, *content)
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"
