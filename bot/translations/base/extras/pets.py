from __future__ import annotations

from typing import Callable, List


class PetInfo:
    def __init__(self, specie, name, price):
        self.specie: str = specie
        self.emoji: str = name
        self.price: int = price


PetsDict = dict[str, PetInfo]
PetFuncCallable = Callable[[List[PetsDict]], List[PetInfo]]


def from_list_to_pet_list(pets_dict: List[PetsDict]) -> List[PetInfo]:
    return [PetInfo(specie=pet["specie"], name=pet["emoji"], price=pet["price"]) for pet in pets_dict]
