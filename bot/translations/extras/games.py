# -*- coding: utf-8 -*-
from __future__ import annotations

import random


class Games:
    def __init__(self, data: dict):
        self.fight_options = data["fight"]

    def get_random_fight(self) -> str:
        return random.choice(self.fight_options)
