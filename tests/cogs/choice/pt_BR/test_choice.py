# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.choice.command.choice import ChoiceCmd
from tests.cogs.choice.templates import templates
from tests.helpers.mock_classes import MockContext

tests_lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ChoiceCmd(bot=mock_bot)


@pytest.fixture
def mock_context(mock_bot):
    return MockContext("username", 12345, "channelname", 123456, mock_bot)  # NOQA


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_choice_or(interact, mock_context: MockContext):
    await templates.test_choice(interact, mock_context, lang=tests_lang, content="1 ou 2 ou 3", expected="2")


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_choice_space(interact, mock_context: MockContext):
    await templates.test_choice(interact, mock_context, lang=tests_lang, content="1 2 3", expected="2")


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_choice_comma(interact, mock_context: MockContext):
    await templates.test_choice(interact, mock_context, lang=tests_lang, content="1, 2, 3", expected="2")


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_choice_mixed(interact, mock_context: MockContext):
    await templates.test_choice(interact, mock_context, lang=tests_lang, content="1 ou 2, 3 4", expected="4")
