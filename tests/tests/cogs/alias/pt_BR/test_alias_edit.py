# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.alias.templates import test_alias_edit as templates

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_no_content(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected='Nenhum alias ou nome de comando fornecido!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_wrong_name_no_command(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_alias"],
        expected='Nenhum alias ou nome de comando fornecido!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_wrong_name_wrong_command(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=["Wrong_alias", "chance"],
        expected='Você não tem o alias "Wrong_alias"!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_name_wrong_command(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias", "blablablablablablablablablablablabla"],
        expected='Não é possível editar o alias! O comando "blablablablablablablablablablablabla" não existe.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_alias_link_wrong_command(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang, special_user=True,
        content=["The_Link_alias", "chance"],
        expected='Você não pode editar links para outros aliases!'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_guard_caught(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias", "restart"],
        expected='Você não está autorizado a usar o comando "restart" motivo: "DevRequired". '
                 'Se achar que isso é um erro, entre em contato com @dev_name.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_describe_success(interact, mock_context: MockContext):
    await templates.test_edit(
        interact,
        mock_context,
        lang=lang,
        content=["The_Tests_alias", "chance"],
        expected='Seu alias "The_Tests_alias" foi editado com sucesso.'
    )

























