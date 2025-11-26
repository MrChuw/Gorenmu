from datetime import datetime
from typing import Dict, List, Optional, Union
from urllib.parse import unquote

from yarl import URL


def parse_datetime(data: dict, key: str, formato: str) -> Optional[datetime]:
    date = data.get(key)
    if date is not None and formato == "%Y-%m-%dT%H:%M:%S.%f%z":
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")

    if date is not None and formato == "%Y-%m-%dT%H:%M:%S.%f":
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")

    if date is not None and formato == "%a %b %d %H:%M:%S %z %Y":
        return datetime.strptime(date, "%a %b %d %H:%M:%S %z %Y")

    if date is not None and formato == "timestamp":
        return datetime.fromtimestamp(date)

    return None


def str_to_url(data: dict, key: str) -> Optional[URL]:
    url = data.get(key)

    if isinstance(url, list):
        urls = []
        for urll in url:
            urll = unquote(urll)
            urls.append(URL(urll))
        return urls

    if url is not None:
        url = unquote(url)
        return URL(url.replace(" ", "_"))

    return None


class Gelbooru:
    def __init__(self, data: dict):
        self.change: int = data.get("change", 0)
        self.created_at: Optional[datetime] = parse_datetime(
            data, "created_at", "%a %b %d %H:%M:%S %z %Y"
        )
        self.creator_id: int = data.get("creator_id", 0)
        self.directory: str = data.get("directory", "")
        self.file_url: Optional[URL] = str_to_url(data, "file_url")
        self.has_children: bool = data.get("has_children", False)
        self.has_comments: bool = data.get("has_comments", False)
        self.has_notes: bool = data.get("has_notes", False)
        self.height: int = data.get("height", 0)
        self.id: int = data.get("id", 0)
        self.image: str = data.get("image", "")
        self.md5: str = data.get("md5", "")
        self.owner: str = data.get("owner", "")
        self.parent_id: Optional[int] = data.get("parent_id")
        self.post_locked: Optional[int] = data.get("post_locked")
        self.post_url: Optional[URL] = str_to_url(data, "post_url")
        self.preview_height: int = data.get("preview_height", 0)
        self.preview_url: Optional[URL] = str_to_url(data, "preview_url")
        self.preview_width: int = data.get("preview_width", 0)
        self.rating: str = data.get("rating", "")
        self.sample: int = data.get("sample", 0)
        self.sample_height: int = data.get("sample_height", 0)
        self.sample_url: Optional[URL] = str_to_url(data, "sample_url")
        self.sample_width: int = data.get("sample_width", 0)
        self.score: Union[int, None] = data.get("score")
        self.source: Optional[URL] = str_to_url(data, "source")
        self.status: str = data.get("status", "")
        self.tags: List[str] = data.get("tags", "").split(" ")
        self.title: str = data.get("title", "")
        self.width: int = data.get("width", 0)


class Rule34:
    def __init__(self, data: dict):
        self.change: int = data.get("change", 0)
        self.comment_count: int = data.get("comment_count", 0)
        self.directory: int = data.get("directory", 0)
        self.file_url: Optional[URL] = str_to_url(data, "file_url")
        self.has_notes: bool = data.get("has_notes", False)
        self.hash: str = data.get("hash", "")
        self.height: int = data.get("height", 0)
        self.id: int = data.get("id", 0)
        self.image: str = data.get("image", "")
        self.owner: str = data.get("owner", "")
        self.parent_id: int = data.get("parent_id", 0)
        self.post_url: Optional[URL] = str_to_url(data, "post_url")
        self.preview_url: Optional[URL] = str_to_url(data, "preview_url")
        self.rating: str = data.get("rating", "")
        self.sample: bool = data.get("sample", False)
        self.sample_height: int = data.get("sample_height", 0)
        self.sample_url: Optional[URL] = str_to_url(data, "sample_url")
        self.sample_width: int = data.get("sample_width", 0)
        self.score: Union[int, None] = data.get("score")
        self.source: Optional[URL] = str_to_url(data, "source")
        self.status: str = data.get("status", "")
        self.tags: List[str] = data.get("tags", "").split(" ")
        self.width: int = data.get("width", 0)


class Tbib:
    def __init__(self, data: dict):
        self.change: int = data.get("change", 0)
        self.directory: int = data.get("directory", 0)
        self.file_url: URL = str_to_url(data, "file_url")
        self.hash: str = data.get("hash", "")
        self.height: int = data.get("height", 0)
        self.id: int = data.get("id", 0)
        self.image: str = data.get("image", "")
        self.owner: str = data.get("owner", "")
        self.parent_id: int = data.get("parent_id", 0)
        self.post_url: URL = str_to_url(data, "post_url")
        self.rating: str = data.get("rating", "")
        self.sample: int = data.get("sample", 0)
        self.sample_height: int = data.get("sample_height", 0)
        self.sample_width: int = data.get("sample_width", 0)
        self.score: Union[int, None] = data.get("score")
        self.tags: List[str] = data.get("tags", "").split(" ")
        self.width: int = data.get("width", 0)


