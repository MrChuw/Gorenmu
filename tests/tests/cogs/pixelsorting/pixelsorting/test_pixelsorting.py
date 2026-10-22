from io import BytesIO
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from PIL import Image

from bot.cogs.pixelsorting.command.pixelsorting import PixelSortCmd
from tests.helpers.mock_classes import MockContext
from tests.tests.cogs.pixelsorting.pixelsorting.test_params import Params

PATH = Path(__file__).parent / "images"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return PixelSortCmd(bot=mock_bot)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, helper, usage", Params.decorators)
async def test_decorators(interact, mock_context: MockContext, lang: str, helper: str, usage: str):
    await mock_context.prepare_context(lang, interact=interact)
    mock_context.Asserter.assert_string(interact.translations.PixelSorting.deco_usage("+"), usage)
    mock_context.Asserter.assert_string(interact.translations.PixelSorting.deco_helper("+"), helper)


async def base_pixelsorting(
    interact: PixelSortCmd,
    mock_context: MockContext,
    lang: str,
    content: str,
) -> Any:
    await mock_context.prepare_context(lang, interact=interact)
    image = [Image.open(PATH / "test.jpeg").convert("RGBA")]
    async with mock_context.MockBuilder.Commands.request_images(image):
        response = await interact.pixel_sorting._callback(interact, mock_context, args=content)  # NOQA
    return response


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_normal)
async def test_normal(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(
        interact,
        mock_context,
        lang=lang,
        content="blablabla.com",
    )
    the_expected = get_expected(expected)
    assert response == the_expected


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_red)
async def test_type_red(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:red blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_green)
async def test_type_green(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:green blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_blue)
async def test_type_blue(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:blue blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_rgb)
async def test_type_rgb(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:rgb blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_rgba)
async def test_type_rgba(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:rgba blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_sum)
async def test_type_sum(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:sum blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_hue)
async def test_type_hue(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:hue blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_saturation)
async def test_type_saturation(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:saturation blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_value)
async def test_type_value(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:value blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_lightness)
async def test_type_lightness(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:lightness blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_luma)
async def test_type_luma(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:luma blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_chroma)
async def test_type_chroma(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:chroma blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_dist_white)
async def test_type_dist_white(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:dist_white blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_type_dist_black)
async def test_type_dist_black(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:dist_black blablabla.com")
    assert response == get_expected(expected)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.only_type_random)
# async def test_type_random(interact, mock_context: MockContext, lang: str, expected: str):
#     random.seed(1)
#     response = await base_pixelsorting(interact, mock_context, lang=lang, content="type:random blablabla.com")
#     assert response == get_expected(expected)


# @pytest.mark.asyncio
# @pytest.mark.parametrize("lang, expected", Params.only_rand_true)
# async def test_rand_true(interact, mock_context: MockContext, lang: str, expected: str):
#     random.seed(1)
#     response = await base_pixelsorting(interact, mock_context, lang=lang, content="rand:true blablabla.com")
#     assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_dire_global)
async def test_dire_global(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="dire:global blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_dire_horizontal)
async def test_dire_horizontal(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="dire:horizontal blablabla.com")
    assert response == get_expected(expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, expected", Params.only_dire_vertical)
async def test_dire_vertical(interact, mock_context: MockContext, lang: str, expected: str):
    response = await base_pixelsorting(interact, mock_context, lang=lang, content="dire:vertical blablabla.com")
    assert response == get_expected(expected)


def get_expected(expected: str):
    buffer = BytesIO()
    image = Image.open(PATH / expected)
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()
