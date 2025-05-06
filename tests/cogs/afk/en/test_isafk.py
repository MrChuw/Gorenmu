# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.isafk import IsAfkCmd
from tests.cogs.afk.templates import templates_isafk as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return IsAfkCmd(bot=mock_bot)


@pytest.mark.asyncio
async def test_isafk_own_user(interact, mock_context: MockContext):
    await templates.test_isafk(
        interact, mock_context, lang=lang, content="username", expected="you're not afk… obviously."
    )


@pytest.mark.asyncio
async def test_isafk_bot_nick(interact, mock_context: MockContext):
    await templates.test_isafk(
        interact, mock_context, lang=lang, content="bot_name", expected="I'm always here… watching."
    )


@pytest.mark.asyncio
async def test_isafk_no_content(interact, mock_context: MockContext):
    await templates.test_isafk(
        interact, mock_context, lang=lang, content="status_user_50", expected="@status_user_50 it's afk 🏃⌨"
    )


@pytest.mark.asyncio
async def test_isafk_content(interact, mock_context: MockContext):
    await templates.test_isafk(
        interact,
        mock_context,
        lang=lang,
        content="status_user_51",
        expected="@status_user_51 it's afk 🏃⌨ and left a note: content",
    )


@pytest.mark.asyncio
async def test_isafk_user_dont_exist(interact, mock_context: MockContext):
    await templates.test_isafk(
        interact,
        mock_context,
        lang=lang,
        content="not_user_1234",
        expected="I don't remember ever seeing any @not_user_1234.",
    )
