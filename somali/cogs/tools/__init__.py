# -*- coding: utf-8 -*-
from collections import namedtuple


def create_afks():
    keys = ["emoji", "afk", "isafk", "returned", "rafk"]
    values = [
        ["afk", "๐โจ", "ficou AFK", "AFK", "voltou", "AFK"],
        ["art", "๐จ", "foi desenhar", "desenhando", "desenhou", "desenhando"],
        ["brb", "๐โจ", "volta jรก", "fora", "voltou", "fora"],
        ["code", "๐ป", "foi programar", "programando", "programou", "programando"],
        ["food", "๐ฝ", "foi comer", "comendo", "comeu", "comendo"],
        ["game", "๐ฎ", "foi jogar", "jogando", "jogou", "jogando"],
        ["gn", "๐ค", "foi dormir", "dormindo", "acordou", "dormindo"],
        ["work", "๐ผ", "foi trabalhar", "trabalhando", "trabalhou", "trabalhando"],
        ["read", "๐", "foi ler", "lendo", "leu", "lendo"],
        ["shower", "๐ฟ", "foi pro banho", "no banho", "tomou banho", "o banho"],
        ["study", "๐", "foi estudar", "estudando", "estudou", "estudando"],
        ["watch", "๐บ", "foi assistir", "assistindo", "assistiu", "assistindo"],
    ]
    return {value[0]: namedtuple(value[0], keys)(*value[1:]) for value in values}


afks = create_afks()
