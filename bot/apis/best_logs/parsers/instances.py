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
class Instance:
    name: Optional[str] = None
    user_id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Instance":
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        user_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("userID"))
        return Instance(name, user_id)

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
class Instances:
    instances_stats: Optional[InstancesStats] = None
    instances: Optional[Dict[str, List[Instance]]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Instances":
        assert isinstance(obj, dict)
        instances_stats = from_union([InstancesStats.from_dict, from_none], obj.get("instancesStats"))
        instances = from_union(
            [lambda x: from_dict(lambda x: from_list(Instance.from_dict, x), x), from_none], obj.get("instances")
        )
        return Instances(instances_stats, instances)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.instances_stats is not None:
            result["instancesStats"] = from_union(
                [lambda x: to_class(InstancesStats, x), from_none], self.instances_stats
            )
        if self.instances is not None:
            result["instances"] = from_union(
                [lambda x: from_dict(lambda x: from_list(lambda x: to_class(Instance, x), x), x), from_none],
                self.instances,
            )
        return result


def instances_from_dict(s: Any) -> Instances:
    return Instances.from_dict(s)


def instances_to_dict(x: Instances) -> Any:
    return to_class(Instances, x)
