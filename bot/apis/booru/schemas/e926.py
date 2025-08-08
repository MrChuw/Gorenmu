from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, cast

import dateutil.parser

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


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


class EXT(Enum):
    GIF = "gif"
    JPG = "jpg"
    PNG = "png"
    WEBM = "webm"


@dataclass
class File:
    width: Optional[int] = None
    height: Optional[int] = None
    ext: Optional[EXT] = None
    size: Optional[int] = None
    md5: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "File":
        assert isinstance(obj, dict)
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        ext = from_union([EXT, from_none], obj.get("ext"))
        size = from_union([from_int, from_none], obj.get("size"))
        md5 = from_union([from_str, from_none], obj.get("md5"))
        url = from_union([from_none, from_str], obj.get("url"))
        return File(width, height, ext, size, md5, url)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.ext is not None:
            result["ext"] = from_union([lambda x: to_enum(EXT, x), from_none], self.ext)
        if self.size is not None:
            result["size"] = from_union([from_int, from_none], self.size)
        if self.md5 is not None:
            result["md5"] = from_union([from_str, from_none], self.md5)
        if self.url is not None:
            result["url"] = from_union([from_none, from_str], self.url)
        return result


@dataclass
class Flags:
    pending: Optional[bool] = None
    flagged: Optional[bool] = None
    note_locked: Optional[bool] = None
    status_locked: Optional[bool] = None
    rating_locked: Optional[bool] = None
    deleted: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> "Flags":
        assert isinstance(obj, dict)
        pending = from_union([from_bool, from_none], obj.get("pending"))
        flagged = from_union([from_bool, from_none], obj.get("flagged"))
        note_locked = from_union([from_bool, from_none], obj.get("note_locked"))
        status_locked = from_union([from_bool, from_none], obj.get("status_locked"))
        rating_locked = from_union([from_bool, from_none], obj.get("rating_locked"))
        deleted = from_union([from_bool, from_none], obj.get("deleted"))
        return Flags(pending, flagged, note_locked, status_locked, rating_locked, deleted)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.pending is not None:
            result["pending"] = from_union([from_bool, from_none], self.pending)
        if self.flagged is not None:
            result["flagged"] = from_union([from_bool, from_none], self.flagged)
        if self.note_locked is not None:
            result["note_locked"] = from_union([from_bool, from_none], self.note_locked)
        if self.status_locked is not None:
            result["status_locked"] = from_union([from_bool, from_none], self.status_locked)
        if self.rating_locked is not None:
            result["rating_locked"] = from_union([from_bool, from_none], self.rating_locked)
        if self.deleted is not None:
            result["deleted"] = from_union([from_bool, from_none], self.deleted)
        return result


class LockedTag(Enum):
    CONDITIONAL_DNP = "conditional_dnp"


@dataclass
class Preview:
    width: Optional[int] = None
    height: Optional[int] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Preview":
        assert isinstance(obj, dict)
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        url = from_union([from_none, from_str], obj.get("url"))
        return Preview(width, height, url)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.url is not None:
            result["url"] = from_union([from_none, from_str], self.url)
        return result


class Rating(Enum):
    S = "s"


