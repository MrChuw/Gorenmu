# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, NamedTuple, Optional

if TYPE_CHECKING:
    from bot.models import Alias, Status


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
