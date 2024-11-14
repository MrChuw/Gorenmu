# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from bot.ext.commands import Context



class Games:
    def __init__(self, data: dict):
        self.fight_options = data["fight"]


    def get_random_fight(self) -> str:
        return random.choice(self.fight_options)

































