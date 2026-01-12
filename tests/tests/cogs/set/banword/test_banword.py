import pytest
import pytest_asyncio

from bot.cogs.set.command.set import SetCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return SetCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Banword.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Banword.deco_helper("+"), helper, strict=True)


async def base_banword(
    interact,
    mock_context: MockContext,
    lang: str,
    option: str,
    content: str,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    response = await interact.set_banword._callback(interact, mock_context, action=option, args=content)  # NOQA
    mock_context.Asserter.assert_boolean(response.success, success)
    return response


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.add)
async def test_add(interact, mock_context: MockContext, lang: str, expected: str):
    content = "blablabla, blablablabla. asdfaadsf! pasldfjl?, asldfjpalsdfc"
    response = await base_banword(interact, mock_context, lang=lang, option="add", content=content, success=True)
    words = interact.StringTools.extract_words_simple(content)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    assert words == list(channel.banwords.keys())


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.remove)
async def test_remove(interact, mock_context: MockContext, lang: str, expected: str):
    content = "blablabla, blablablabla. asdfaadsf! pasldfjl?, asldfjpalsdfc"
    await base_banword(interact, mock_context, lang=lang, option="add", content=content, success=True)
    response = await base_banword(interact, mock_context, lang=lang, option="remove", content=content, success=True)
    words = interact.StringTools.extract_words_simple(content)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    assert words != list(channel.banwords.keys())


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.clean)
async def test_clean(interact, mock_context: MockContext, lang: str, expected: str):
    content = "blablabla, blablablabla. asdfaadsf! pasldfjl?, asldfjpalsdfc"
    await base_banword(interact, mock_context, lang=lang, option="add", content=content, success=True)
    response = await base_banword(interact, mock_context, lang=lang, option="clean", content=" ", success=True)
    words = interact.StringTools.extract_words_simple(content)
    mock_context.Asserter.assert_string(response.response_string, expected=expected)
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    assert words != list(channel.banwords.keys())


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.add_remove)
async def test_add_remove(interact, mock_context: MockContext, lang: str, expected: str):
    content = "blablabla, blablablabla. asdfaadsf! pasldfjl?, asldfjpalsdfc"
    response = await base_banword(interact, mock_context, lang=lang, option="None", content=content, success=False)
    words = interact.StringTools.extract_words_simple(content)
    mock_context.Asserter.assert_string(response.response_string, expected=expected, strict=True)
    channel = mock_context.bot.channels[mock_context.channel.name.lower()]
    assert words != list(channel.banwords.keys())


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.what)
# async def test_what(interact, mock_context: MockContext, lang: str, expected: str):
#     await base_banword(
#         interact,
#         mock_context,
#         lang=lang,
#         option="what",
#         content="",
#         expected=expected,
#         success=True
#     )
