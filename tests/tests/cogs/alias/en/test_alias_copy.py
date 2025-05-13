# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_copy as templates

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_copy_no_content(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang,
        content=[""],
        expected='No target user provided!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_copy_user_no_alias(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_user"],
        expected='No target alias provided!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_copy_user_invalid_alias(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_user", "Invalid_alias#"],
        expected='The copied alias\'s name is not valid and therefore can\'t be copied!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_copy_user_alias_conflict(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_user", "The_Tests_alias"],
        expected='Cannot add alias "The_Tests_alias" - you already have one! '
                 'You can either "edit" its definition, "rename" it or "remove" it.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_copy_user_not_found(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_ser", "Invalid_alias"],
        expected="I couldn't find any user named @The_Tests_ser."
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_copy_user_alias_not_found(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "Invalid_alias"],
        expected="I couldn't find Invalid_alias in user The_Tests_user!"
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_copy_user_alias_link(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "The_Alias_link"],
        expected='You cannot copy links to other aliases. Instead, use +alias copy The_Tests_user The_Alias_test'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_copy_user_alias_success(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "The_Alias_test"],
        expected='Alias "The_Alias_test" copied successfully.'
    )


































