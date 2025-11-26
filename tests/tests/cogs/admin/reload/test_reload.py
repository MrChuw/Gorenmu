import pytest

from bot.ext import Response
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.admin.reload.test_params import Params


async def reload_commands(
    interact,
    mock_context: MockContext,
    lang: str,
    command: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
):
    await mock_context.prepare_context(lang)
    response: Response = await interact.reload._callback(self=interact, ctx=mock_context, command=command)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected, re_expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang)
    mock_context.Asserter.assert_string(interact.translations.Reload.deco_usage(mock_context, "+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Reload.deco_helper(mock_context, "+"), helper)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.translations)
async def test_translations(interact, mock_context: MockContext, lang: str, expected: str):
    await reload_commands(
        interact,
        mock_context,
        lang=lang,
        command="translations",
        expected=expected,
        success=True,
    )


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.emotes)
# async def test_emotes(interact, mock_context: MockContext, lang: str, expected: str):
#     await reload_commands(interact, mock_context, lang=lang, command="emotes", expected=expected, success=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.commands)
async def test_commands(interact, mock_context: MockContext, lang: str, expected: str):
    await reload_commands(
        interact,
        mock_context,
        lang=lang,
        command="commands",
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.all)
async def test_all(interact, mock_context: MockContext, lang: str, expected: str):
    await reload_commands(
        interact,
        mock_context,
        lang=lang,
        command="all",
        expected=expected,
        success=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.error_translations)
async def test_error_translations(interact, mock_context: MockContext, lang: str, expected: str):
    async with mock_context.MockBuilder.Errors.import_module(ImportError("Error")):
        await reload_commands(
            interact,
            mock_context,
            lang=lang,
            command="translations",
            expected=expected,
            success=False,
        )


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.error_emotes)
# async def test_error_emotes(interact, mock_context: MockContext, lang: str, expected: str):
#     async with mock_context.MockBuilder.Errors.import_module(ImportError("Error")):
#         await reload_commands(interact, mock_context, lang=lang, command="emotes", expected=expected, success=False)
