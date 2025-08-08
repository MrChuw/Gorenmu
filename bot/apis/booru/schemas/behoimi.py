from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, List, Optional, Type, TypeVar, cast

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


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


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Author(Enum):
    KILLERKAIM = "killerkaim"
    NIL = "nil!"
    SUNNILY = "Sunnily"
    UP8 = "UP8"


class JSONClass(Enum):
    TIME = "Time"


@dataclass
class CreatedAt:
    json_class: Optional[JSONClass] = None
    n: Optional[int] = None
    s: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "CreatedAt":
        assert isinstance(obj, dict)
        json_class = from_union([JSONClass, from_none], obj.get("json_class"))
        n = from_union([from_int, from_none], obj.get("n"))
        s = from_union([from_int, from_none], obj.get("s"))
        return CreatedAt(json_class, n, s)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.json_class is not None:
            result["json_class"] = from_union([lambda x: to_enum(JSONClass, x), from_none], self.json_class)
        if self.n is not None:
            result["n"] = from_union([from_int, from_none], self.n)
        if self.s is not None:
            result["s"] = from_union([from_int, from_none], self.s)
        return result


class Rating(Enum):
    E = "e"
    Q = "q"
    S = "s"


class Status(Enum):
    ACTIVE = "active"
    PENDING = "pending"


@dataclass
class BehoimiElement:
    status: Optional[Status] = None
    creator_id: Optional[int] = None
    preview_width: Optional[int] = None
    source: Optional[str] = None
    author: Optional[Author] = None
    width: Optional[int] = None
    score: Optional[int] = None
    preview_height: Optional[int] = None
    has_comments: Optional[bool] = None
    sample_width: Optional[int] = None
    has_children: Optional[bool] = None
    sample_url: Optional[str] = None
    file_url: Optional[str] = None
    parent_id: Optional[str | int] = None
    sample_height: Optional[int] = None
    md5: Optional[str] = None
    tags: Optional[str] = None
    change: Optional[int] = None
    has_notes: Optional[bool] = None
    rating: Optional[Rating] = None
    id: Optional[int] = None
    height: Optional[int] = None
    preview_url: Optional[str] = None
    file_size: Optional[int] = None
    created_at: Optional[CreatedAt] = None

    @staticmethod
    def from_dict(obj: Any) -> "BehoimiElement":
        assert isinstance(obj, dict)
        status = from_union([Status, from_none], obj.get("status"))
        creator_id = from_union([from_int, from_none], obj.get("creator_id"))
        preview_width = from_union([from_int, from_none], obj.get("preview_width"))
        source = from_union([from_str, from_none], obj.get("source"))
        author = from_union([Author, from_none], obj.get("author"))
        width = from_union([from_int, from_none], obj.get("width"))
        score = from_union([from_int, from_none], obj.get("score"))
        preview_height = from_union([from_int, from_none], obj.get("preview_height"))
        has_comments = from_union([from_bool, from_none], obj.get("has_comments"))
        sample_width = from_union([from_int, from_none], obj.get("sample_width"))
        has_children = from_union([from_bool, from_none], obj.get("has_children"))
        sample_url = from_union([from_str, from_none], obj.get("sample_url"))
        file_url = from_union([from_str, from_none], obj.get("file_url"))
        parent_id = from_union([from_int, from_str, from_none], obj.get("parent_id"))
        sample_height = from_union([from_int, from_none], obj.get("sample_height"))
        md5 = from_union([from_str, from_none], obj.get("md5"))
        tags = from_union([from_str, from_none], obj.get("tags"))
        change = from_union([from_int, from_none], obj.get("change"))
        has_notes = from_union([from_bool, from_none], obj.get("has_notes"))
        rating = from_union([Rating, from_none], obj.get("rating"))
        id = from_union([from_int, from_none], obj.get("id"))
        height = from_union([from_int, from_none], obj.get("height"))
        preview_url = from_union([from_str, from_none], obj.get("preview_url"))
        file_size = from_union([from_int, from_none], obj.get("file_size"))
        created_at = from_union([CreatedAt.from_dict, from_none], obj.get("created_at"))
        return BehoimiElement(
            status,
            creator_id,
            preview_width,
            source,
            author,
            width,
            score,
            preview_height,
            has_comments,
            sample_width,
            has_children,
            sample_url,
            file_url,
            parent_id,
            sample_height,
            md5,
            tags,
            change,
            has_notes,
            rating,
            id,
            height,
            preview_url,
            file_size,
            created_at,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.status is not None:
            result["status"] = from_union([lambda x: to_enum(Status, x), from_none], self.status)
        if self.creator_id is not None:
            result["creator_id"] = from_union([from_int, from_none], self.creator_id)
        if self.preview_width is not None:
            result["preview_width"] = from_union([from_int, from_none], self.preview_width)
        if self.source is not None:
            result["source"] = from_union([from_str, from_none], self.source)
        if self.author is not None:
            result["author"] = from_union([lambda x: to_enum(Author, x), from_none], self.author)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.score is not None:
            result["score"] = from_union([from_int, from_none], self.score)
        if self.preview_height is not None:
            result["preview_height"] = from_union([from_int, from_none], self.preview_height)
        if self.has_comments is not None:
            result["has_comments"] = from_union([from_bool, from_none], self.has_comments)
        if self.sample_width is not None:
            result["sample_width"] = from_union([from_int, from_none], self.sample_width)
        if self.has_children is not None:
            result["has_children"] = from_union([from_bool, from_none], self.has_children)
        if self.sample_url is not None:
            result["sample_url"] = from_union([from_str, from_none], self.sample_url)
        if self.file_url is not None:
            result["file_url"] = from_union([from_str, from_none], self.file_url)
        if self.parent_id is not None:
            result["parent_id"] = from_none(self.parent_id)
        if self.sample_height is not None:
            result["sample_height"] = from_union([from_int, from_none], self.sample_height)
        if self.md5 is not None:
            result["md5"] = from_union([from_str, from_none], self.md5)
        if self.tags is not None:
            result["tags"] = from_union([from_str, from_none], self.tags)
        if self.change is not None:
            result["change"] = from_union([from_int, from_none], self.change)
        if self.has_notes is not None:
            result["has_notes"] = from_union([from_bool, from_none], self.has_notes)
        if self.rating is not None:
            result["rating"] = from_union([lambda x: to_enum(Rating, x), from_none], self.rating)
        if self.id is not None:
            result["id"] = from_union([from_int, from_none], self.id)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.preview_url is not None:
            result["preview_url"] = from_union([from_str, from_none], self.preview_url)
        if self.file_size is not None:
            result["file_size"] = from_union([from_int, from_none], self.file_size)
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: to_class(CreatedAt, x), from_none], self.created_at)
        return result


def behoimi_from_dict(s: Any) -> List[BehoimiElement]:
    return from_list(BehoimiElement.from_dict, s)


def behoimi_to_dict(x: List[BehoimiElement]) -> Any:
    return from_list(lambda x: to_class(BehoimiElement, x), x)
