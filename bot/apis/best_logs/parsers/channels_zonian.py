from dataclasses import dataclass
from typing import Any, TypeVar

from .shared import (
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
)

T = TypeVar("T")


@dataclass
class Channel:
    name: str | None = None
    user_id: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Channel":
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        user_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("userID"))
        return Channel(name, user_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.user_id is not None:
            result["userID"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
                ],
                self.user_id,
            )
        return result


@dataclass
class InstancesStats:
    count: int | None = None
    down: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> "InstancesStats":
        assert isinstance(obj, dict)
        count = from_union([from_int, from_none], obj.get("count"))
        down = from_union([from_int, from_none], obj.get("down"))
        return InstancesStats(count, down)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.count is not None:
            result["count"] = from_union([from_int, from_none], self.count)
        if self.down is not None:
            result["down"] = from_union([from_int, from_none], self.down)
        return result


@dataclass
class ChannelsZonian:
    instances_stats: InstancesStats | None = None
    channels: list[Channel] | None = None

    @staticmethod
    def from_dict(obj: Any) -> "ChannelsZonian":
        assert isinstance(obj, dict)
        instances_stats = from_union([InstancesStats.from_dict, from_none], obj.get("instancesStats"))
        channels = from_union([lambda x: from_list(Channel.from_dict, x), from_none], obj.get("channels"))
        return ChannelsZonian(instances_stats, channels)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.instances_stats is not None:
            result["instancesStats"] = from_union(
                [lambda x: to_class(InstancesStats, x), from_none], self.instances_stats
            )
        if self.channels is not None:
            result["channels"] = from_union(
                [lambda x: from_list(lambda x: to_class(Channel, x), x), from_none],
                self.channels,
            )
        return result


def channels_from_dict(s: Any) -> ChannelsZonian:
    return ChannelsZonian.from_dict(s)


def channels_to_dict(x: ChannelsZonian) -> Any:
    return to_class(ChannelsZonian, x)
