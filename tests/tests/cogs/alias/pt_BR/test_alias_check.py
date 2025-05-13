# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.tests.cogs.alias.templates import test_alias_check as templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_no_content(interact, mock_context: MockContext):
    """if not first_name and not second_name:"""
    await templates.test_alias_check(
        interact,
        mock_context,
        lang=lang,
        content=[""],
        expected="Lista dos seus aliases: The_Tests_alias | Lista detalhada: https://shlink.mrchuw.com.br/uQqt5",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_no_match_and_no_second_name(interact, mock_context: MockContext):
    """if not target_aliases_flat and first_name not in aliases_flat and not second_name:"""
    await templates.test_alias_check(
        interact,
        mock_context,
        lang=lang,
        content=["some_user_44"],
        expected="O usuário some_user_44 não possui aliases registrados.",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_alias_match_without_second_name(interact, mock_context: MockContext):
    """elif not target_aliases_flat and first_name in aliases_flat and not second_name:"""
    await templates.test_alias_check(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias"],
        expected="The_Tests_alias || Invoca: chance  || Link: https://shlink.mrchuw.com.br/uQqt5",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_user(interact, mock_context: MockContext):
    """elif target_aliases_flat and first_name not in aliases_flat and not second_name:"""
    await templates.test_alias_check(
        interact,
        mock_context,
        lang=lang,
        content=["some_user_45"],
        expected="Lista de aliases de @some_user_45: https://shlink.mrchuw.com.br/uQqt5",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_special_case(interact, mock_context: MockContext):
    """elif target_aliases_flat and first_name in aliases_flat and not second_name:"""
    await templates.test_alias_check(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user"],
        expected="Caso especial!\n"
        'Seu alias "The_Tests_user": https://shlink.mrchuw.com.br/uQqt5\n'
        "Lista dos aliases de The_Tests_user: https://shlink.mrchuw.com.br/uQqt5",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_search_alias_on_user(interact, mock_context: MockContext):
    """if second_name:"""
    await templates.test_alias_check(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Alias_test"],
        expected="The_Alias_test || Invoca: chance  || Link: https://shlink.mrchuw.com.br/uQqt5",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_search_wrong_alias_on_user(interact, mock_context: MockContext):
    """if second_name:"""
    await templates.test_alias_check(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Wrong_Alias_test"],
        expected='@The_Tests_user não tem o alias "The_Wrong_Alias_test"!',
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_check_search_deleted_alias_on_user(interact, mock_context: MockContext):
    """if not alias.command and not alias.parent:"""
    await templates.test_alias_check(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Deleted_Alias_test"],
        expected="The_Deleted_Alias_test alias é um link para um alias diferente, mas o original foi excluído.",
    )
