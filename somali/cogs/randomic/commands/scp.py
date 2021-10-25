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
description = f"Escolhe de 1 ate 3 paginas aleatorias do scp. (Caso tenha mais sugestoes de wiki mandar um sg)"
usage = 'digite o comando, "scp" e uma quantidade de 1 a 3. (Devido ao fato de eu não ser um bom programardor esse daqui demora um pouco)'


async def command(ctx, repete: int = 1) -> None:
    count = 0
    contar = 1
    while count < repete and 3 > count:
        def get_url():
            url = f'https://scp-wiki.wikidot.com/scp-{random.randint(1, 5000)}'
            return url

        url = get_url()
        r = requests.get(url)
        while r.status_code == 404:
            url = get_url()
            r = requests.get(url)

        else:
            ctx.response = f'{ctx.author.name} FBBlock {url} o {contar}º.'
            break
        
    contar += 1
    count += 1


