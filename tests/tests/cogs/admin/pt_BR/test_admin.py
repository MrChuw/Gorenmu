# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.admin.commands.admin import AdminSmallCmds
from tests.tests.cogs.admin.templates import templates
from tests.helpers.mock_classes import MockContext

tests_lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AdminSmallCmds(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_nada(interact, mock_context: MockContext):
    await templates.test_nada(
        interact, mock_context, lang=tests_lang, content="", expected="O comando foi executado com sucesso."
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_restart_success(interact, mock_context: MockContext):
    await templates.test_restart_success(interact, mock_context, lang=tests_lang)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_restart_failure(interact, mock_context: MockContext):
    await templates.test_restart_failure(
        interact, mock_context, lang=tests_lang, expected="Um erro aconteceu ao reiniciar o bot: exec failed"
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_reload_translations(interact, mock_context: MockContext):
    await templates.test_reload_commands(
        interact,
        mock_context,
        lang=tests_lang,
        command="translations",
        expected="As traduções foram recarregadas com sucesso.",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_reload_emotes(interact, mock_context: MockContext):
    await templates.test_reload_commands(
        interact,
        mock_context,
        lang=tests_lang,
        command="emotes",
        expected='Os emotes foram recarregadas com sucesso.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_reload_all(interact, mock_context: MockContext):
    await templates.test_reload_commands(
        interact, mock_context, lang=tests_lang, command="all", expected="Os comando foram recarregados com sucesso."
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_reload_error_translations(interact, mock_context: MockContext):
    await templates.test_reload_importlib_error(
        interact,
        mock_context,
        lang=tests_lang,
        command="translations",
        expected="As traduções tiveram um erro ao recarregar: Error",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_reload_error_emotes(interact, mock_context: MockContext):
    await templates.test_reload_importlib_error(
        interact,
        mock_context,
        lang=tests_lang,
        command="emotes",
        expected='Os emotes tiveram um erro ao recarregar: Error'
    )