class Safebooru:
    def __init__(self, data: dict):
        self.change: int = data.get("change", 0)
        self.directory: int = data.get("directory", 0)
        self.file_url: URL = str_to_url(data, "file_url")
        self.hash: str = data.get("hash", "")
        self.height: int = data.get("height", 0)
        self.id: int = data.get("id", 0)
        self.image: str = data.get("image", "")
        self.owner: str = data.get("owner", "")
        self.parent_id: int = data.get("parent_id", 0)
        self.post_url: URL = str_to_url(data, "post_url")
        self.rating: str = data.get("rating", "")
        self.sample: int = data.get("sample", 0)
        self.sample_height: int = data.get("sample_height", 0)
        self.sample_width: int = data.get("sample_width", 0)
        self.score: Union[int, None] = data.get("score")
        self.tags: List[str] = data.get("tags", "").split(" ")
        self.width: int = data.get("width", 0)


class Xbooru:
    def __init__(self, data: dict):
        self.change: int = data.get("change", 0)
        self.directory: int = data.get("directory", 0)
        self.file_url: URL = str_to_url(data, "file_url")
        self.hash: str = data.get("hash", "")
        self.height: int = data.get("height", 0)
        self.id: int = data.get("id", 0)
        self.image: str = data.get("image", "")
        self.owner: str = data.get("owner", "")
        self.parent_id: int = data.get("parent_id", 0)
        self.post_url: URL = str_to_url(data, "post_url")
        self.rating: str = data.get("rating", "")
        self.sample: int = data.get("sample", 0)
        self.sample_height: int = data.get("sample_height", 0)
        self.sample_width: int = data.get("sample_width", 0)
        self.score: Union[int, None] = data.get("score")
        self.tags: List[str] = data.get("tags", "").split(" ")
        self.width: int = data.get("width", 0)


class Realbooru:
    def __init__(self, data: dict):
        self.change: int = data.get("change", 0)
        self.directory: int = data.get("directory", 0)
        self.file_url: URL = str_to_url(data, "file_url")
        self.hash: str = data.get("hash", "")
        self.height: int = data.get("height", 0)
        self.id: int = data.get("id", 0)
        self.image: str = data.get("image", "")
        self.owner: str = data.get("owner", "")
        self.parent_id: int = data.get("parent_id", 0)
        self.post_url: URL = str_to_url(data, "post_url")
        self.rating: str = data.get("rating", "")
        self.sample: int = data.get("sample", 0)
        self.sample_height: int = data.get("sample_height", 0)
        self.sample_width: int = data.get("sample_width", 0)
        self.score: Union[int, None] = data.get("score")
        self.tags: List[str] = data.get("tags", "").split(" ")
        self.width: int = data.get("width", 0)


class Hypnohub:
    def __init__(self, data: dict):
        self.change: int = data.get("change", 0)
        self.directory: int = data.get("directory", 0)
        self.file_url: URL = str_to_url(data, "file_url")
        self.hash: str = data.get("hash", "")
        self.height: int = data.get("height", 0)
        self.id: int = data.get("id", 0)
        self.image: str = data.get("image", "")
        self.owner: str = data.get("owner", "")
        self.parent_id: int = data.get("parent_id", 0)
        self.post_url: URL = str_to_url(data, "post_url")
        self.preview_url: URL = str_to_url(data, "preview_url")
        self.rating: str = data.get("rating", "")
        self.sample: int = data.get("sample", 0)
        self.sample_height: int = data.get("sample_height", 0)
        self.sample_url: URL = str_to_url(data, "sample_url")
        self.sample_width: int = data.get("sample_width", 0)
        self.score: Union[int, None] = data.get("score")
        self.tags: List[str] = data.get("tags", "").split(" ")
        self.width: int = data.get("width", 0)


class Variants:
    def __init__(self, data: dict):
        self.file_ext: str = data.get("file_ext")
        self.height: int = data.get("height")
        self.type: str = data.get("type")
        self.url: URL = str_to_url(data, "url")
        self.width: int = data.get("width")


