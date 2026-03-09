import pytest
import pytest_asyncio

from bot.cogs.pet.command.pet import PetCmd
from tests.helpers.mock_classes import MockContext

from .test_params import Params


@pytest_asyncio.fixture
async def interact(mock_bot):
    return PetCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact, pet_data=True)
    mock_context.Asserter.assert_string(interact.translations.Pet.deco_usage("+"), usage, strict=True)
    mock_context.Asserter.assert_string(interact.translations.Pet.deco_helper("+"), helper, strict=True)


async def base_pet(
    interact,
    mock_context: MockContext,
    lang: str,
    content: str,
    expected: str | None = None,
    re_expected: str | None = None,
    success: bool = False,
    create_pet: bool = False,
):
    await mock_context.prepare_context(lang, interact=interact, pet_data=create_pet)
    response: Response = await interact.pet._callback(interact, mock_context, name="")  # NOQA
    mock_context.Asserter.assert_string(
        response.response_string, expected=expected, re_expected=re_expected, strict=True
    )
    mock_context.Asserter.assert_boolean(response.success, success)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content)
async def test_no_content(interact, mock_context: MockContext, lang: str, expected: str):
    await base_pet(interact, mock_context, lang=lang, content="", expected=expected, success=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.no_content_but_pet)
async def test_no_content_but_pet(interact, mock_context: MockContext, lang: str, expected: str):
    await base_pet(interact, mock_context, lang=lang, content="", expected=expected, success=True, create_pet=True)


# TODO: Need to make the rest of the tests.

# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.no_content)
# async def test_(interact, mock_context: MockContext, lang: str, expected: str):
#     cookie = (await Cookies.get_or_create(user=mock_context.user))[0]
#     await cookie.dev_give(10000)
#     await base_pet(interact, mock_context, lang=lang, content="", expected=expected, success=True)
