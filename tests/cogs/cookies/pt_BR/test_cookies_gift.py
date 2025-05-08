# -*- coding: utf-8 -*-

import datetime

import pytest
import pytest_asyncio

from bot.cogs.cookies.command.cookies import CookieCmd
from tests.cogs.cookies.templates import templates_cookies_gift as templates
from tests.helpers.mock_classes import MockContext

lang = "pt_BR"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return CookieCmd(bot=mock_bot)


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_bot(interact, mock_context: MockContext):
    await templates.test_cookie_gift(
        interact, mock_context, lang=lang, content=[mock_context.bot.bot_nick], expected="Não quero a seu cookie."
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_yourself(interact, mock_context: MockContext):
    await templates.test_cookie_gift(
        interact,
        mock_context,
        lang=lang,
        content=[mock_context.author.name],
        expected="você tentou presentear você mesmo, uau!",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_unknown_user(interact, mock_context: MockContext):
    await templates.test_cookie_gift(
        interact,
        mock_context,
        lang=lang,
        content=["random_user"],
        expected="o usuário @random_user ainda não foi registrado e não usou nenhum comando de cookie.",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_other_user_no_cookie(interact, mock_context: MockContext):
    await templates.test_cookie_gift(
        interact,
        mock_context,
        lang=lang,
        content=["channelname"],
        expected="O usuário @channelname ainda não usou nenhum comando relacionado aos cookies.",
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_other_user_zero(interact, mock_context: MockContext):
    await templates.test_cookie_gift_user(
        interact,
        mock_context,
        lang=lang,
        content=["channelname", "0"],
        expected=["Você não deu nada de presente, uau!"],
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_other_user_negative_amount(interact, mock_context: MockContext):
    await templates.test_cookie_gift_user(
        interact,
        mock_context,
        lang=lang,
        content=["channelname", "-1"],
        expected=["Você não pode dar cookies negativos, a menos que seja um ladrão de cookies... e você não é, certo?"],
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_cooldown_no_stock(interact, mock_context: MockContext):
    values = [10, 0, 10, 10, datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)]
    await templates.test_cookie_gift_user_edited(
        interact,
        mock_context,
        lang=lang,
        content=["channelname", "1"],
        expected="Você não tem nenhum cookie 🍪 armazenado ou aguardando para ser resgatado. O próximo chega em 59",
        values=values,
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_other_user_all(interact, mock_context: MockContext):
    await templates.test_cookie_gift_user(
        interact,
        mock_context,
        lang=lang,
        content=["channelname", "all"],
        expected=["você presenteou @channelname com 12 cookie 🎁"],
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_other_user_no_amount(interact, mock_context: MockContext):
    await templates.test_cookie_gift_user(
        interact, mock_context, lang=lang, content=["channelname"], expected=["você deu um cookie para @channelname 🎁"]
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_other_user_exact_amount(interact, mock_context: MockContext):
    await templates.test_cookie_gift_user(
        interact,
        mock_context,
        lang=lang,
        content=["channelname", "10"],
        expected=["você presenteou @channelname com 10 cookie 🎁"],
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_other_user(interact, mock_context: MockContext):
    await templates.test_cookie_gift_user(
        interact, mock_context, lang=lang, content=["channelname"], expected=["você deu um cookie para @channelname 🎁"]
    )


@pytest.mark.pt_BR
@pytest.mark.asyncio
async def test_cookie_gift_other_user_no_stock_cooldown(interact, mock_context: MockContext):
    expected = [
        "você presenteou @channelname com 5 cookie 🎁",
        "você presenteou @channelname com 5 cookie 🎁",
        "Para presentear, você deve primeiro resgatar os 2 cookies que você tem disponíveis.",
    ]
    await templates.test_cookie_gift_user(
        interact, mock_context, lang=lang, content=["channelname", "5"], expected=expected, amount=3
    )