class MediaAsset:
    def __init__(self, data: Dict[str, Union[str, int, bool, None]]) -> None:
        self.created_at: Optional[datetime] = parse_datetime(
            data, "created_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.duration: Optional[str] = data.get("duration")
        self.file_ext: Optional[str] = data.get("file_ext")
        self.file_size: Optional[int] = data.get("file_size")
        self.id: Optional[int] = data.get("id")
        self.image_height: Optional[int] = data.get("image_height")
        self.image_width: Optional[int] = data.get("image_width")
        self.is_public: Optional[bool] = data.get("is_public")
        self.md5: Optional[str] = data.get("md5")
        self.pixel_hash: Optional[str] = data.get("pixel_hash")
        self.status: Optional[str] = data.get("status")
        self.updated_at: Optional[datetime] = parse_datetime(
            data, "updated_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.variants: Optional[List[Variants]] = [
            Variants(variant) for variant in data.get("variants", [])
        ]


class Danbooru:
    def __init__(
        self, data: Dict[str, Union[str, int, bool, None, MediaAsset]]
    ) -> None:
        self.approver_id: Optional[int] = data.get("approver_id")
        self.bit_flags: Optional[int] = data.get("bit_flags", 0)
        self.created_at: Optional[datetime] = parse_datetime(
            data, "created_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.down_score: Optional[int] = data.get("down_score", 0)
        self.fav_count: Optional[int] = data.get("fav_count", 0)
        self.file_ext: Optional[str] = data.get("file_ext")
        self.file_size: Optional[int] = data.get("file_size", 0)
        self.file_url: Optional[URL] = str_to_url(data, "file_url")
        self.has_active_children: Optional[bool] = data.get(
            "has_active_children", False
        )
        self.has_children: Optional[bool] = data.get("has_children", False)
        self.has_large: Optional[bool] = data.get("has_large", False)
        self.has_visible_children: Optional[bool] = data.get(
            "has_visible_children", False
        )
        self.id: Optional[int] = data.get("id", 0)
        self.image_height: Optional[int] = data.get("image_height", 0)
        self.image_width: Optional[int] = data.get("image_width", 0)
        self.is_banned: Optional[bool] = data.get("is_banned", False)
        self.is_deleted: Optional[bool] = data.get("is_deleted", False)
        self.is_flagged: Optional[bool] = data.get("is_flagged", False)
        self.is_pending: Optional[bool] = data.get("is_pending", False)
        self.last_comment_bumped_at: Optional[datetime] = parse_datetime(
            data, "last_comment_bumped_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.last_commented_at: Optional[datetime] = parse_datetime(
            data, "last_commented_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.last_noted_at: Optional[datetime] = parse_datetime(
            data, "last_noted_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.md5: Optional[str] = data.get("md5", "")
        self.media_asset: MediaAsset = MediaAsset(data.get("media_asset", {}))
        self.parent_id: Optional[int] = data.get("parent_id")
        self.pixiv_id: Optional[int] = data.get("pixiv_id", 0)
        self.post_url: Optional[URL] = str_to_url(data, "post_url")
        self.preview_file_url: Optional[URL] = str_to_url(data, "preview_file_url")
        self.rating: Optional[str] = data.get("rating", "")
        self.score: Optional[int] = data.get("score", 0)
        self.source: Optional[URL] = str_to_url(data, "source")
        self.tag_count: Optional[int] = data.get("tag_count", 0)
        self.tag_count_artist: Optional[int] = data.get("tag_count_artist", 0)
        self.tag_count_character: Optional[int] = data.get("tag_count_character", 0)
        self.tag_count_copyright: Optional[int] = data.get("tag_count_copyright", 0)
        self.tag_count_general: Optional[int] = data.get("tag_count_general", 0)
        self.tag_count_meta: Optional[int] = data.get("tag_count_meta", 0)
        self.tag_string: List[str] = data.get("tag_string", "").split(" ")
        self.tag_string_artist: Optional[str] = data.get("tag_string_artist", "")
        self.tag_string_character: Optional[str] = data.get("tag_string_character", "")
        self.tag_string_copyright: Optional[str] = data.get("tag_string_copyright", "")
        self.tag_string_general: List[str] = data.get("tag_string_general", "").split(
            " "
        )
        self.tag_string_meta: Optional[str] = data.get("tag_string_meta", "")
        self.up_score: Optional[int] = data.get("up_score", 0)
        self.updated_at: Optional[datetime] = parse_datetime(
            data, "updated_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.uploader_id: Optional[int] = data.get("uploader_id", 0)


class Atfbooru:
    def __init__(
        self, data: Dict[str, Union[str, int, bool, None, MediaAsset]]
    ) -> None:
        self.approver_id: Optional[int] = data.get("approver_id")
        self.bit_flags: Optional[int] = data.get("bit_flags", 0)
        self.created_at: Optional[datetime] = parse_datetime(
            data, "created_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.down_score: Optional[int] = data.get("down_score", 0)
        self.fav_count: Optional[int] = data.get("fav_count", 0)
        self.file_ext: Optional[str] = data.get("file_ext")
        self.file_size: Optional[int] = data.get("file_size", 0)
        self.file_url: Optional[URL] = str_to_url(data, "file_url")
        self.has_active_children: Optional[bool] = data.get(
            "has_active_children", False
        )
        self.has_children: Optional[bool] = data.get("has_children", False)
        self.has_large: Optional[bool] = data.get("has_large", False)
        self.has_visible_children: Optional[bool] = data.get(
            "has_visible_children", False
        )
        self.id: Optional[int] = data.get("id", 0)
        self.image_height: Optional[int] = data.get("image_height", 0)
        self.image_width: Optional[int] = data.get("image_width", 0)
        self.is_banned: Optional[bool] = data.get("is_banned", False)
        self.is_deleted: Optional[bool] = data.get("is_deleted", False)
        self.is_flagged: Optional[bool] = data.get("is_flagged", False)
        self.is_pending: Optional[bool] = data.get("is_pending", False)
        self.last_comment_bumped_at: Optional[datetime] = parse_datetime(
            data, "last_comment_bumped_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.last_commented_at: Optional[datetime] = parse_datetime(
            data, "last_commented_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.last_noted_at: Optional[datetime] = parse_datetime(
            data, "last_noted_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.md5: Optional[str] = data.get("md5", "")
        self.media_asset: MediaAsset = MediaAsset(data.get("media_asset", {}))
        self.parent_id: Optional[int] = data.get("parent_id")
        self.pixiv_id: Optional[int] = data.get("pixiv_id", 0)
        self.post_url: Optional[URL] = str_to_url(data, "post_url")
        self.preview_file_url: Optional[URL] = str_to_url(data, "preview_file_url")
        self.rating: Optional[str] = data.get("rating", "")
        self.score: Optional[int] = data.get("score", 0)
        self.source: Optional[URL] = str_to_url(data, "source")
        self.tag_count: Optional[int] = data.get("tag_count", 0)
        self.tag_count_artist: Optional[int] = data.get("tag_count_artist", 0)
        self.tag_count_character: Optional[int] = data.get("tag_count_character", 0)
        self.tag_count_copyright: Optional[int] = data.get("tag_count_copyright", 0)
        self.tag_count_general: Optional[int] = data.get("tag_count_general", 0)
        self.tag_count_meta: Optional[int] = data.get("tag_count_meta", 0)
        self.tag_string: List[str] = data.get("tag_string", "").split(" ")
        self.tag_string_artist: Optional[str] = data.get("tag_string_artist", "")
        self.tag_string_character: Optional[str] = data.get("tag_string_character", "")
        self.tag_string_copyright: Optional[str] = data.get("tag_string_copyright", "")
        self.tag_string_general: List[str] = data.get("tag_string_general", "").split(
            " "
        )
        self.tag_string_meta: Optional[str] = data.get("tag_string_meta", "")
        self.up_score: Optional[int] = data.get("up_score", 0)
        self.updated_at: Optional[datetime] = datetime.strptime(
            data.get("updated_at", ""), "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.uploader_id: Optional[int] = data.get("uploader_id", 0)


class Yandere:
    def __init__(self, data: dict):
        self.actual_preview_height: Optional[int] = data.get("actual_preview_height")
        self.actual_preview_width: Optional[int] = data.get("actual_preview_width")
        self.approver_id: Optional[int] = data.get("approver_id")
        self.author: Optional[str] = data.get("author")
        self.change: Optional[int] = data.get("change")
        self.created_at: Optional[datetime] = parse_datetime(
            data, "created_at", "timestamp"
        )
        self.creator_id: Optional[int] = data.get("creator_id")
        self.file_ext: Optional[str] = data.get("file_ext")
        self.file_size: Optional[int] = data.get("file_size")
        self.file_url: Optional[URL] = str_to_url(data, "file_url")
        self.frames: List[str] = data.get("frames", [])
        self.frames_pending: List[str] = data.get("frames_pending", [])
        self.frames_pending_string: str = data.get("frames_pending_string", "")
        self.frames_string: str = data.get("frames_string", "")
        self.has_children: Optional[bool] = data.get("has_children")
        self.height: Optional[int] = data.get("height")
        self.id: Optional[int] = data.get("id")
        self.is_held: Optional[bool] = data.get("is_held")
        self.is_note_locked: Optional[bool] = data.get("is_note_locked")
        self.is_pending: Optional[bool] = data.get("is_pending")
        self.is_rating_locked: Optional[bool] = data.get("is_rating_locked")
        self.is_shown_in_index: Optional[bool] = data.get("is_shown_in_index")
        self.jpeg_file_size: Optional[int] = data.get("jpeg_file_size")
        self.jpeg_height: Optional[int] = data.get("jpeg_height")
        self.jpeg_url: Optional[URL] = str_to_url(data, "jpeg_url")
        self.jpeg_width: Optional[int] = data.get("jpeg_width")
        self.last_commented_at: Optional[int] = data.get("last_commented_at")
        self.last_noted_at: Optional[int] = data.get("last_noted_at")
        self.md5: Optional[str] = data.get("md5")
        self.parent_id: Optional[int] = data.get("parent_id")
        self.post_url: Optional[URL] = str_to_url(data, "post_url")
        self.preview_height: Optional[int] = data.get("preview_height")
        self.preview_url: Optional[URL] = str_to_url(data, "preview_url")
        self.preview_width: Optional[int] = data.get("preview_width")
        self.rating: Optional[str] = data.get("rating")
        self.sample_file_size: Optional[int] = data.get("sample_file_size")
        self.sample_height: Optional[int] = data.get("sample_height")
        self.sample_url: Optional[URL] = str_to_url(data, "sample_url")
        self.sample_width: Optional[int] = data.get("sample_width")
        self.score: Optional[int] = data.get("score")
        self.source: Optional[URL] = str_to_url(data, "source")
        self.status: Optional[str] = data.get("status")
        self.tags: Optional[List[str]] = data.get("tags").split(" ")
        self.updated_at: Optional[datetime] = parse_datetime(
            data, "updated_at", "timestamp"
        )
        self.width: Optional[int] = data.get("width")


class Konachan:
    def __init__(self, data: dict):
        self.actual_preview_height: Optional[int] = data.get("actual_preview_height")
        self.actual_preview_width: Optional[int] = data.get("actual_preview_width")
        self.approver_id: Optional[int] = data.get("approver_id")
        self.author: Optional[str] = data.get("author")
        self.change: Optional[int] = data.get("change")
        self.created_at: Optional[datetime] = parse_datetime(
            data, "created_at", "timestamp"
        )
        self.creator_id: Optional[int] = data.get("creator_id")
        self.file_ext: Optional[str] = data.get("file_ext")
        self.file_size: Optional[int] = data.get("file_size")
        self.file_url: Optional[URL] = str_to_url(data, "file_url")
        self.frames: List[str] = data.get("frames", [])
        self.frames_pending: List[str] = data.get("frames_pending", [])
        self.frames_pending_string: str = data.get("frames_pending_string", "")
        self.frames_string: str = data.get("frames_string", "")
        self.has_children: Optional[bool] = data.get("has_children")
        self.height: Optional[int] = data.get("height")
        self.id: Optional[int] = data.get("id")
        self.is_held: Optional[bool] = data.get("is_held")
        self.is_note_locked: Optional[bool] = data.get("is_note_locked")
        self.is_pending: Optional[bool] = data.get("is_pending")
        self.is_rating_locked: Optional[bool] = data.get("is_rating_locked")
        self.is_shown_in_index: Optional[bool] = data.get("is_shown_in_index")
        self.jpeg_file_size: Optional[int] = data.get("jpeg_file_size")
        self.jpeg_height: Optional[int] = data.get("jpeg_height")
        self.jpeg_url: Optional[URL] = str_to_url(data, "jpeg_url")
        self.jpeg_width: Optional[int] = data.get("jpeg_width")
        self.last_commented_at: Optional[int] = data.get("last_commented_at")
        self.last_noted_at: Optional[int] = data.get("last_noted_at")
        self.md5: Optional[str] = data.get("md5")
        self.parent_id: Optional[int] = data.get("parent_id")
        self.post_url: Optional[URL] = str_to_url(data, "post_url")
        self.preview_height: Optional[int] = data.get("preview_height")
        self.preview_url: Optional[URL] = str_to_url(data, "preview_url")
        self.preview_width: Optional[int] = data.get("preview_width")
        self.rating: Optional[str] = data.get("rating")
        self.sample_file_size: Optional[int] = data.get("sample_file_size")
        self.sample_height: Optional[int] = data.get("sample_height")
        self.sample_url: Optional[URL] = str_to_url(data, "sample_url")
        self.sample_width: Optional[int] = data.get("sample_width")
        self.score: Optional[int] = data.get("score")
        self.source: Optional[URL] = str_to_url(data, "source")
        self.status: Optional[str] = data.get("status")
        self.tags: Optional[List[str]] = data.get("tags").split(" ")
        self.updated_at: Optional[datetime] = parse_datetime(
            data, "updated_at", "timestamp"
        )
        self.width: Optional[int] = data.get("width")


class Konachan_Net:
    def __init__(self, data: dict):
        self.actual_preview_height: Optional[int] = data.get("actual_preview_height")
        self.actual_preview_width: Optional[int] = data.get("actual_preview_width")
        self.approver_id: Optional[int] = data.get("approver_id")
        self.author: Optional[str] = data.get("author")
        self.change: Optional[int] = data.get("change")
        self.created_at: Optional[datetime] = parse_datetime(
            data, "created_at", "timestamp"
        )
        self.creator_id: Optional[int] = data.get("creator_id")
        self.file_ext: Optional[str] = data.get("file_ext")
        self.file_size: Optional[int] = data.get("file_size")
        self.file_url: Optional[URL] = str_to_url(data, "file_url")
        self.frames: List[str] = data.get("frames", [])
        self.frames_pending: List[str] = data.get("frames_pending", [])
        self.frames_pending_string: str = data.get("frames_pending_string", "")
        self.frames_string: str = data.get("frames_string", "")
        self.has_children: Optional[bool] = data.get("has_children")
        self.height: Optional[int] = data.get("height")
        self.id: Optional[int] = data.get("id")
        self.is_held: Optional[bool] = data.get("is_held")
        self.is_note_locked: Optional[bool] = data.get("is_note_locked")
        self.is_pending: Optional[bool] = data.get("is_pending")
        self.is_rating_locked: Optional[bool] = data.get("is_rating_locked")
        self.is_shown_in_index: Optional[bool] = data.get("is_shown_in_index")
        self.jpeg_file_size: Optional[int] = data.get("jpeg_file_size")
        self.jpeg_height: Optional[int] = data.get("jpeg_height")
        self.jpeg_url: Optional[URL] = str_to_url(data, "jpeg_url")
        self.jpeg_width: Optional[int] = data.get("jpeg_width")
        self.last_commented_at: Optional[int] = data.get("last_commented_at")
        self.last_noted_at: Optional[int] = data.get("last_noted_at")
        self.md5: Optional[str] = data.get("md5")
        self.parent_id: Optional[int] = data.get("parent_id")
        self.post_url: Optional[URL] = str_to_url(data, "post_url")
        self.preview_height: Optional[int] = data.get("preview_height")
        self.preview_url: Optional[URL] = str_to_url(data, "preview_url")
        self.preview_width: Optional[int] = data.get("preview_width")
        self.rating: Optional[str] = data.get("rating")
        self.sample_file_size: Optional[int] = data.get("sample_file_size")
        self.sample_height: Optional[int] = data.get("sample_height")
        self.sample_url: Optional[URL] = str_to_url(data, "sample_url")
        self.sample_width: Optional[int] = data.get("sample_width")
        self.score: Optional[int] = data.get("score")
        self.source: Optional[URL] = str_to_url(data, "source")
        self.status: Optional[str] = data.get("status")
        self.tags: Optional[List[str]] = data.get("tags").split(" ")
        self.updated_at: Optional[datetime] = parse_datetime(
            data, "updated_at", "timestamp"
        )
        self.width: Optional[int] = data.get("width")


class Lolibooru:
    def __init__(self, data: dict):
        self.change: int = data.get("change", 0)
        self.directory: int = data.get("directory", 0)
        self.file_url: URL = URL(data, "file_url")
        self.hash: str = data.get("hash", "")
        self.height: int = data.get("height", 0)
        self.id: int = data.get("id", 0)
        self.image: str = data.get("image", "")
        self.owner: str = data.get("owner", "")
        self.parent_id: int = data.get("parent_id", 0)
        self.post_url: URL = URL(data, "post_url")
        self.rating: str = data.get("rating", "")
        self.sample: int = data.get("sample", 0)
        self.sample_height: int = data.get("sample_height", 0)
        self.sample_width: int = data.get("sample_width", 0)
        self.score: Union[int, None] = data.get("score")
        self.tags: List[str] = data.get("tags", "").split(" ")
        self.width: int = data.get("width", 0)


class File:
    def __init__(self, data: dict):
        self.ext: str = data.get("ext", "")
        self.height: int = data.get("height", 0)
        self.md5: str = data.get("md5", "")
        self.size: int = data.get("size", 0)
        self.url: URL = str_to_url(data, "url")
        self.width: int = data.get("width", 0)


class Flags:
    def __init__(self, data: dict):
        self.deleted: bool = data.get("deleted", False)
        self.flagged: bool = data.get("flagged", False)
        self.note_locked: bool = data.get("note_locked", False)
        self.pending: bool = data.get("pending", False)
        self.rating_locked: bool = data.get("rating_locked", False)
        self.status_locked: bool = data.get("status_locked", False)


class Preview:
    def __init__(self, data: dict):
        self.height: int = data.get("height", 0)
        self.url: URL = str_to_url(data, "url")
        self.width: int = data.get("width", 0)


class Relationships:
    def __init__(self, data: dict):
        self.children: List[int] = data.get("children", [])
        self.has_active_children: bool = data.get("has_active_children", False)
        self.has_children: bool = data.get("has_children", False)
        self.parent_id: Optional[int] = data.get("parent_id")


class Alternates:
    def __init__(self, data: dict):
        self.height: int = data.get("height", 0)
        self.url: URL = str_to_url(data, "url")
        self.width: int = data.get("width", 0)


class Sample:
    def __init__(self, data: dict):
        self.alternates: dict = data.get("alternates", {})
        self.has: bool = data.get("has", False)
        self.height: int = data.get("height", 0)
        self.url: URL = str_to_url(data, "url")
        self.width: int = data.get("width", 0)


class Score:
    def __init__(self, data: dict):
        self.down: int = data.get("down", 0)
        self.total: int = data.get("total", 0)
        self.up: int = data.get("up", 0)


class Tags:
    def __init__(self, data: dict):
        self.artist: List[str] = data.get("artist", [])
        self.character: List[str] = data.get("character", [])
        self.copyright: List[str] = data.get("copyright", [])
        self.general: List[str] = data.get("general", [])
        self.invalid: List[str] = data.get("invalid", [])
        self.lore: List[str] = data.get("lore", [])
        self.meta: List[str] = data.get("meta", [])
        self.species: List[str] = data.get("species", [])


class E621:
    def __init__(self, data: dict):
        self.approver_id: int = data.get("approver_id", 0)
        self.change_seq: int = data.get("change_seq", 0)
        self.comment_count: int = data.get("comment_count", 0)
        self.created_at: Optional[datetime] = parse_datetime(
            data, "created_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.description: str = data.get("description", "")
        self.duration: Optional[int] = data.get("duration", None)
        self.fav_count: int = data.get("fav_count", 0)
        self.file: File = File(data.get("file", {}))
        self.flags: Flags = Flags(data.get("flags", {}))
        self.has_notes: bool = data.get("has_notes", False)
        self.id: int = data.get("id", 0)
        self.is_favorited: bool = data.get("is_favorited", False)
        self.locked_tags: List[str] = data.get("locked_tags", [])
        self.pools: List[int] = data.get("pools", [])
        self.post_url: URL = str_to_url(data, "post_url")
        self.preview: Preview = Preview(data.get("preview", {}))
        self.rating: str = data.get("rating", "")
        self.relationships: Relationships = Relationships(data.get("relationships", {}))
        self.sample: Sample = Sample(data.get("sample", {}))
        self.score: Score = Score(data.get("score", {}))
        self.sources: List[str] = data.get("sources", [])
        self.tags: Tags = Tags(data.get("tags", {}))
        self.updated_at: Optional[datetime] = parse_datetime(
            data, "updated_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.uploader_id: int = data.get("uploader_id", 0)


class E926:
    def __init__(self, data: dict):
        self.approver_id: int = data.get("approver_id", 0)
        self.change_seq: int = data.get("change_seq", 0)
        self.comment_count: int = data.get("comment_count", 0)
        self.created_at: Optional[datetime] = parse_datetime(
            data, "created_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.description: str = data.get("description", "")
        self.duration: Optional[int] = data.get("duration", None)
        self.fav_count: int = data.get("fav_count", 0)
        self.file: File = File(data.get("file", {}))
        self.flags: Flags = Flags(data.get("flags", {}))
        self.has_notes: bool = data.get("has_notes", False)
        self.id: int = data.get("id", 0)
        self.is_favorited: bool = data.get("is_favorited", False)
        self.locked_tags: List[str] = data.get("locked_tags", [])
        self.pools: List[int] = data.get("pools", [])
        self.post_url: URL = str_to_url(data, "post_url")
        self.preview: Preview = Preview(data.get("preview", {}))
        self.rating: str = data.get("rating", "")
        self.relationships: Relationships = Relationships(data.get("relationships", {}))
        self.sample: Sample = Sample(data.get("sample", {}))
        self.score: Score = Score(data.get("score", {}))
        self.sources: List[str] = data.get("sources", [])
        self.tags: Tags = Tags(data.get("tags", {}))
        self.updated_at: Optional[datetime] = parse_datetime(
            data, "updated_at", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        self.uploader_id: int = data.get("uploader_id", 0)


class Intensities:
    def __init__(self, data: dict):
        self.ne: float = data.get("ne", 0.0)
        self.nw: float = data.get("nw", 0.0)
        self.se: float = data.get("se", 0.0)
        self.sw: float = data.get("sw", 0.0)


class Representations:
    def __init__(self, data: dict):
        self.full: URL = str_to_url(data, "full")
        self.large: URL = str_to_url(data, "large")
        self.medium: URL = str_to_url(data, "medium")
        self.small: URL = str_to_url(data, "small")
        self.tall: URL = str_to_url(data, "tall")
        self.thumb: URL = str_to_url(data, "thumb")
        self.thumb_small: URL = str_to_url(data, "thumb_small")
        self.thumb_tiny: URL = str_to_url(data, "thumb_tiny")


class Derpibooru:
    def __init__(self, data: dict):
        self.animated: bool = data.get("animated", False)
        self.aspect_ratio: float = data.get("aspect_ratio", 0.0)
        self.comment_count: int = data.get("comment_count", 0)
        self.created_at: datetime = parse_datetime(
            data, "created_at", "%Y-%m-%dT%H:%M:%SZ"
        )
        self.deletion_reason = data.get("deletion_reason")
        self.description: str = data.get("description", "")
        self.downvotes: int = data.get("downvotes", 0)
        self.duplicate_of = data.get("duplicate_of", None)
        self.duration: float = data.get("duration", 0.0)
        self.faves: int = data.get("faves", 0)
        self.first_seen_at: datetime = parse_datetime(
            data, "first_seen_at", "%Y-%m-%dT%H:%M:%SZ"
        )
        self.format: str = data.get("format", "")
        self.height: int = data.get("height", 0)
        self.hidden_from_users: bool = data.get("hidden_from_users", False)
        self.id: int = data.get("id", 0)
        self.intensities: Intensities = Intensities(data.get("intensities", {}))
        self.mime_type: str = data.get("mime_type", "")
        self.name: str = data.get("name", "")
        self.orig_sha512_hash: str = data.get("orig_sha512_hash", "")
        self.post_url: URL = str_to_url(data, "post_url")
        self.processed: bool = data.get("processed", False)
        self.representations: Representations = Representations(
            data.get("representations", {})
        )
        self.score: int = data.get("score", 0)
        self.sha512_hash: str = data.get("sha512_hash", "")
        self.size: int = data.get("size", 0)
        self.source_url: URL = str_to_url(data, "source_url")
        self.source_urls: List[URL] = data.get("source_urls", [])
        self.spoilered: bool = data.get("spoilered", False)
        self.tag_count: int = data.get("tag_count", 0)
        self.tag_ids: List[int] = data.get("tag_ids", [])
        self.tags: List[str] = data.get("tags", [])
        self.thumbnails_generated: bool = data.get("thumbnails_generated", False)
        self.updated_at: datetime = parse_datetime(
            data, "updated_at", "%Y-%m-%dT%H:%M:%SZ"
        )
        self.uploader = data.get("uploader")
        self.uploader_id = data.get("uploader_id")
        self.upvotes: int = data.get("upvotes", 0)
        self.view_url: URL = str_to_url(data, "view_url")
        self.width: int = data.get("width", 0)
        self.wilson_score: float = data.get("wilson_score", 0.0)


class Furbooru:
    def __init__(self, data: dict):
        self.change: int = data.get("change", 0)
        self.directory: int = data.get("directory", 0)
        self.file_url: URL = URL(data, "file_url")
        self.hash: str = data.get("hash", "")
        self.height: int = data.get("height", 0)
        self.id: int = data.get("id", 0)
        self.image: str = data.get("image", "")
        self.owner: str = data.get("owner", "")
        self.parent_id: int = data.get("parent_id", 0)
        self.post_url: URL = URL(data, "post_url")
        self.rating: str = data.get("rating", "")
        self.sample: int = data.get("sample", 0)
        self.sample_height: int = data.get("sample_height", 0)
        self.sample_width: int = data.get("sample_width", 0)
        self.score: Union[int, None] = data.get("score")
        self.tags: List[str] = data.get("tags", "").split(" ")
        self.width: int = data.get("width", 0)


class CreatedAt:
    def __init__(self, data: dict):
        self.json_class: str = data.get("json_class", "")
        self.n: int = data.get("n", 0)
        self.s: datetime = parse_datetime(data, "s", "timestamp")


class Behoimi:
    def __init__(self, data: dict):
        self.author: str = data.get("author", "")
        self.change: int = data.get("change", 0)
        self.created_at: CreatedAt = CreatedAt(data.get("created_at", {}))
        self.creator_id: int = data.get("creator_id", 0)
        self.file_size: int = data.get("file_size", 0)
        self.file_url: URL = str_to_url(data, "file_url")
        self.has_children: bool = data.get("has_children", False)
        self.has_comments: bool = data.get("has_comments", False)
        self.has_notes: bool = data.get("has_notes", False)
        self.height: int = data.get("height", 0)
        self.id: int = data.get("id", 0)
        self.md5: str = data.get("md5", "")
        self.parent_id = data.get("parent_id", None)
        self.post_url: URL = str_to_url(data, "post_url")
        self.preview_height: int = data.get("preview_height", 0)
        self.preview_url: URL = str_to_url(data, "preview_url")
        self.preview_width: int = data.get("preview_width", 0)
        self.rating: str = data.get("rating", "")
        self.sample_height: int = data.get("sample_height", 0)
        self.sample_url: URL = str_to_url(data, "sample_url")
        self.sample_width: int = data.get("sample_width", 0)
        self.score: int = data.get("score", 0)
        self.source: str = data.get("source", "")
        self.status: str = data.get("status", "")
        self.tags: str = data.get("tags", "").split(" ")
        self.width: int = data.get("width", 0)


class Paheal:
    def __init__(self, data: dict):
        self.author: str = data.get("@author", "")
        self.date: datetime = parse_datetime(data, "@date", "%Y-%m-%d %H:%M:%S")
        self.file_name: str = data.get("@file_name", "")
        self.file_url: URL = str_to_url(data, "@file_url")
        self.height: int = int(data.get("@height", 0))
        self.id: int = int(data.get("@id", 0))
        self.md5: str = data.get("@md5", "")
        self.preview_height: str = int(data.get("@preview_height", 0))
        self.preview_url: URL = None  # tenho que entender como funciona
        self.preview_width = int(data.get("@preview_width", 0))
        self.rating = data.get("@rating", "")
        self.score = int(data.get("@score", 0))
        self.source = data.get("@source", "")
        self.tags = data.get("@tags", "").split()  # Split tags into list
        self.width = int(data.get("@width", 0))
