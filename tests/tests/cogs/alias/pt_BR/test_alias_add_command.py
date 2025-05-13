# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.alias.command.alias import AliasCmd
from tests.tests.cogs.alias.templates import test_alias_add_command as templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AliasCmd(bot=mock_bot)



@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_add_command_no_content(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=[""],
            expected='Você não enviou um comando! Use: +alias add (nome) (comando) (…argumentos)'
    )


@pytest.mark.pt_BR
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
                expected='Seu nome de alias não é válido! Seu alias deve conter apenas letras, números '
                         'e ter entre 2-30 caracteres de comprimento.'
        )


@pytest.mark.pt_BR
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
                expected=f'Seu alias "{name}" foi criado com sucesso.'
        )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_add_command_conflict(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=["The_Tests_alias", "chance"],
            expected='Não é possível adicionar o alias "The_Tests_alias" - você já possui um! '
                     'Você pode “editar” sua definição, “renomear” ou “removê-la”.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_add_command_guard_caught(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=["The_Tests", "restart"],
            expected='Você não está autorizado a usar o comando "restart" motivo: '
                     '"DevRequired". Se achar que isso é um erro, entre em contato com @dev_name.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_add_command_success(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=["The_Tests", "choice"],
            expected='Seu alias "The_Tests" foi criado com sucesso.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_add_command_pipe_guard_caught(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=["The_Tests", "choice | restart"],
            expected='Você não está autorizado a usar o comando "restart" motivo: "DevRequired". '
                     'Se achar que isso é um erro, entre em contato com @dev_name.'
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_alias_add_command_pipe_success(interact, mock_context: MockContext):
    await templates.test_alias_add_command(
            interact, mock_context, lang=lang,
            content=["advanced_usage", "choice", "1234", "123456", "|", "count", "{0}"],
            expected='Seu alias "advanced_usage" foi criado com sucesso.'
    )
