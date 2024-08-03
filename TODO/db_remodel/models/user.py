# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

import humanize
from urlextract import URLExtract

if TYPE_CHECKING:
    from bot.bot import Context

# Local

extractor = URLExtract()
extractor.update()


humanize.activate("pt_BR")


