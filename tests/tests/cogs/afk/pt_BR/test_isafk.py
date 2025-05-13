# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.afk.commands.isafk import IsAfkCmd
from tests.tests.cogs.afk.templates import templates_isafk as templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return IsAfkCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_isafk_own_user(interact, mock_context: MockContext):
    await templates.test_isafk(
        interact, mock_context, lang=lang, content="username", expected="você não está afk... obviamente."
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_isafk_bot_nick(interact, mock_context: MockContext):
    await templates.test_isafk(
        interact, mock_context, lang=lang, content="bot_name", expected="Estou sempre aqui... assistindo."
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_isafk_no_content(interact, mock_context: MockContext):
    await templates.test_isafk(
        interact, mock_context, lang=lang, content="status_user_50", expected="@status_user_50 está ausente 🏃⌨"
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_isafk_content(interact, mock_context: MockContext):
    await templates.test_isafk(
        interact,
        mock_context,
        lang=lang,
        content="status_user_51",
        expected="@status_user_51 está ausente 🏃⌨ e deixou uma nota: content",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_isafk_user_dont_exist(interact, mock_context: MockContext):
    await templates.test_isafk(
        interact,
        mock_context,
        lang=lang,
        content="not_user_1234",
        expected="Não me lembro de ter visto nenhum @not_user_1234.",
    )
