from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


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


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Format(Enum):
    GIF = "gif"
    JPG = "jpg"
    PNG = "png"


@dataclass
class Intensities:
    nw: Optional[float] = None
    ne: Optional[float] = None
    sw: Optional[float] = None
    se: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Intensities':
        assert isinstance(obj, dict)
        nw = from_union([from_float, from_none], obj.get("nw"))
        ne = from_union([from_float, from_none], obj.get("ne"))
        sw = from_union([from_float, from_none], obj.get("sw"))
        se = from_union([from_float, from_none], obj.get("se"))
        return Intensities(nw, ne, sw, se)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nw is not None:
            result["nw"] = from_union([to_float, from_none], self.nw)
        if self.ne is not None:
            result["ne"] = from_union([to_float, from_none], self.ne)
        if self.sw is not None:
            result["sw"] = from_union([to_float, from_none], self.sw)
        if self.se is not None:
            result["se"] = from_union([to_float, from_none], self.se)
        return result


class MIMEType(Enum):
    IMAGE_GIF = "image/gif"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"


@dataclass
class Representations:
    full: Optional[str] = None
    small: Optional[str] = None
    thumb_tiny: Optional[str] = None
    thumb_small: Optional[str] = None
    thumb: Optional[str] = None
    medium: Optional[str] = None
    large: Optional[str] = None
    tall: Optional[str] = None
    mp4: Optional[str] = None
    webm: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Representations':
        assert isinstance(obj, dict)
        full = from_union([from_str, from_none], obj.get("full"))
        small = from_union([from_str, from_none], obj.get("small"))
        thumb_tiny = from_union([from_str, from_none], obj.get("thumb_tiny"))
        thumb_small = from_union([from_str, from_none], obj.get("thumb_small"))
        thumb = from_union([from_str, from_none], obj.get("thumb"))
        medium = from_union([from_str, from_none], obj.get("medium"))
        large = from_union([from_str, from_none], obj.get("large"))
        tall = from_union([from_str, from_none], obj.get("tall"))
        mp4 = from_union([from_str, from_none], obj.get("mp4"))
        webm = from_union([from_str, from_none], obj.get("webm"))
        return Representations(full, small, thumb_tiny, thumb_small, thumb, medium, large, tall, mp4, webm)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.full is not None:
            result["full"] = from_union([from_str, from_none], self.full)
        if self.small is not None:
            result["small"] = from_union([from_str, from_none], self.small)
        if self.thumb_tiny is not None:
            result["thumb_tiny"] = from_union([from_str, from_none], self.thumb_tiny)
        if self.thumb_small is not None:
            result["thumb_small"] = from_union([from_str, from_none], self.thumb_small)
        if self.thumb is not None:
            result["thumb"] = from_union([from_str, from_none], self.thumb)
        if self.medium is not None:
            result["medium"] = from_union([from_str, from_none], self.medium)
        if self.large is not None:
            result["large"] = from_union([from_str, from_none], self.large)
        if self.tall is not None:
            result["tall"] = from_union([from_str, from_none], self.tall)
        if self.mp4 is not None:
            result["mp4"] = from_union([from_str, from_none], self.mp4)
        if self.webm is not None:
            result["webm"] = from_union([from_str, from_none], self.webm)
        return result


