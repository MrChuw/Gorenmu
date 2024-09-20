from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, Callable, cast
from enum import Enum


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


def from_stringified_bool(x: str) -> bool:
    if x == "true":
        return True
    if x == "false":
        return False
    assert False


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Attributes:
    limit: Optional[int] = None
    offset: Optional[int] = None
    count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Attributes':
        assert isinstance(obj, dict)
        limit = from_union([from_int, from_none], obj.get("limit"))
        offset = from_union([from_int, from_none], obj.get("offset"))
        count = from_union([from_int, from_none], obj.get("count"))
        return Attributes(limit, offset, count)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.limit is not None:
            result["limit"] = from_union([from_int, from_none], self.limit)
        if self.offset is not None:
            result["offset"] = from_union([from_int, from_none], self.offset)
        if self.count is not None:
            result["count"] = from_union([from_int, from_none], self.count)
        return result


class Rating(Enum):
    EXPLICIT = "explicit"
    GENERAL = "general"
    QUESTIONABLE = "questionable"
    SENSITIVE = "sensitive"


class Status(Enum):
    ACTIVE = "active"


@dataclass
class Post:
    id: Optional[int] = None
    created_at: Optional[str] = None
    score: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    md5: Optional[str] = None
    directory: Optional[str] = None
    image: Optional[str] = None
    rating: Optional[Rating] = None
    source: Optional[str] = None
    change: Optional[int] = None
    owner: Optional[str] = None
    creator_id: Optional[int] = None
    parent_id: Optional[int] = None
    sample: Optional[int] = None
    preview_height: Optional[int] = None
    preview_width: Optional[int] = None
    tags: Optional[str] = None
    title: Optional[str] = None
    has_notes: Optional[bool] = None
    has_comments: Optional[bool] = None
    file_url: Optional[str] = None
    preview_url: Optional[str] = None
    sample_url: Optional[str] = None
    sample_height: Optional[int] = None
    sample_width: Optional[int] = None
    status: Optional[Status] = None
    post_locked: Optional[int] = None
    has_children: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Post':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        created_at = from_union([from_str, from_none], obj.get("created_at"))
        score = from_union([from_int, from_none], obj.get("score"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        md5 = from_union([from_str, from_none], obj.get("md5"))
        directory = from_union([from_str, from_none], obj.get("directory"))
        image = from_union([from_str, from_none], obj.get("image"))
        rating = from_union([Rating, from_none], obj.get("rating"))
        source = from_union([from_str, from_none], obj.get("source"))
        change = from_union([from_int, from_none], obj.get("change"))
        owner = from_union([from_str, from_none], obj.get("owner"))
        creator_id = from_union([from_int, from_none], obj.get("creator_id"))
        parent_id = from_union([from_int, from_none], obj.get("parent_id"))
        sample = from_union([from_int, from_none], obj.get("sample"))
        preview_height = from_union([from_int, from_none], obj.get("preview_height"))
        preview_width = from_union([from_int, from_none], obj.get("preview_width"))
        tags = from_union([from_str, from_none], obj.get("tags"))
        title = from_union([from_str, from_none], obj.get("title"))
        has_notes = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("has_notes"))
        has_comments = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("has_comments"))
        file_url = from_union([from_str, from_none], obj.get("file_url"))
        preview_url = from_union([from_str, from_none], obj.get("preview_url"))
        sample_url = from_union([from_str, from_none], obj.get("sample_url"))
        sample_height = from_union([from_int, from_none], obj.get("sample_height"))
        sample_width = from_union([from_int, from_none], obj.get("sample_width"))
        status = from_union([Status, from_none], obj.get("status"))
        post_locked = from_union([from_int, from_none], obj.get("post_locked"))
        has_children = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("has_children"))
        return Post(id, created_at, score, width, height, md5, directory, image, rating, source, change, owner, creator_id, parent_id, sample, preview_height, preview_width, tags, title, has_notes, has_comments, file_url, preview_url, sample_url, sample_height, sample_width, status, post_locked, has_children)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_int, from_none], self.id)
        if self.created_at is not None:
            result["created_at"] = from_union([from_str, from_none], self.created_at)
        if self.score is not None:
            result["score"] = from_union([from_int, from_none], self.score)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.md5 is not None:
            result["md5"] = from_union([from_str, from_none], self.md5)
        if self.directory is not None:
            result["directory"] = from_union([from_str, from_none], self.directory)
        if self.image is not None:
            result["image"] = from_union([from_str, from_none], self.image)
        if self.rating is not None:
            result["rating"] = from_union([lambda x: to_enum(Rating, x), from_none], self.rating)
        if self.source is not None:
            result["source"] = from_union([from_str, from_none], self.source)
        if self.change is not None:
            result["change"] = from_union([from_int, from_none], self.change)
        if self.owner is not None:
            result["owner"] = from_union([from_str, from_none], self.owner)
        if self.creator_id is not None:
            result["creator_id"] = from_union([from_int, from_none], self.creator_id)
        if self.parent_id is not None:
            result["parent_id"] = from_union([from_int, from_none], self.parent_id)
        if self.sample is not None:
            result["sample"] = from_union([from_int, from_none], self.sample)
        if self.preview_height is not None:
            result["preview_height"] = from_union([from_int, from_none], self.preview_height)
        if self.preview_width is not None:
            result["preview_width"] = from_union([from_int, from_none], self.preview_width)
        if self.tags is not None:
            result["tags"] = from_union([from_str, from_none], self.tags)
        if self.title is not None:
            result["title"] = from_union([from_str, from_none], self.title)
        if self.has_notes is not None:
            result["has_notes"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))], self.has_notes)
        if self.has_comments is not None:
            result["has_comments"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))], self.has_comments)
        if self.file_url is not None:
            result["file_url"] = from_union([from_str, from_none], self.file_url)
        if self.preview_url is not None:
            result["preview_url"] = from_union([from_str, from_none], self.preview_url)
        if self.sample_url is not None:
            result["sample_url"] = from_union([from_str, from_none], self.sample_url)
        if self.sample_height is not None:
            result["sample_height"] = from_union([from_int, from_none], self.sample_height)
        if self.sample_width is not None:
            result["sample_width"] = from_union([from_int, from_none], self.sample_width)
        if self.status is not None:
            result["status"] = from_union([lambda x: to_enum(Status, x), from_none], self.status)
        if self.post_locked is not None:
            result["post_locked"] = from_union([from_int, from_none], self.post_locked)
        if self.has_children is not None:
            result["has_children"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))], self.has_children)
        return result


@dataclass
class Gelbooru:
    attributes: Optional[Attributes] = None
    post: Optional[List[Post]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Gelbooru':
        assert isinstance(obj, dict)
        attributes = from_union([Attributes.from_dict, from_none], obj.get("@attributes"))
        post = from_union([lambda x: from_list(Post.from_dict, x), from_none], obj.get("post"))
        return Gelbooru(attributes, post)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.attributes is not None:
            result["@attributes"] = from_union([lambda x: to_class(Attributes, x), from_none], self.attributes)
        if self.post is not None:
            result["post"] = from_union([lambda x: from_list(lambda x: to_class(Post, x), x), from_none], self.post)
        return result


def gelbooru_from_dict(s: Any) -> Gelbooru:
    return Gelbooru.from_dict(s)


def gelbooru_to_dict(x: Gelbooru) -> Any:
    return to_class(Gelbooru, x)
