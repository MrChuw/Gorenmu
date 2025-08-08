from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, List, Optional, Type, TypeVar, cast

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Rating(Enum):
    EXPLICIT = "explicit"
    QUESTIONABLE = "questionable"


@dataclass
class RealbooruElement:
    directory: Optional[str] = None
    hash: Optional[str] = None
    height: Optional[int] = None
    id: Optional[int] = None
    image: Optional[str] = None
    change: Optional[int] = None
    owner: Optional[str] = None
    parent_id: Optional[int] = None
    rating: Optional[Rating] = None
    sample: Optional[int] = None
    sample_height: Optional[int] = None
    sample_width: Optional[int] = None
    score: Optional[int] = None
    tags: Optional[str] = None
    width: Optional[int] = None
    url: str | None = None
    preview: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> "RealbooruElement":
        assert isinstance(obj, dict)
        directory = from_union([from_str, from_none], obj.get("directory"))
        hash = from_union([from_str, from_none], obj.get("hash"))
        height = from_union([from_int, from_none], obj.get("height"))
        id = from_union([from_int, from_none], obj.get("id"))
        image = from_union([from_str, from_none], obj.get("image"))
        change = from_union([from_int, from_none], obj.get("change"))
        owner = from_union([from_str, from_none], obj.get("owner"))
        parent_id = from_union([from_int, from_none], obj.get("parent_id"))
        rating = from_union([Rating, from_none], obj.get("rating"))
        sample = from_union([from_int, from_none], obj.get("sample"))
        sample_height = from_union([from_int, from_none], obj.get("sample_height"))
        sample_width = from_union([from_int, from_none], obj.get("sample_width"))
        score = from_union([from_int, from_none], obj.get("score"))
        tags = from_union([from_str, from_none], obj.get("tags"))
        width = from_union([from_int, from_none], obj.get("width"))
        url = f"https://realbooru.com/images/{directory}/{image}"
        preview = f"https://realbooru.com/thumbnails/{directory}/thumbnail_{image.replace('jpeg','jpg').replace('webm','jpg').replace('mp4','jpg')}"
        return RealbooruElement(
            directory,
            hash,
            height,
            id,
            image,
            change,
            owner,
            parent_id,
            rating,
            sample,
            sample_height,
            sample_width,
            score,
            tags,
            width,
            url,
            preview,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.directory is not None:
            result["directory"] = from_union([from_str, from_none], self.directory)
        if self.hash is not None:
            result["hash"] = from_union([from_str, from_none], self.hash)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.id is not None:
            result["id"] = from_union([from_int, from_none], self.id)
        if self.image is not None:
            result["image"] = from_union([from_str, from_none], self.image)
        if self.change is not None:
            result["change"] = from_union([from_int, from_none], self.change)
        if self.owner is not None:
            result["owner"] = from_union([from_str, from_none], self.owner)
        if self.parent_id is not None:
            result["parent_id"] = from_union([from_int, from_none], self.parent_id)
        if self.rating is not None:
            result["rating"] = from_union([lambda x: to_enum(Rating, x), from_none], self.rating)
        if self.sample is not None:
            result["sample"] = from_union([from_int, from_none], self.sample)
        if self.sample_height is not None:
            result["sample_height"] = from_union([from_int, from_none], self.sample_height)
        if self.sample_width is not None:
            result["sample_width"] = from_union([from_int, from_none], self.sample_width)
        if self.score is not None:
            result["score"] = from_none(self.score)
        if self.tags is not None:
            result["tags"] = from_union([from_str, from_none], self.tags)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        return result


def realbooru_from_dict(s: Any) -> List[RealbooruElement]:
    return from_list(RealbooruElement.from_dict, s)


def realbooru_to_dict(x: List[RealbooruElement]) -> Any:
    return from_list(lambda x: to_class(RealbooruElement, x), x)