@dataclass
class Image:
    view_url: Optional[str] = None
    sha512_hash: Optional[str] = None
    width: Optional[int] = None
    description: Optional[str] = None
    height: Optional[int] = None
    orig_sha512_hash: Optional[str] = None
    processed: Optional[bool] = None
    format: Optional[Format] = None
    comment_count: Optional[int] = None
    faves: Optional[int] = None
    representations: Optional[Representations] = None
    size: Optional[int] = None
    mime_type: Optional[MIMEType] = None
    source_url: Optional[str] = None
    source_urls: Optional[List[str]] = None
    upvotes: Optional[int] = None
    uploader: Optional[str] = None
    duration: Optional[float] = None
    intensities: Optional[Intensities] = None
    wilson_score: Optional[float] = None
    tags: Optional[List[str]] = None
    tag_ids: Optional[List[int]] = None
    score: Optional[int] = None
    first_seen_at: Optional[datetime] = None
    animated: Optional[bool] = None
    aspect_ratio: Optional[float] = None
    id: Optional[int] = None
    name: Optional[str] = None
    duplicate_of: Optional[str] = None
    orig_size: Optional[int] = None
    hidden_from_users: Optional[bool] = None
    spoilered: Optional[bool] = None
    thumbnails_generated: Optional[bool] = None
    created_at: Optional[datetime] = None
    deletion_reason: Optional[str] = None
    downvotes: Optional[int] = None
    updated_at: Optional[datetime] = None
    tag_count: Optional[int] = None
    uploader_id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        assert isinstance(obj, dict)
        view_url = from_union([from_str, from_none], obj.get("view_url"))
        sha512_hash = from_union([from_str, from_none], obj.get("sha512_hash"))
        width = from_union([from_int, from_none], obj.get("width"))
        description = from_union([from_str, from_none], obj.get("description"))
        height = from_union([from_int, from_none], obj.get("height"))
        orig_sha512_hash = from_union([from_str, from_none], obj.get("orig_sha512_hash"))
        processed = from_union([from_bool, from_none], obj.get("processed"))
        format = from_union([Format, from_none], obj.get("format"))
        comment_count = from_union([from_int, from_none], obj.get("comment_count"))
        faves = from_union([from_int, from_none], obj.get("faves"))
        representations = from_union([Representations.from_dict, from_none], obj.get("representations"))
        size = from_union([from_int, from_none], obj.get("size"))
        mime_type = from_union([MIMEType, from_none], obj.get("mime_type"))
        source_url = from_union([from_str, from_none], obj.get("source_url"))
        source_urls = from_union([lambda x: from_list(from_str, x), from_none], obj.get("source_urls"))
        upvotes = from_union([from_int, from_none], obj.get("upvotes"))
        uploader = from_union([from_none, from_str], obj.get("uploader"))
        duration = from_union([from_float, from_none], obj.get("duration"))
        intensities = from_union([Intensities.from_dict, from_none], obj.get("intensities"))
        wilson_score = from_union([from_float, from_none], obj.get("wilson_score"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        tag_ids = from_union([lambda x: from_list(from_int, x), from_none], obj.get("tag_ids"))
        score = from_union([from_int, from_none], obj.get("score"))
        first_seen_at = from_union([from_datetime, from_none], obj.get("first_seen_at"))
        animated = from_union([from_bool, from_none], obj.get("animated"))
        aspect_ratio = from_union([from_float, from_none], obj.get("aspect_ratio"))
        id = from_union([from_int, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        duplicate_of = from_union([from_str, from_none], obj.get("duplicate_of"))
        orig_size = from_union([from_int, from_none], obj.get("orig_size"))
        hidden_from_users = from_union([from_bool, from_none], obj.get("hidden_from_users"))
        spoilered = from_union([from_bool, from_none], obj.get("spoilered"))
        thumbnails_generated = from_union([from_bool, from_none], obj.get("thumbnails_generated"))
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        deletion_reason = from_union([from_str, from_none], obj.get("deletion_reason"))
        downvotes = from_union([from_int, from_none], obj.get("downvotes"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        tag_count = from_union([from_int, from_none], obj.get("tag_count"))
        uploader_id = from_union([from_int, from_none], obj.get("uploader_id"))
        return Image(view_url, sha512_hash, width, description, height, orig_sha512_hash, processed, format, comment_count, faves, representations, size, mime_type, source_url, source_urls, upvotes, uploader, duration, intensities, wilson_score, tags, tag_ids, score, first_seen_at, animated, aspect_ratio, id, name, duplicate_of, orig_size, hidden_from_users, spoilered, thumbnails_generated, created_at, deletion_reason, downvotes, updated_at, tag_count, uploader_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.view_url is not None:
            result["view_url"] = from_union([from_str, from_none], self.view_url)
        if self.sha512_hash is not None:
            result["sha512_hash"] = from_union([from_str, from_none], self.sha512_hash)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.description is not None:
            result["description"] = from_union([from_str, from_none], self.description)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.orig_sha512_hash is not None:
            result["orig_sha512_hash"] = from_union([from_str, from_none], self.orig_sha512_hash)
        if self.processed is not None:
            result["processed"] = from_union([from_bool, from_none], self.processed)
        if self.format is not None:
            result["format"] = from_union([lambda x: to_enum(Format, x), from_none], self.format)
        if self.comment_count is not None:
            result["comment_count"] = from_union([from_int, from_none], self.comment_count)
        if self.faves is not None:
            result["faves"] = from_union([from_int, from_none], self.faves)
        if self.representations is not None:
            result["representations"] = from_union([lambda x: to_class(Representations, x), from_none], self.representations)
        if self.size is not None:
            result["size"] = from_union([from_int, from_none], self.size)
        if self.mime_type is not None:
            result["mime_type"] = from_union([lambda x: to_enum(MIMEType, x), from_none], self.mime_type)
        if self.source_url is not None:
            result["source_url"] = from_union([from_str, from_none], self.source_url)
        if self.source_urls is not None:
            result["source_urls"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_urls)
        if self.upvotes is not None:
            result["upvotes"] = from_union([from_int, from_none], self.upvotes)
        if self.uploader is not None:
            result["uploader"] = from_union([from_none, from_str], self.uploader)
        if self.duration is not None:
            result["duration"] = from_union([to_float, from_none], self.duration)
        if self.intensities is not None:
            result["intensities"] = from_union([lambda x: to_class(Intensities, x), from_none], self.intensities)
        if self.wilson_score is not None:
            result["wilson_score"] = from_union([to_float, from_none], self.wilson_score)
        if self.tags is not None:
            result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        if self.tag_ids is not None:
            result["tag_ids"] = from_union([lambda x: from_list(from_int, x), from_none], self.tag_ids)
        if self.score is not None:
            result["score"] = from_union([from_int, from_none], self.score)
        if self.first_seen_at is not None:
            result["first_seen_at"] = from_union([lambda x: x.isoformat(), from_none], self.first_seen_at)
        if self.animated is not None:
            result["animated"] = from_union([from_bool, from_none], self.animated)
        if self.aspect_ratio is not None:
            result["aspect_ratio"] = from_union([to_float, from_none], self.aspect_ratio)
        if self.id is not None:
            result["id"] = from_union([from_int, from_none], self.id)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.duplicate_of is not None:
            result["duplicate_of"] = from_none(self.duplicate_of)
        if self.orig_size is not None:
            result["orig_size"] = from_union([from_int, from_none], self.orig_size)
        if self.hidden_from_users is not None:
            result["hidden_from_users"] = from_union([from_bool, from_none], self.hidden_from_users)
        if self.spoilered is not None:
            result["spoilered"] = from_union([from_bool, from_none], self.spoilered)
        if self.thumbnails_generated is not None:
            result["thumbnails_generated"] = from_union([from_bool, from_none], self.thumbnails_generated)
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.deletion_reason is not None:
            result["deletion_reason"] = from_none(self.deletion_reason)
        if self.downvotes is not None:
            result["downvotes"] = from_union([from_int, from_none], self.downvotes)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        if self.tag_count is not None:
            result["tag_count"] = from_union([from_int, from_none], self.tag_count)
        if self.uploader_id is not None:
            result["uploader_id"] = from_union([from_int, from_none], self.uploader_id)
        return result


@dataclass
class Furbooru:
    total: Optional[int] = None
    images: Optional[List[Image]] = None
    interactions: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Furbooru':
        assert isinstance(obj, dict)
        total = from_union([from_int, from_none], obj.get("total"))
        images = from_union([lambda x: from_list(Image.from_dict, x), from_none], obj.get("images"))
        interactions = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("interactions"))
        return Furbooru(total, images, interactions)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.total is not None:
            result["total"] = from_union([from_int, from_none], self.total)
        if self.images is not None:
            result["images"] = from_union([lambda x: from_list(lambda x: to_class(Image, x), x), from_none], self.images)
        if self.interactions is not None:
            result["interactions"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.interactions)
        return result


def furbooru_from_dict(s: Any) -> Furbooru:
    return Furbooru.from_dict(s)


def furbooru_to_dict(x: Furbooru) -> Any:
    return to_class(Furbooru, x)
