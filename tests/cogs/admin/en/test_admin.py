# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.admin.commands.admin import AdminSmallCmds
from tests.cogs.admin.templates import templates
from tests.helpers.mock_classes import MockContext

tests_lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AdminSmallCmds(bot=mock_bot)


@pytest.mark.asyncio
async def test_nada(interact, mock_context: MockContext):
    await templates.test_nada(
        interact, mock_context, lang=tests_lang, content="", expected="The command was executed successfully."
    )


@pytest.mark.asyncio
async def test_restart_success(interact, mock_context: MockContext):
    await templates.test_restart_success(interact, mock_context, lang=tests_lang)


@pytest.mark.asyncio
async def test_restart_failure(interact, mock_context: MockContext):
    await templates.test_restart_failure(
        interact, mock_context, lang=tests_lang, expected="There was an error restarting the bot: exec failed"
    )


@pytest.mark.asyncio
async def test_reload_translations(interact, mock_context: MockContext):
    await templates.test_reload_commands(
        interact,
        mock_context,
        lang=tests_lang,
        command="translations",
        expected="The translations were successfully reloaded.",
    )


@pytest.mark.asyncio
async def test_reload_emotes(interact, mock_context: MockContext):
    await templates.test_reload_commands(
        interact,
        mock_context,
        lang=tests_lang,
        command="emotes",
        expected='The emotes were successfully reloaded.'
    )


@pytest.mark.asyncio
async def test_reload_all(interact, mock_context: MockContext):
    await templates.test_reload_commands(
        interact, mock_context, lang=tests_lang, command="all", expected="The commands were successfully reloaded."
    )


@pytest.mark.asyncio
async def test_reload_error_translations(interact, mock_context: MockContext):
    await templates.test_reload_importlib_error(
        interact,
        mock_context,
        lang=tests_lang,
        command="translations",
        expected="The translations had an error while reloading: Error",
    )


@pytest.mark.asyncio
async def test_reload_error_emotes(interact, mock_context: MockContext):
    await templates.test_reload_importlib_error(
        interact,
        mock_context,
        lang=tests_lang,
        command="emotes",
        expected='The emotes had an error while reloading: Error'
    )
