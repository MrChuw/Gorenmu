# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest

from bot.translations import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.check.test_params import Params


async def alias_check(
    interact, mock_context: MockContext, lang: str, content: list[str], expected: str, special_user: bool = False
):
    await mock_context.prepare_context(lang)
    await mock_context.prepare_alias(special_user)
    with (
        patch("bot.utils.UploadThings.upload_alias", return_value="https://alias.mrchuw.com.br/812d49c5415f474b"),
        patch("bot.utils.UploadThings.shortener", return_value="https://shlink.mrchuw.com.br/uQqt5"),
    ):
        response: Response = await interact.check_alias._callback(interact, mock_context, *content)  # NOQA
    assert response.response_string == expected, f"Expected {expected!r}, got: {response.response_string!r}"


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    """if not first_name and not second_name:"""
    await alias_check(interact, mock_context, lang=lang, content=[""], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_match_and_no_second_name)
async def test_no_match_and_no_second_name(interact, mock_context: MockContext, lang: str, expected: str):
    """if not target_aliases_flat and first_name not in aliases_flat and not second_name:"""
    await alias_check(interact, mock_context, lang=lang, content=["some_user_44"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.alias_match_without_second_name)
async def test_match_without_second_name(interact, mock_context: MockContext, lang: str, expected: str):
    """elif not target_aliases_flat and first_name in aliases_flat and not second_name:"""
    await alias_check(interact, mock_context, lang=lang, content=["The_Tests_alias"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.check_user)
async def test_check_user(interact, mock_context: MockContext, lang: str, expected: str):
    """elif target_aliases_flat and first_name not in aliases_flat and not second_name:"""
    await alias_check(interact, mock_context, lang=lang, content=["some_user_45"], expected=expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.special_case)
async def test_special_case(interact, mock_context: MockContext, lang: str, expected: str):
    """elif target_aliases_flat and first_name in aliases_flat and not second_name:"""
    await alias_check(
        interact, mock_context, lang=lang, special_user=True, content=["The_Tests_user"], expected=expected
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.search_alias_on_user)
async def test_search_alias_on_user(interact, mock_context: MockContext, lang: str, expected: str):
    """if second_name:"""
    await alias_check(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Alias_test"],
        expected=expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.search_wrong_alias_on_user)
async def test_search_wrong_alias_on_user(interact, mock_context: MockContext, lang: str, expected: str):
    """if second_name:"""
    await alias_check(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Wrong_Alias_test"],
        expected=expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.search_deleted_alias_on_user)
async def test_search_deleted_alias_on_user(interact, mock_context: MockContext, lang: str, expected: str):
    """if not alias.command and not alias.parent:"""
    await alias_check(
        interact,
        mock_context,
        lang=lang,
        special_user=True,
        content=["The_Tests_user", "The_Deleted_Alias_test"],
        expected=expected,
    )
