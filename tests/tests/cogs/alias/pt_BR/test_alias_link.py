# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_link as templates

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_link_no_content(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected='Você não forneceu um nome de usuário ou alias! Use: +alias link (usuário) (nome do alias)'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_link_alias_conflict(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_username", "The_Tests_alias"],
        expected='Não é possível adicionar o alias "The_Tests_alias" - você já possui um! '
                 'Você pode “editar” sua definição, “renomear” ou “removê-la”.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_link_alias_name_conflict(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_username", "The_Tests_alias", "The_Tests_alias"],
        expected='Não é possível vincular um novo alias - você já possui um alias com esse nome!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_link_wrong_username(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_username", "."],
        expected='Não consegui encontrar nenhum usuário chamado @Wrong_username.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_link_user_no_alias(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "The_Alias_"],
        expected='O usuário fornecido não possui o alias "The_Alias_"!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_link_user_link_to_link(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "The_Alias_link_link"],
        expected='Você tentou criar um link a partir de um alias link '
                 '(alias The_Alias_link_link por The_Tests_user), '
                 'então usei o original como modelo. Quando o original mudar, o seu também mudará.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_link_user_link_to_link_custom_name(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Tests_user", "The_Alias_link_link", "Custom_Name"],
        expected='Você tentou criar um link a partir de um alias link '
                 '(alias The_Alias_link_link por The_Tests_user), então usei o original como modelo, '
                 'com um nome personalizado de "Custom_Name". Quando o original mudar, o seu também mudará.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_link_user_alias_success(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=["some_user_45", "The_Tests_alias45"],
        expected='Alias vinculado com sucesso. Quando o original for alterado, o seu também será.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_link_user_alias_custom_name_success(interact, mock_context: MockContext):
    await templates.test_link(
        interact,
        mock_context,
        lang=lang,
        content=["some_user_45", "The_Tests_alias45", "Custom_Name"],
        expected='Alias vinculado com sucesso, com um nome personalizado de "Custom_Name". '
                 'Quando o original for alterado, o seu também será.'
    )

























