# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.choice.command.choice import ChoiceCmd
from tests.tests.cogs.choice.templates import templates
from tests.helpers.mock_classes import MockContext

tests_lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ChoiceCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_choice_or(interact, mock_context: MockContext):
    await templates.test_choice(interact, mock_context, lang=tests_lang, content="1 or 2 or 3", expected="2")


@pytest.mark.en
@pytest.mark.asyncio
async def test_choice_space(interact, mock_context: MockContext):
    await templates.test_choice(interact, mock_context, lang=tests_lang, content="1 2 3", expected="2")


@pytest.mark.en
@pytest.mark.asyncio
async def test_choice_comma(interact, mock_context: MockContext):
    await templates.test_choice(interact, mock_context, lang=tests_lang, content="1, 2, 3", expected="2")


@pytest.mark.en
@pytest.mark.asyncio
async def test_choice_mixed(interact, mock_context: MockContext):
    await templates.test_choice(interact, mock_context, lang=tests_lang, content="1 or 2, 3 4", expected="4")
