# -*- coding: utf-8 -*-

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.cogs.cookies.templates import templates_cookies_count as templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.mark.asyncio
async def test_count_no_name(interact, mock_context: MockContext):
    await templates.test_count(
        interact,
        mock_context,
        lang=lang,
        content=[],
        expected="você tem 10 em estoque, e tem um total de 2 não resgatados.",
    )


@pytest.mark.asyncio
async def test_count_bot_name(interact, mock_context: MockContext):
    await templates.test_count(
        interact,
        mock_context,
        lang=lang,
        content=[mock_context.bot.bot_nick],
        expected="Tenho cookies infinitos e dou uma fração deles para você.",
    )


@pytest.mark.asyncio
async def test_count_other_user(interact, mock_context: MockContext):
    await templates.test_count_user(
        interact,
        mock_context,
        lang=lang,
        expected="@channelname já comeu já comeu 54 biscoitos 🥠, tem 8534 em estoque, "
        "foi apresentado com 25, presenteou 93, e tem um total de 2 não resgatados.",
        use_target_user=True,
    )


@pytest.mark.asyncio
async def test_count_author_with_a_bunch_of_things(interact, mock_context: MockContext):
    await templates.test_count_user(
        interact,
        mock_context,
        lang=lang,
        expected="você já comeu já comeu 54 biscoitos 🥠, "
        "tem 8534 em estoque, foi apresentado com 25, "
        "presenteou 93, e tem um total de 2 não resgatados.",
        use_target_user=False,
    )


@pytest.mark.asyncio
async def test_count_user_not_found(interact, mock_context: MockContext):
    await templates.test_count(
        interact,
        mock_context,
        lang=lang,
        content=["random_user"],
        expected="o usuário @random_user ainda não foi registrado e não usou nenhum comando de cookie.",
    )
