# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_link as templates

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_link_no_content(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected="You didn't provide a user or alias name! Use: +alias link (user) (alias name)"
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_link_alias_conflict(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_username", "The_Tests_alias"],
        expected='Cannot add alias "The_Tests_alias" - you already have one! '
                 'You can either "edit" its definition, "rename" it or "remove" it.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_link_alias_name_conflict(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_username", "The_Tests_alias", "The_Tests_alias"],
        expected='Cannot link a new alias - you already have an alias with that name!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_link_wrong_username(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_username", "."],
        expected="I couldn't find any user named @Wrong_username."
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_link_user_no_alias(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "The_Alias_"],
        expected='The provided user does not have the alias "The_Alias_"!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_link_user_link_to_link(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "The_Alias_link_link"],
        expected='You tried to create a link from a linked alias '
                 '(alias The_Alias_link_link by The_Tests_user), '
                 'so I used the original as your template. When the original changes, yours will too.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_link_user_link_to_link_custom_name(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "The_Alias_link_link", "Custom_Name"],
        expected='You tried to create a link from a linked alias '
                 '(alias The_Alias_link_link by The_Tests_user), '
                 'so I used the original as your template, with a custom name of "Custom_Name". '
                 'When the original changes, yours will too.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_link_user_alias_success(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=["some_user_45", "The_Tests_alias45"],
        expected='Alias successfully linked. When the original changes, yours will too.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_link_user_alias_custom_name_success(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=["some_user_45", "The_Tests_alias45", "Custom_Name"],
        expected='Alias successfully linked, with a custom name of "Custom_Name". '
                 'When the original changes, yours will too.'
    )

























