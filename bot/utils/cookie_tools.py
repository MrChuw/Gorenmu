# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import random
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from bot.bot import Gorenmu



class CookieTools:
    def __init__(self, bot: Gorenmu):
        self.bot: Gorenmu = bot
        self.seed: int = None
        self.multiplicador = 1

    @staticmethod
    async def calculate_reward(sequencia, recompensas, comprimento_sequencia):
        total_recompensa = 0
        index = 0

        while index < len(sequencia):
            await asyncio.sleep(0)
            current_element = sequencia[index]
            consecutive_count = 1
            while (
                index + consecutive_count < len(sequencia) and sequencia[index + consecutive_count] == current_element
            ):
                consecutive_count += 1

            if consecutive_count >= comprimento_sequencia:
                if (consecutive_count, current_element) in recompensas:
                    total_recompensa += recompensas[(consecutive_count, current_element)]
                index += consecutive_count
            else:
                index += 1

        return total_recompensa

    async def all_slotmachine(
        self,
        frutas: List[str],
        rewards: dict[tuple[int, str], int],
        quantidade,
    ):
        sequencias = [random.choices(frutas, k=5) for _ in range(quantidade)]
        recompensas_valores = [await self.calculate_reward(sequencia, rewards, 2) for sequencia in sequencias]
        recompensas = list(zip(sequencias, recompensas_valores))

        soma_total = sum(recompensas_valores)

        contagem_valores = {}
        for _, recompensa in recompensas:
            if recompensa in contagem_valores:
                contagem_valores[recompensa] += 1
            else:
                contagem_valores[recompensa] = 1

        return soma_total, contagem_valores































