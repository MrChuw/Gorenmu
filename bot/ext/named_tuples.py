# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
from typing import NamedTuple, TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from bot.models import Alias
    from bot.models import Status


class AliasCached(NamedTuple):
    alias: Alias
    invocation: str
    arguments: list[str]
    parent: Optional[Alias] = None


class RAfkNamedTuple(NamedTuple):
    content: str
    updated_at: datetime.datetime
    alias: str
    afk: Status









