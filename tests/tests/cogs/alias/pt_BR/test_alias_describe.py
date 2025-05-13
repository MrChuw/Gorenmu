# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_describe as templates

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_no_content(interact, mock_context: MockContext):
    await templates.test_describe(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected="Você não forneceu um alias ou uma descrição! Use: +alias describe (nome) (…descrição)"
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_wrong_alias_no_description(interact, mock_context: MockContext):
    await templates.test_describe(
        interact,
        mock_context,
        lang=lang,
        content=["Some_alias"],
        expected='Você não tem o alias "Some_alias"!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_alias_no_description(interact, mock_context: MockContext):
    await templates.test_describe(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias"],
        expected='A descrição do alias "The_Tests_alias" foi removida com sucesso.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_alias_description(interact, mock_context: MockContext):
    await templates.test_describe(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias", "Some_description"],
        expected='A descrição do alias "The_Tests_alias" foi atualizada com sucesso.'
    )



































