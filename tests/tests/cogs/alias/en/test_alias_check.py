# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.tests.cogs.alias.templates import test_alias_check as templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)



@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_no_content(interact, mock_context: MockContext):
    """if not first_name and not second_name:"""
    await templates.test_alias_check(
            interact, mock_context, lang=lang,
            content=[""],
            expected='List of your aliases: The_Tests_alias | Detailed list: https://shlink.mrchuw.com.br/uQqt5'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_no_match_and_no_second_name(interact, mock_context: MockContext):
    """if not target_aliases_flat and first_name not in aliases_flat and not second_name:"""
    await templates.test_alias_check(
            interact, mock_context, lang=lang,
            content=["some_user_44"],
            expected='User some_user_44 has no registered aliases.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_alias_match_without_second_name(interact, mock_context: MockContext):
    """elif not target_aliases_flat and first_name in aliases_flat and not second_name:"""
    await templates.test_alias_check(
            interact, mock_context, lang=lang,
            content=["The_Tests_alias"],
            expected='The_Tests_alias || Invoke: chance  || Link: https://shlink.mrchuw.com.br/uQqt5'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_user(interact, mock_context: MockContext):
    """elif target_aliases_flat and first_name not in aliases_flat and not second_name:"""
    await templates.test_alias_check(
            interact, mock_context, lang=lang,
            content=["some_user_45"],
            expected='List of @some_user_45 aliases: https://shlink.mrchuw.com.br/uQqt5'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_special_case(interact, mock_context: MockContext):
    """elif target_aliases_flat and first_name in aliases_flat and not second_name:"""
    await templates.test_alias_check(
            interact, mock_context, lang=lang,
            special_user=True,
            content=["The_Tests_user"],
            expected='Special case!\n '
                     'Your alias "The_Tests_user": https://shlink.mrchuw.com.br/uQqt5\n '
                     'List of The_Tests_user\'s aliases: https://shlink.mrchuw.com.br/uQqt5'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_search_alias_on_user(interact, mock_context: MockContext):
    """if second_name:"""
    await templates.test_alias_check(
            interact, mock_context, lang=lang,
            special_user=True,
            content=["The_Tests_user", "The_Alias_test"],
            expected='The_Alias_test || Invoke: chance  || Link: https://shlink.mrchuw.com.br/uQqt5'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_search_wrong_alias_on_user(interact, mock_context: MockContext):
    """if second_name:"""
    await templates.test_alias_check(
            interact, mock_context, lang=lang,
            special_user=True,
            content=["The_Tests_user", "The_Wrong_Alias_test"],
            expected='@The_Tests_user don\'t have the "The_Wrong_Alias_test" alias!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio  # TODO:
async def test_alias_check_search_deleted_alias_on_user(interact, mock_context: MockContext):
    """if not alias.command and not alias.parent:"""
    await templates.test_alias_check(
            interact, mock_context, lang=lang,
            special_user=True,
            content=["The_Tests_user", "The_Deleted_Alias_test"],
            expected='The_Deleted_Alias_test alias is a link to a different alias, but the original has been deleted.'
    )





















