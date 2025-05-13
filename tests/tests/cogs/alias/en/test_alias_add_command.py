# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.tests.cogs.alias.templates import test_alias_add_command as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)



@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_add_command_no_content(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=[""],
            expected="You didn't send a command! Usage: +alias add (name) (command) (…arguments)"
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_add_command_invalid_name(interact, mock_context: MockContext):
    rejected = [
        "my alias",
        "hello!",
        "@user",
        "cool#1",
        "good.name",
        "dollar$ign",
        "per cent%",
        "1*alias",
        "alias(name)",
        "name+123",
        "name\nnext",
        "tab\tname",
        "😄",
        "🤖bot",
    ]

    for name in rejected:
        await templates.test_alias_add_command(
                interact, mock_context, lang=lang,
                content=[name, "chance"],
                expected='Your alias name is not valid! Your alias should only contain letters, '
                         'numbers and be 2-30 characters long.'
        )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_add_command_valid_name(interact, mock_context: MockContext):
    accepted = [
        "alpha",
        "user_123",
        "test-name",
        "©name",
        "®brand",
        "   name",
        "名字",
        "hello你好",
        "1234567890",
        "X_Y-Z",
    ]

    for name in accepted:
        await templates.test_alias_add_command(
                interact, mock_context, lang=lang,
                content=[name, "chance"],
                expected=f'Your alias "{name}" has been created successfully.'
        )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_add_command_conflict(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=["The_Tests_alias", "chance"],
            expected='Cannot add alias "The_Tests_alias" - you already have one! You can either '
                     '"edit" its definition, "rename" it or "remove" it.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_add_command_guard_caught(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=["The_Tests", "restart"],
            expected='You are not authorized to use the "restart" command due to "DevRequired". '
                     'If you think this is an error, contact @dev_name.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_add_command_success(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=["The_Tests", "choice"],
            expected='Your alias "The_Tests" has been created successfully.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_add_command_pipe_guard_caught(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=["The_Tests", "choice | restart"],
            expected='You are not authorized to use the "restart" command due to "DevRequired". '
                     'If you think this is an error, contact @dev_name.'
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_alias_add_command_pipe_success(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=["advanced_usage", "choice", "1234", "123456", "|", "count", "{0}"],
            expected='Your alias "advanced_usage" has been created successfully.'
    )
