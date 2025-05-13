# -*- coding: utf-8 -*-


import pytest
import pytest_asyncio

from bot.cogs.annotations.command.annotations import AnnotationsCmd
from tests.tests.cogs.annotations.templates import templates
from tests.helpers.mock_classes import MockContext

lang = "en"


@pytest_asyncio.fixture
async def interact(mock_bot):
    return AnnotationsCmd(bot=mock_bot)


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations(interact, mock_context: MockContext):
    expected = ["", 1, "Shush"]
    await templates.test_annotations(interact, mock_context, lang=lang, content="", expected=expected)


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_add_no_content(interact, mock_context: MockContext):
    await templates.test_annotations_add(
        interact, mock_context, lang=lang, content="", expected="You need to provide content for this command."
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_add_content_no_title(interact, mock_context: MockContext):
    await templates.test_annotations_add(
        interact,
        mock_context,
        lang=lang,
        content="A note about something I want to be able to check forever.",
        expected="Note successfully created. 📝 (ID: 1)",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_add_content_too_long_no_title(interact, mock_context: MockContext):
    await templates.test_annotations_add(
        interact,
        mock_context,
        lang=lang,
        content="a" * 451,
        expected="The message must have a maximum of 450 characters.",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_add_content_title(interact, mock_context: MockContext):
    await templates.test_annotations_add(
        interact,
        mock_context,
        lang=lang,
        content='title:"title easier to remember" A note about something I want to be able to check forever.',
        expected="Note successfully created. 📝 (ID: 1)",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_add_content_title_too_long(interact, mock_context: MockContext):
    await templates.test_annotations_add(
        interact,
        mock_context,
        lang=lang,
        content='title:"title to make it easier to remember the content" '
        "A note about something I want to be able to check forever.",
        expected="The title must have a maximum of 32 characters.",
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_check_wrong_id(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact, mock_context, lang=lang, content="title", expected="title is not a valid ID."
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_check_no_content_no_annotations(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact, mock_context, lang=lang, content="", expected="You don't have any annotations saved."
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_check_one_annotation(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected="Your annotations are the ones with ID: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1]",
        amount=1,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_check_two_annotation(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact,
        mock_context,
        lang=lang,
        content="",
        expected="Your annotations are the ones with ID: "
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [1], "
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa [2]",
        amount=2,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_check_annotation_id_one(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="a note about something I want to be able to check forever. 0",
        amount=2,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_check_annotation_id_two(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact,
        mock_context,
        lang=lang,
        content="2",
        expected="a note about something I want to be able to check forever. 1",
        amount=2,
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_check_annotation_wrong_id(interact, mock_context: MockContext):
    await templates.test_annotations_check(
        interact, mock_context, lang=lang, content="3", expected="You don't have any annotation with ID 3.", amount=2
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_delete_no_id(interact, mock_context: MockContext):
    await templates.test_annotations_delete(
        interact, mock_context, lang=lang, content="", expected="You need to provide a valid numeric ID.", amount=2
    )


@pytest.mark.en
@pytest.mark.asyncio
async def test_annotations_delete_id(interact, mock_context: MockContext):
    await templates.test_annotations_delete(
        interact,
        mock_context,
        lang=lang,
        content="1",
        expected="Your annotation with ID 1 was successfully deleted. 🗑",
        amount=2,
    )
