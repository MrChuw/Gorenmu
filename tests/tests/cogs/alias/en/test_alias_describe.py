# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_describe as templates

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_no_content(interact, mock_context: MockContext):
    await templates.test_describe(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected="You didn't provide a alias or description! Use: +alias describe (name) (…description)"
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_wrong_alias_no_description(interact, mock_context: MockContext):
    await templates.test_describe(
        interact,
        mock_context,
        lang=lang,
        content=["Some_alias"],
        expected='You don\'t have the "Some_alias" alias!'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_alias_no_description(interact, mock_context: MockContext):
    await templates.test_describe(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias"],
        expected='The description of alias "The_Tests_alias" has been reset successfully.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_describe_alias_description(interact, mock_context: MockContext):
    await templates.test_describe(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias", "Some_description"],
        expected='The description of alias "The_Tests_alias" has been updated successfully.'
    )



































