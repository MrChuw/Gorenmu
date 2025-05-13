# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_rename as templates

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_rename_no_content(interact, mock_context: MockContext):
    await templates.test_rename(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected='You must provide both the current alias name and the new one!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_rename_no_alias(interact, mock_context: MockContext):
    await templates.test_rename(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_alias_name", "New_alias_name"],
        expected='You don\'t have the "Wrong_alias_name" alias!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_rename_alias_conflict(interact, mock_context: MockContext):
    await templates.test_rename(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_alias", "The_Tests_user"],
        expected='You already have the "The_Tests_user" alias!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_rename_success(interact, mock_context: MockContext):
    await templates.test_rename(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_alias", "The_new_name"],
        expected='Your alias "The_Tests_alias" has been successfully renamed to "The_new_name".'
    )




















