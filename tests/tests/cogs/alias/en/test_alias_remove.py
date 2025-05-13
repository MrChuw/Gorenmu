# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_remove as templates

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_remove_no_content(interact, mock_context: MockContext):
    await templates.test_remove(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected='No alias name provided!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_remove_no_alias(interact, mock_context: MockContext):
    await templates.test_remove(
        interact,
        mock_context,
        lang=lang,
        content=["Some_Alias"],
        expected='You don\'t have the "Some_Alias" alias!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_remove_success(interact, mock_context: MockContext):
    await templates.test_remove(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias"],
        expected='Your alias "The_Tests_alias" has been successfully removed.'
    )