@dataclass
class Relationships:
    parent_id: Optional[int] = None
    has_children: Optional[bool] = None
    has_active_children: Optional[bool] = None
    children: Optional[List[int]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Relationships":
        assert isinstance(obj, dict)
        parent_id = from_union([from_int, from_none], obj.get("parent_id"))
        has_children = from_union([from_bool, from_none], obj.get("has_children"))
        has_active_children = from_union([from_bool, from_none], obj.get("has_active_children"))
        children = from_union([lambda x: from_list(from_int, x), from_none], obj.get("children"))
        return Relationships(parent_id, has_children, has_active_children, children)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.parent_id is not None:
            result["parent_id"] = from_union([from_int, from_none], self.parent_id)
        if self.has_children is not None:
            result["has_children"] = from_union([from_bool, from_none], self.has_children)
        if self.has_active_children is not None:
            result["has_active_children"] = from_union([from_bool, from_none], self.has_active_children)
        if self.children is not None:
            result["children"] = from_union([lambda x: from_list(from_int, x), from_none], self.children)
        return result


class TypeEnum(Enum):
    VIDEO = "video"


@dataclass
class Alternate:
    type: Optional[TypeEnum] = None
    height: Optional[int] = None
    width: Optional[int] = None
    urls: Optional[List[Optional[str]]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Alternate":
        assert isinstance(obj, dict)
        type = from_union([TypeEnum, from_none], obj.get("type"))
        height = from_union([from_int, from_none], obj.get("height"))
        width = from_union([from_int, from_none], obj.get("width"))
        urls = from_union(
            [lambda x: from_list(lambda x: from_union([from_none, from_str], x), x), from_none], obj.get("urls")
        )
        return Alternate(type, height, width, urls)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union([lambda x: to_enum(TypeEnum, x), from_none], self.type)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.urls is not None:
            result["urls"] = from_union(
                [lambda x: from_list(lambda x: from_union([from_none, from_str], x), x), from_none], self.urls
            )
        return result


@dataclass
class Sample:
    has: Optional[bool] = None
    height: Optional[int] = None
    width: Optional[int] = None
    url: Optional[str] = None
    alternates: Optional[Dict[str, Alternate]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Sample":
        assert isinstance(obj, dict)
        has = from_union([from_bool, from_none], obj.get("has"))
        height = from_union([from_int, from_none], obj.get("height"))
        width = from_union([from_int, from_none], obj.get("width"))
        url = from_union([from_none, from_str], obj.get("url"))
        alternates = from_union([lambda x: from_dict(Alternate.from_dict, x), from_none], obj.get("alternates"))
        return Sample(has, height, width, url, alternates)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.has is not None:
            result["has"] = from_union([from_bool, from_none], self.has)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.url is not None:
            result["url"] = from_union([from_none, from_str], self.url)
        if self.alternates is not None:
            result["alternates"] = from_union(
                [lambda x: from_dict(lambda x: to_class(Alternate, x), x), from_none], self.alternates
            )
        return result


@dataclass
class Score:
    up: Optional[int] = None
    down: Optional[int] = None
    total: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Score":
        assert isinstance(obj, dict)
        up = from_union([from_int, from_none], obj.get("up"))
        down = from_union([from_int, from_none], obj.get("down"))
        total = from_union([from_int, from_none], obj.get("total"))
        return Score(up, down, total)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.up is not None:
            result["up"] = from_union([from_int, from_none], self.up)
        if self.down is not None:
            result["down"] = from_union([from_int, from_none], self.down)
        if self.total is not None:
            result["total"] = from_union([from_int, from_none], self.total)
        return result


@dataclass
class Tags:
    general: Optional[List[str]] = None
    artist: Optional[List[str]] = None
    copyright: Optional[List[str]] = None
    character: Optional[List[str]] = None
    species: Optional[List[str]] = None
    invalid: Optional[List[str]] = None
    meta: Optional[List[str]] = None
    lore: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Tags":
        assert isinstance(obj, dict)
        general = from_union([lambda x: from_list(from_str, x), from_none], obj.get("general"))
        artist = from_union([lambda x: from_list(from_str, x), from_none], obj.get("artist"))
        copyright = from_union([lambda x: from_list(from_str, x), from_none], obj.get("copyright"))
        character = from_union([lambda x: from_list(from_str, x), from_none], obj.get("character"))
        species = from_union([lambda x: from_list(from_str, x), from_none], obj.get("species"))
        invalid = from_union([lambda x: from_list(from_str, x), from_none], obj.get("invalid"))
        meta = from_union([lambda x: from_list(from_str, x), from_none], obj.get("meta"))
        lore = from_union([lambda x: from_list(from_str, x), from_none], obj.get("lore"))
        return Tags(general, artist, copyright, character, species, invalid, meta, lore)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.general is not None:
            result["general"] = from_union([lambda x: from_list(from_str, x), from_none], self.general)
        if self.artist is not None:
            result["artist"] = from_union([lambda x: from_list(from_str, x), from_none], self.artist)
        if self.copyright is not None:
            result["copyright"] = from_union([lambda x: from_list(from_str, x), from_none], self.copyright)
        if self.character is not None:
            result["character"] = from_union([lambda x: from_list(from_str, x), from_none], self.character)
        if self.species is not None:
            result["species"] = from_union([lambda x: from_list(from_str, x), from_none], self.species)
        if self.invalid is not None:
            result["invalid"] = from_union([lambda x: from_list(from_str, x), from_none], self.invalid)
        if self.meta is not None:
            result["meta"] = from_union([lambda x: from_list(from_str, x), from_none], self.meta)
        if self.lore is not None:
            result["lore"] = from_union([lambda x: from_list(from_str, x), from_none], self.lore)
        return result


@dataclass
class Post:
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    file: Optional[File] = None
    preview: Optional[Preview] = None
    sample: Optional[Sample] = None
    score: Optional[Score] = None
    tags: Optional[Tags] = None
    locked_tags: Optional[List[LockedTag]] = None
    change_seq: Optional[int] = None
    flags: Optional[Flags] = None
    rating: Optional[Rating] = None
    fav_count: Optional[int] = None
    sources: Optional[List[str]] = None
    pools: Optional[List[int]] = None
    relationships: Optional[Relationships] = None
    approver_id: Optional[int] = None
    uploader_id: Optional[int] = None
    description: Optional[str] = None
    comment_count: Optional[int] = None
    is_favorited: Optional[bool] = None
    has_notes: Optional[bool] = None
    duration: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> "Post":
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        file = from_union([File.from_dict, from_none], obj.get("file"))
        preview = from_union([Preview.from_dict, from_none], obj.get("preview"))
        sample = from_union([Sample.from_dict, from_none], obj.get("sample"))
        score = from_union([Score.from_dict, from_none], obj.get("score"))
        tags = from_union([Tags.from_dict, from_none], obj.get("tags"))
        locked_tags = from_union([lambda x: from_list(LockedTag, x), from_none], obj.get("locked_tags"))
        change_seq = from_union([from_int, from_none], obj.get("change_seq"))
        flags = from_union([Flags.from_dict, from_none], obj.get("flags"))
        rating = from_union([Rating, from_none], obj.get("rating"))
        fav_count = from_union([from_int, from_none], obj.get("fav_count"))
        sources = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sources"))
        pools = from_union([lambda x: from_list(from_int, x), from_none], obj.get("pools"))
        relationships = from_union([Relationships.from_dict, from_none], obj.get("relationships"))
        approver_id = from_union([from_int, from_none], obj.get("approver_id"))
        uploader_id = from_union([from_int, from_none], obj.get("uploader_id"))
        description = from_union([from_str, from_none], obj.get("description"))
        comment_count = from_union([from_int, from_none], obj.get("comment_count"))
        is_favorited = from_union([from_bool, from_none], obj.get("is_favorited"))
        has_notes = from_union([from_bool, from_none], obj.get("has_notes"))
        duration = from_union([from_none, from_float], obj.get("duration"))
        return Post(
            id,
            created_at,
            updated_at,
            file,
            preview,
            sample,
            score,
            tags,
            locked_tags,
            change_seq,
            flags,
            rating,
            fav_count,
            sources,
            pools,
            relationships,
            approver_id,
            uploader_id,
            description,
            comment_count,
            is_favorited,
            has_notes,
            duration,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_int, from_none], self.id)
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        if self.file is not None:
            result["file"] = from_union([lambda x: to_class(File, x), from_none], self.file)
        if self.preview is not None:
            result["preview"] = from_union([lambda x: to_class(Preview, x), from_none], self.preview)
        if self.sample is not None:
            result["sample"] = from_union([lambda x: to_class(Sample, x), from_none], self.sample)
        if self.score is not None:
            result["score"] = from_union([lambda x: to_class(Score, x), from_none], self.score)
        if self.tags is not None:
            result["tags"] = from_union([lambda x: to_class(Tags, x), from_none], self.tags)
        if self.locked_tags is not None:
            result["locked_tags"] = from_union(
                [lambda x: from_list(lambda x: to_enum(LockedTag, x), x), from_none], self.locked_tags
            )
        if self.change_seq is not None:
            result["change_seq"] = from_union([from_int, from_none], self.change_seq)
        if self.flags is not None:
            result["flags"] = from_union([lambda x: to_class(Flags, x), from_none], self.flags)
        if self.rating is not None:
            result["rating"] = from_union([lambda x: to_enum(Rating, x), from_none], self.rating)
        if self.fav_count is not None:
            result["fav_count"] = from_union([from_int, from_none], self.fav_count)
        if self.sources is not None:
            result["sources"] = from_union([lambda x: from_list(from_str, x), from_none], self.sources)
        if self.pools is not None:
            result["pools"] = from_union([lambda x: from_list(from_int, x), from_none], self.pools)
        if self.relationships is not None:
            result["relationships"] = from_union([lambda x: to_class(Relationships, x), from_none], self.relationships)
        if self.approver_id is not None:
            result["approver_id"] = from_union([from_int, from_none], self.approver_id)
        if self.uploader_id is not None:
            result["uploader_id"] = from_union([from_int, from_none], self.uploader_id)
        if self.description is not None:
            result["description"] = from_union([from_str, from_none], self.description)
        if self.comment_count is not None:
            result["comment_count"] = from_union([from_int, from_none], self.comment_count)
        if self.is_favorited is not None:
            result["is_favorited"] = from_union([from_bool, from_none], self.is_favorited)
        if self.has_notes is not None:
            result["has_notes"] = from_union([from_bool, from_none], self.has_notes)
        if self.duration is not None:
            result["duration"] = from_union([from_none, to_float], self.duration)
        return result


@dataclass
class E926:
    posts: Optional[List[Post]] = None

    @staticmethod
    def from_dict(obj: Any) -> "E926":
        assert isinstance(obj, dict)
        posts = from_union([lambda x: from_list(Post.from_dict, x), from_none], obj.get("posts"))
        return E926(posts)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.posts is not None:
            result["posts"] = from_union([lambda x: from_list(lambda x: to_class(Post, x), x), from_none], self.posts)
        return result


def e926_from_dict(s: Any) -> E926:
    return E926.from_dict(s)


def e926_to_dict(x: E926) -> Any:
    return to_class(E926, x)
