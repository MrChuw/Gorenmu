# -*- coding: utf-8 -*-



class PetInfo:
    def __init__(self, specie, name, price):
        self.specie: str = specie
        self.emoji: str = name
        self.price: int = price



class PetDict:
    def __init__(self, data: dict):
        self.pets = self.generate_pets(data["Pets Names"])

    @staticmethod
    def generate_pets(data: dict):
        pets = {}
        for pet in data:
            pets[pet] = PetInfo(specie=data[pet]["specie"], name=data[pet]["emoji"], price=data[pet]["price"])
        return pets
































