# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_edit as templates

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_no_content(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected='No alias or command name provided!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_wrong_name_no_command(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_alias"],
        expected='No alias or command name provided!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_wrong_name_wrong_command(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_alias", "chance"],
        expected='You don\'t have the "Wrong_alias" alias!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_name_wrong_command(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias", "blablablablablablablablablablablabla"],
        expected='Cannot edit alias! The command "blablablablablablablablablablablabla" does not exist.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_alias_link_wrong_command(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Link_alias", "chance"],
        expected='You cannot edit links to other aliases!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_guard_caught(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias", "restart"],
        expected='You are not authorized to use the "restart" command due to "DevRequired". '
                 'If you think this is an error, contact @dev_name.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_success(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias", "chance"],
        expected='Your alias "The_Tests_alias" has been successfully edited.'
    )

























