# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_copy as templates

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_copy_no_content(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang,
        content=[""],
        expected="Nenhum usuário alvo fornecido!"
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_copy_user_no_alias(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_user"],
        expected='Nenhum alias de destino fornecido!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_copy_user_invalid_alias(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_user", "Invalid_alias#"],
        expected='O nome do alias copiado não é válido e portanto não pode ser copiado!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_copy_user_alias_conflict(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_user", "The_Tests_alias"],
        expected='Não é possível adicionar o alias "The_Tests_alias" - você já possui um! '
                 'Você pode “editar” sua definição, “renomear” ou “removê-la”.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_copy_user_not_found(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_ser", "Invalid_alias"],
        expected='Não consegui encontrar nenhum usuário chamado @The_Tests_ser.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_copy_user_alias_not_found(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "Invalid_alias"],
        expected='Não consegui encontrar Invalid_alias no usuário The_Tests_user!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_copy_user_alias_link(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "The_Alias_link"],
        expected='Você não pode copiar links para outros aliases. '
                 'Em vez disso, use +alias copy The_Tests_user The_Alias_test'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_copy_user_alias_success(interact, mock_context: MockContext):
    await templates.test_copy(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "The_Alias_test"],
        expected='Alias "The_Alias_test" copiado com sucesso.'
    )


































