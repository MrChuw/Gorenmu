from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, Callable, cast
from datetime import datetime
import dateutil.parser


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


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class FileEXT(Enum):
    JPG = "jpg"
    MP4 = "mp4"
    PNG = "png"
    WEBP = "webp"
    ZIP = "zip"


class Status(Enum):
    ACTIVE = "active"


class TypeEnum(Enum):
    ORIGINAL = "original"
    SAMPLE = "sample"
    THE_180_X180 = "180x180"
    THE_360_X360 = "360x360"
    THE_720_X720 = "720x720"


@dataclass
class Variant:
    type: Optional[TypeEnum] = None
    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    file_ext: Optional[FileEXT] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Variant':
        assert isinstance(obj, dict)
        type = from_union([TypeEnum, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        file_ext = from_union([FileEXT, from_none], obj.get("file_ext"))
        return Variant(type, url, width, height, file_ext)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union([lambda x: to_enum(TypeEnum, x), from_none], self.type)
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.file_ext is not None:
            result["file_ext"] = from_union([lambda x: to_enum(FileEXT, x), from_none], self.file_ext)
        return result


@dataclass
class MediaAsset:
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    md5: Optional[str] = None
    file_ext: Optional[FileEXT] = None
    file_size: Optional[int] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    duration: Optional[float] = None
    status: Optional[Status] = None
    file_key: Optional[str] = None
    is_public: Optional[bool] = None
    pixel_hash: Optional[str] = None
    variants: Optional[List[Variant]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MediaAsset':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        md5 = from_union([from_str, from_none], obj.get("md5"))
        file_ext = from_union([FileEXT, from_none], obj.get("file_ext"))
        file_size = from_union([from_int, from_none], obj.get("file_size"))
        image_width = from_union([from_int, from_none], obj.get("image_width"))
        image_height = from_union([from_int, from_none], obj.get("image_height"))
        duration = from_union([from_none, from_float], obj.get("duration"))
        status = from_union([Status, from_none], obj.get("status"))
        file_key = from_union([from_str, from_none], obj.get("file_key"))
        is_public = from_union([from_bool, from_none], obj.get("is_public"))
        pixel_hash = from_union([from_str, from_none], obj.get("pixel_hash"))
        variants = from_union([lambda x: from_list(Variant.from_dict, x), from_none], obj.get("variants"))
        return MediaAsset(id, created_at, updated_at, md5, file_ext, file_size, image_width, image_height, duration, status, file_key, is_public, pixel_hash, variants)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_int, from_none], self.id)
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        if self.md5 is not None:
            result["md5"] = from_union([from_str, from_none], self.md5)
        if self.file_ext is not None:
            result["file_ext"] = from_union([lambda x: to_enum(FileEXT, x), from_none], self.file_ext)
        if self.file_size is not None:
            result["file_size"] = from_union([from_int, from_none], self.file_size)
        if self.image_width is not None:
            result["image_width"] = from_union([from_int, from_none], self.image_width)
        if self.image_height is not None:
            result["image_height"] = from_union([from_int, from_none], self.image_height)
        if self.duration is not None:
            result["duration"] = from_union([from_none, to_float], self.duration)
        if self.status is not None:
            result["status"] = from_union([lambda x: to_enum(Status, x), from_none], self.status)
        if self.file_key is not None:
            result["file_key"] = from_union([from_str, from_none], self.file_key)
        if self.is_public is not None:
            result["is_public"] = from_union([from_bool, from_none], self.is_public)
        if self.pixel_hash is not None:
            result["pixel_hash"] = from_union([from_str, from_none], self.pixel_hash)
        if self.variants is not None:
            result["variants"] = from_union([lambda x: from_list(lambda x: to_class(Variant, x), x), from_none], self.variants)
        return result


class Rating(Enum):
    E = "e"
    G = "g"
    Q = "q"
    S = "s"


@dataclass
class DanbooruElement:
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    uploader_id: Optional[int] = None
    score: Optional[int] = None
    source: Optional[str] = None
    md5: Optional[str] = None
    last_comment_bumped_at: Optional[datetime] = None
    rating: Optional[Rating] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    tag_string: Optional[str] = None
    fav_count: Optional[int] = None
    file_ext: Optional[FileEXT] = None
    last_noted_at: Optional[datetime] = None
    parent_id: Optional[int] = None
    has_children: Optional[bool] = None
    approver_id: Optional[int] = None
    tag_count_general: Optional[int] = None
    tag_count_artist: Optional[int] = None
    tag_count_character: Optional[int] = None
    tag_count_copyright: Optional[int] = None
    file_size: Optional[int] = None
    up_score: Optional[int] = None
    down_score: Optional[int] = None
    is_pending: Optional[bool] = None
    is_flagged: Optional[bool] = None
    is_deleted: Optional[bool] = None
    tag_count: Optional[int] = None
    updated_at: Optional[datetime] = None
    is_banned: Optional[bool] = None
    pixiv_id: Optional[int] = None
    last_commented_at: Optional[datetime] = None
    has_active_children: Optional[bool] = None
    bit_flags: Optional[int] = None
    tag_count_meta: Optional[int] = None
    has_large: Optional[bool] = None
    has_visible_children: Optional[bool] = None
    media_asset: Optional[MediaAsset] = None
    tag_string_general: Optional[str] = None
    tag_string_character: Optional[str] = None
    tag_string_copyright: Optional[str] = None
    tag_string_artist: Optional[str] = None
    tag_string_meta: Optional[str] = None
    file_url: Optional[str] = None
    large_file_url: Optional[str] = None
    preview_file_url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DanbooruElement':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        uploader_id = from_union([from_int, from_none], obj.get("uploader_id"))
        score = from_union([from_int, from_none], obj.get("score"))
        source = from_union([from_str, from_none], obj.get("source"))
        md5 = from_union([from_str, from_none], obj.get("md5"))
        last_comment_bumped_at = from_union([from_datetime, from_none], obj.get("last_comment_bumped_at"))
        rating = from_union([Rating, from_none], obj.get("rating"))
        image_width = from_union([from_int, from_none], obj.get("image_width"))
        image_height = from_union([from_int, from_none], obj.get("image_height"))
        tag_string = from_union([from_str, from_none], obj.get("tag_string"))
        fav_count = from_union([from_int, from_none], obj.get("fav_count"))
        file_ext = from_union([FileEXT, from_none], obj.get("file_ext"))
        last_noted_at = from_union([from_datetime, from_none], obj.get("last_noted_at"))
        parent_id = from_union([from_int, from_none], obj.get("parent_id"))
        has_children = from_union([from_bool, from_none], obj.get("has_children"))
        approver_id = from_union([from_int, from_none], obj.get("approver_id"))
        tag_count_general = from_union([from_int, from_none], obj.get("tag_count_general"))
        tag_count_artist = from_union([from_int, from_none], obj.get("tag_count_artist"))
        tag_count_character = from_union([from_int, from_none], obj.get("tag_count_character"))
        tag_count_copyright = from_union([from_int, from_none], obj.get("tag_count_copyright"))
        file_size = from_union([from_int, from_none], obj.get("file_size"))
        up_score = from_union([from_int, from_none], obj.get("up_score"))
        down_score = from_union([from_int, from_none], obj.get("down_score"))
        is_pending = from_union([from_bool, from_none], obj.get("is_pending"))
        is_flagged = from_union([from_bool, from_none], obj.get("is_flagged"))
        is_deleted = from_union([from_bool, from_none], obj.get("is_deleted"))
        tag_count = from_union([from_int, from_none], obj.get("tag_count"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        is_banned = from_union([from_bool, from_none], obj.get("is_banned"))
        pixiv_id = from_union([from_int, from_none], obj.get("pixiv_id"))
        last_commented_at = from_union([from_datetime, from_none], obj.get("last_commented_at"))
        has_active_children = from_union([from_bool, from_none], obj.get("has_active_children"))
        bit_flags = from_union([from_int, from_none], obj.get("bit_flags"))
        tag_count_meta = from_union([from_int, from_none], obj.get("tag_count_meta"))
        has_large = from_union([from_bool, from_none], obj.get("has_large"))
        has_visible_children = from_union([from_bool, from_none], obj.get("has_visible_children"))
        media_asset = from_union([MediaAsset.from_dict, from_none], obj.get("media_asset"))
        tag_string_general = from_union([from_str, from_none], obj.get("tag_string_general"))
        tag_string_character = from_union([from_str, from_none], obj.get("tag_string_character"))
        tag_string_copyright = from_union([from_str, from_none], obj.get("tag_string_copyright"))
        tag_string_artist = from_union([from_str, from_none], obj.get("tag_string_artist"))
        tag_string_meta = from_union([from_str, from_none], obj.get("tag_string_meta"))
        file_url = from_union([from_str, from_none], obj.get("file_url"))
        large_file_url = from_union([from_str, from_none], obj.get("large_file_url"))
        preview_file_url = from_union([from_str, from_none], obj.get("preview_file_url"))
        return DanbooruElement(id, created_at, uploader_id, score, source, md5, last_comment_bumped_at, rating, image_width, image_height, tag_string, fav_count, file_ext, last_noted_at, parent_id, has_children, approver_id, tag_count_general, tag_count_artist, tag_count_character, tag_count_copyright, file_size, up_score, down_score, is_pending, is_flagged, is_deleted, tag_count, updated_at, is_banned, pixiv_id, last_commented_at, has_active_children, bit_flags, tag_count_meta, has_large, has_visible_children, media_asset, tag_string_general, tag_string_character, tag_string_copyright, tag_string_artist, tag_string_meta, file_url, large_file_url, preview_file_url)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_int, from_none], self.id)
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.uploader_id is not None:
            result["uploader_id"] = from_union([from_int, from_none], self.uploader_id)
        if self.score is not None:
            result["score"] = from_union([from_int, from_none], self.score)
        if self.source is not None:
            result["source"] = from_union([from_str, from_none], self.source)
        if self.md5 is not None:
            result["md5"] = from_union([from_str, from_none], self.md5)
        if self.last_comment_bumped_at is not None:
            result["last_comment_bumped_at"] = from_union([lambda x: x.isoformat(), from_none], self.last_comment_bumped_at)
        if self.rating is not None:
            result["rating"] = from_union([lambda x: to_enum(Rating, x), from_none], self.rating)
        if self.image_width is not None:
            result["image_width"] = from_union([from_int, from_none], self.image_width)
        if self.image_height is not None:
            result["image_height"] = from_union([from_int, from_none], self.image_height)
        if self.tag_string is not None:
            result["tag_string"] = from_union([from_str, from_none], self.tag_string)
        if self.fav_count is not None:
            result["fav_count"] = from_union([from_int, from_none], self.fav_count)
        if self.file_ext is not None:
            result["file_ext"] = from_union([lambda x: to_enum(FileEXT, x), from_none], self.file_ext)
        if self.last_noted_at is not None:
            result["last_noted_at"] = from_union([lambda x: x.isoformat(), from_none], self.last_noted_at)
        if self.parent_id is not None:
            result["parent_id"] = from_union([from_int, from_none], self.parent_id)
        if self.has_children is not None:
            result["has_children"] = from_union([from_bool, from_none], self.has_children)
        if self.approver_id is not None:
            result["approver_id"] = from_union([from_int, from_none], self.approver_id)
        if self.tag_count_general is not None:
            result["tag_count_general"] = from_union([from_int, from_none], self.tag_count_general)
        if self.tag_count_artist is not None:
            result["tag_count_artist"] = from_union([from_int, from_none], self.tag_count_artist)
        if self.tag_count_character is not None:
            result["tag_count_character"] = from_union([from_int, from_none], self.tag_count_character)
        if self.tag_count_copyright is not None:
            result["tag_count_copyright"] = from_union([from_int, from_none], self.tag_count_copyright)
        if self.file_size is not None:
            result["file_size"] = from_union([from_int, from_none], self.file_size)
        if self.up_score is not None:
            result["up_score"] = from_union([from_int, from_none], self.up_score)
        if self.down_score is not None:
            result["down_score"] = from_union([from_int, from_none], self.down_score)
        if self.is_pending is not None:
            result["is_pending"] = from_union([from_bool, from_none], self.is_pending)
        if self.is_flagged is not None:
            result["is_flagged"] = from_union([from_bool, from_none], self.is_flagged)
        if self.is_deleted is not None:
            result["is_deleted"] = from_union([from_bool, from_none], self.is_deleted)
        if self.tag_count is not None:
            result["tag_count"] = from_union([from_int, from_none], self.tag_count)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        if self.is_banned is not None:
            result["is_banned"] = from_union([from_bool, from_none], self.is_banned)
        if self.pixiv_id is not None:
            result["pixiv_id"] = from_union([from_int, from_none], self.pixiv_id)
        if self.last_commented_at is not None:
            result["last_commented_at"] = from_union([lambda x: x.isoformat(), from_none], self.last_commented_at)
        if self.has_active_children is not None:
            result["has_active_children"] = from_union([from_bool, from_none], self.has_active_children)
        if self.bit_flags is not None:
            result["bit_flags"] = from_union([from_int, from_none], self.bit_flags)
        if self.tag_count_meta is not None:
            result["tag_count_meta"] = from_union([from_int, from_none], self.tag_count_meta)
        if self.has_large is not None:
            result["has_large"] = from_union([from_bool, from_none], self.has_large)
        if self.has_visible_children is not None:
            result["has_visible_children"] = from_union([from_bool, from_none], self.has_visible_children)
        if self.media_asset is not None:
            result["media_asset"] = from_union([lambda x: to_class(MediaAsset, x), from_none], self.media_asset)
        if self.tag_string_general is not None:
            result["tag_string_general"] = from_union([from_str, from_none], self.tag_string_general)
        if self.tag_string_character is not None:
            result["tag_string_character"] = from_union([from_str, from_none], self.tag_string_character)
        if self.tag_string_copyright is not None:
            result["tag_string_copyright"] = from_union([from_str, from_none], self.tag_string_copyright)
        if self.tag_string_artist is not None:
            result["tag_string_artist"] = from_union([from_str, from_none], self.tag_string_artist)
        if self.tag_string_meta is not None:
            result["tag_string_meta"] = from_union([from_str, from_none], self.tag_string_meta)
        if self.file_url is not None:
            result["file_url"] = from_union([from_str, from_none], self.file_url)
        if self.large_file_url is not None:
            result["large_file_url"] = from_union([from_str, from_none], self.large_file_url)
        if self.preview_file_url is not None:
            result["preview_file_url"] = from_union([from_str, from_none], self.preview_file_url)
        return result


def danbooru_from_dict(s: Any) -> List[DanbooruElement]:
    return from_list(DanbooruElement.from_dict, s)


def danbooru_to_dict(x: List[DanbooruElement]) -> Any:
    return from_list(lambda x: to_class(DanbooruElement, x), x)
