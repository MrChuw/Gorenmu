# -*- coding: utf-8 -*-
import random
import sys
import requests
from somali.data.scp import get_random_number
from somali import config

if sys.version_info >= (3, 9):
    from importlib.resources import open_text
# else:
#     from importlib_resources import open_text
import requests

# aliases=['shot']
description = f"Escolhe de 1 ate 3 paginas aleatorias do wikipedia. (Caso tenha mais sugestoes de wiki mandar um sg)"
usage = 'digite o comando, "wikipedia" e uma quantidade de 1 a 3.'


async def command(ctx, repete: int = 1) -> None:
    count = 0
    while count < repete and 3 > count:
        res = requests.get("https://pt.wikipedia.org/wiki/Special:Random")
        ctx.response = f'FBBlock {res.url} .'
        count += 1



