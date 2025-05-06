# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.rafk import RAfkCmd
from tests.cogs.afk.templates import templates_rafk as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return RAfkCmd(bot=mock_bot)


@pytest.mark.asyncio
async def test_rafk_not_in_time(interact, mock_context: MockContext):
    await templates.test_rafk_not_in_time(
        interact, mock_context, lang=lang, expected="Time to return AFK has already expired."
    )


@pytest.mark.asyncio
async def test_rafk_with_content(interact, mock_context: MockContext):
    await templates.test_rafk_with_content(
        interact, mock_context, lang=lang, content="content", expected="you continued afk 🏃⌨ and left a note: content"
    )


@pytest.mark.asyncio
async def test_rafk_no_content(interact, mock_context: MockContext):
    await templates.test_rafk_with_content(
        interact, mock_context, lang=lang, content="", expected="you continued afk 🏃⌨"
    )
