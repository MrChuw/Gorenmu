# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar

from .shared import (
    from_bool,
    from_datetime,
    from_dict,
    from_float,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_float,
)

T = TypeVar("T")


@dataclass
class Elapsed:
    ms: Optional[float] = None
    s: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Elapsed":
        assert isinstance(obj, dict)
        ms = from_union([from_float, from_none], obj.get("ms"))
        s = from_union([from_int, from_none], obj.get("s"))
        return Elapsed(ms, s)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ms is not None:
            result["ms"] = from_union([to_float, from_none], self.ms)
        if self.s is not None:
            result["s"] = from_union([from_int, from_none], self.s)
        return result


@dataclass
class Instance:
    maintainer: Optional[str] = None
    message: None = None
    country: Optional[str] = None
    city: Optional[str] = None
    flag: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Instance":
        assert isinstance(obj, dict)
        maintainer = from_union([from_str, from_none], obj.get("maintainer"))
        message = from_none(obj.get("message"))
        country = from_union([from_str, from_none], obj.get("country"))
        city = from_union([from_str, from_none], obj.get("city"))
        flag = from_union([from_str, from_none], obj.get("flag"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Instance(maintainer, message, country, city, flag, url)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.maintainer is not None:
            result["maintainer"] = from_union([from_str, from_none], self.maintainer)
        if self.message is not None:
            result["message"] = from_none(self.message)
        if self.country is not None:
            result["country"] = from_union([from_str, from_none], self.country)
        if self.city is not None:
            result["city"] = from_union([from_str, from_none], self.city)
        if self.flag is not None:
            result["flag"] = from_union([from_str, from_none], self.flag)
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class InstancesStats:
    count: Optional[int] = None
    down: Optional[int] = None

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
class Health:
    elapsed: Optional[Elapsed] = None
    instances_stats: Optional[InstancesStats] = None
    instances: Optional[Dict[str, int]] = None
    channels: Optional[int] = None
    instance: Optional[Instance] = None

    @staticmethod
    def from_dict(obj: Any) -> "Health":
        assert isinstance(obj, dict)
        elapsed = from_union([Elapsed.from_dict, from_none], obj.get("elapsed"))
        instances_stats = from_union([InstancesStats.from_dict, from_none], obj.get("instancesStats"))
        instances = from_union([lambda x: from_dict(from_int, x), from_none], obj.get("instances"))
        channels = from_union([from_int, from_none], obj.get("channels"))
        instance = from_union([Instance.from_dict, from_none], obj.get("instance"))
        return Health(elapsed, instances_stats, instances, channels, instance)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.elapsed is not None:
            result["elapsed"] = from_union([lambda x: to_class(Elapsed, x), from_none], self.elapsed)
        if self.instances_stats is not None:
            result["instancesStats"] = from_union(
                [lambda x: to_class(InstancesStats, x), from_none], self.instances_stats
            )
        if self.instances is not None:
            result["instances"] = from_union([lambda x: from_dict(from_int, x), from_none], self.instances)
        if self.channels is not None:
            result["channels"] = from_union([from_int, from_none], self.channels)
        if self.instance is not None:
            result["instance"] = from_union([lambda x: to_class(Instance, x), from_none], self.instance)
        return result


def health_from_dict(s: Any) -> Health:
    return Health.from_dict(s)


def health_to_dict(x: Health) -> Any:
    return to_class(Health, x)
