# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_rename as templates

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_rename_no_content(interact, mock_context: MockContext):
    await templates.test_rename(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected='Você deve fornecer o nome alias atual e o novo!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_rename_no_alias(interact, mock_context: MockContext):
    await templates.test_rename(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_alias_name", "New_alias_name"],
        expected='Você não tem o alias "Wrong_alias_name"!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_rename_alias_conflict(interact, mock_context: MockContext):
    await templates.test_rename(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_alias", "The_Tests_user"],
        expected='Você já tem o alias "The_Tests_user"!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_rename_success(interact, mock_context: MockContext):
    await templates.test_rename(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_alias", "The_new_name"],
        expected='Seu alias "The_Tests_alias" foi renomeado com sucesso para "The_new_name".'
    )




















