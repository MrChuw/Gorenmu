from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Rating(Enum):
    E = "e"
    Q = "q"
    S = "s"


class Status(Enum):
    ACTIVE = "active"


@dataclass
class KonachannetElement:
    id: Optional[int] = None
    tags: Optional[str] = None
    created_at: Optional[int] = None
    creator_id: Optional[int] = None
    author: Optional[str] = None
    change: Optional[int] = None
    source: Optional[str] = None
    score: Optional[int] = None
    md5: Optional[str] = None
    file_size: Optional[int] = None
    file_url: Optional[str] = None
    is_shown_in_index: Optional[bool] = None
    preview_url: Optional[str] = None
    preview_width: Optional[int] = None
    preview_height: Optional[int] = None
    actual_preview_width: Optional[int] = None
    actual_preview_height: Optional[int] = None
    sample_url: Optional[str] = None
    sample_width: Optional[int] = None
    sample_height: Optional[int] = None
    sample_file_size: Optional[int] = None
    jpeg_url: Optional[str] = None
    jpeg_width: Optional[int] = None
    jpeg_height: Optional[int] = None
    jpeg_file_size: Optional[int] = None
    rating: Optional[Rating] = None
    has_children: Optional[bool] = None
    parent_id: Optional[int] = None
    status: Optional[Status] = None
    width: Optional[int] = None
    height: Optional[int] = None
    is_held: Optional[bool] = None
    frames_pending_string: Optional[str] = None
    frames_pending: Optional[List[Any]] = None
    frames_string: Optional[str] = None
    frames: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'KonachannetElement':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        tags = from_union([from_str, from_none], obj.get("tags"))
        created_at = from_union([from_int, from_none], obj.get("created_at"))
        creator_id = from_union([from_int, from_none], obj.get("creator_id"))
        author = from_union([from_str, from_none], obj.get("author"))
        change = from_union([from_int, from_none], obj.get("change"))
        source = from_union([from_str, from_none], obj.get("source"))
        score = from_union([from_int, from_none], obj.get("score"))
        md5 = from_union([from_str, from_none], obj.get("md5"))
        file_size = from_union([from_int, from_none], obj.get("file_size"))
        file_url = from_union([from_str, from_none], obj.get("file_url"))
        is_shown_in_index = from_union([from_bool, from_none], obj.get("is_shown_in_index"))
        preview_url = from_union([from_str, from_none], obj.get("preview_url"))
        preview_width = from_union([from_int, from_none], obj.get("preview_width"))
        preview_height = from_union([from_int, from_none], obj.get("preview_height"))
        actual_preview_width = from_union([from_int, from_none], obj.get("actual_preview_width"))
        actual_preview_height = from_union([from_int, from_none], obj.get("actual_preview_height"))
        sample_url = from_union([from_str, from_none], obj.get("sample_url"))
        sample_width = from_union([from_int, from_none], obj.get("sample_width"))
        sample_height = from_union([from_int, from_none], obj.get("sample_height"))
        sample_file_size = from_union([from_int, from_none], obj.get("sample_file_size"))
        jpeg_url = from_union([from_str, from_none], obj.get("jpeg_url"))
        jpeg_width = from_union([from_int, from_none], obj.get("jpeg_width"))
        jpeg_height = from_union([from_int, from_none], obj.get("jpeg_height"))
        jpeg_file_size = from_union([from_int, from_none], obj.get("jpeg_file_size"))
        rating = from_union([Rating, from_none], obj.get("rating"))
        has_children = from_union([from_bool, from_none], obj.get("has_children"))
        parent_id = from_union([from_int, from_none], obj.get("parent_id"))
        status = from_union([Status, from_none], obj.get("status"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        is_held = from_union([from_bool, from_none], obj.get("is_held"))
        frames_pending_string = from_union([from_str, from_none], obj.get("frames_pending_string"))
        frames_pending = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("frames_pending"))
        frames_string = from_union([from_str, from_none], obj.get("frames_string"))
        frames = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("frames"))
        return KonachannetElement(id, tags, created_at, creator_id, author, change, source, score, md5, file_size, file_url, is_shown_in_index, preview_url, preview_width, preview_height, actual_preview_width, actual_preview_height, sample_url, sample_width, sample_height, sample_file_size, jpeg_url, jpeg_width, jpeg_height, jpeg_file_size, rating, has_children, parent_id, status, width, height, is_held, frames_pending_string, frames_pending, frames_string, frames)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_int, from_none], self.id)
        if self.tags is not None:
            result["tags"] = from_union([from_str, from_none], self.tags)
        if self.created_at is not None:
            result["created_at"] = from_union([from_int, from_none], self.created_at)
        if self.creator_id is not None:
            result["creator_id"] = from_union([from_int, from_none], self.creator_id)
        if self.author is not None:
            result["author"] = from_union([from_str, from_none], self.author)
        if self.change is not None:
            result["change"] = from_union([from_int, from_none], self.change)
        if self.source is not None:
            result["source"] = from_union([from_str, from_none], self.source)
        if self.score is not None:
            result["score"] = from_union([from_int, from_none], self.score)
        if self.md5 is not None:
            result["md5"] = from_union([from_str, from_none], self.md5)
        if self.file_size is not None:
            result["file_size"] = from_union([from_int, from_none], self.file_size)
        if self.file_url is not None:
            result["file_url"] = from_union([from_str, from_none], self.file_url)
        if self.is_shown_in_index is not None:
            result["is_shown_in_index"] = from_union([from_bool, from_none], self.is_shown_in_index)
        if self.preview_url is not None:
            result["preview_url"] = from_union([from_str, from_none], self.preview_url)
        if self.preview_width is not None:
            result["preview_width"] = from_union([from_int, from_none], self.preview_width)
        if self.preview_height is not None:
            result["preview_height"] = from_union([from_int, from_none], self.preview_height)
        if self.actual_preview_width is not None:
            result["actual_preview_width"] = from_union([from_int, from_none], self.actual_preview_width)
        if self.actual_preview_height is not None:
            result["actual_preview_height"] = from_union([from_int, from_none], self.actual_preview_height)
        if self.sample_url is not None:
            result["sample_url"] = from_union([from_str, from_none], self.sample_url)
        if self.sample_width is not None:
            result["sample_width"] = from_union([from_int, from_none], self.sample_width)
        if self.sample_height is not None:
            result["sample_height"] = from_union([from_int, from_none], self.sample_height)
        if self.sample_file_size is not None:
            result["sample_file_size"] = from_union([from_int, from_none], self.sample_file_size)
        if self.jpeg_url is not None:
            result["jpeg_url"] = from_union([from_str, from_none], self.jpeg_url)
        if self.jpeg_width is not None:
            result["jpeg_width"] = from_union([from_int, from_none], self.jpeg_width)
        if self.jpeg_height is not None:
            result["jpeg_height"] = from_union([from_int, from_none], self.jpeg_height)
        if self.jpeg_file_size is not None:
            result["jpeg_file_size"] = from_union([from_int, from_none], self.jpeg_file_size)
        if self.rating is not None:
            result["rating"] = from_union([lambda x: to_enum(Rating, x), from_none], self.rating)
        if self.has_children is not None:
            result["has_children"] = from_union([from_bool, from_none], self.has_children)
        if self.parent_id is not None:
            result["parent_id"] = from_union([from_int, from_none], self.parent_id)
        if self.status is not None:
            result["status"] = from_union([lambda x: to_enum(Status, x), from_none], self.status)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.is_held is not None:
            result["is_held"] = from_union([from_bool, from_none], self.is_held)
        if self.frames_pending_string is not None:
            result["frames_pending_string"] = from_union([from_str, from_none], self.frames_pending_string)
        if self.frames_pending is not None:
            result["frames_pending"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.frames_pending)
        if self.frames_string is not None:
            result["frames_string"] = from_union([from_str, from_none], self.frames_string)
        if self.frames is not None:
            result["frames"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.frames)
        return result


def konachannet_from_dict(s: Any) -> List[KonachannetElement]:
    return from_list(KonachannetElement.from_dict, s)


def konachannet_to_dict(x: List[KonachannetElement]) -> Any:
    return from_list(lambda x: to_class(KonachannetElement, x), x)
