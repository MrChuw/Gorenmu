# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.chance.command.chance import ChanceCmd
from tests.tests.cogs.chance.templates import templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return ChanceCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_choice(interact, mock_context: MockContext):
    await templates.test_choice(interact, mock_context, lang=lang, content="", expected="84.44%")
