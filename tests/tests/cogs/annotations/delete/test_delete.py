import pytest
import pytest_asyncio

from bot.cogs.annotations.command.annotations import AnnotationsCmd
from bot.ext import Response
from bot.models import Annotation
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.annotations.delete.test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AnnotationsCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.Delete.deco_usage("+"), usage)
    mock_context.Asserter.assert_string(interact.translations.Delete.deco_helper("+"), helper)


async def base_annotations_delete(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected,
    amount=0,
    success: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact)
    for value in range(amount):
        content_note = f"a note about something I want to be able to check forever. {value}"
        title = "a" * 32
        await Annotation.create(content=content_note, user=mock_context.user, title=title)
    response: Response = await interact.delete._callback(self=interact, ctx=mock_context, content=content)  # NOQA
    mock_context.Asserter.assert_string(response.response_string, expected)
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.delete_no_id)
async def test_delete_no_id(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_delete(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected=expected,
        amount=2,
        success=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.delete_id)
async def test_delete_id(interact, mock_context: MockContext, lang: str, expected: str):
    await base_annotations_delete(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected=expected,
        amount=2,
        success=True,
    )
