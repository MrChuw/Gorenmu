# -*- coding: utf-8 -*-
import string
import random
import requests
import asyncio
import random
import datetime
from somali.utils import roles
from somali.logger import log

description = "Comando para mandar links aleatiros do imgur, CUIDADO pode vir NSFW,"
usage = 'digite o comando, tendo a opção de adicionar um número de 2 a 5 para ditar a quantidade de links por vez'
extra_checks = [roles.owner]

async def command(ctx, quantidade: int = 1):
    count = 0
    TimeTotal = datetime.datetime.now()
    while count < quantidade:
        await asyncio.sleep(2)
        startTime = datetime.datetime.now()
        contador = 1
        BASE_URL = 'https://i.imgur.com/'
        async def get_url():
                counter = 1
                url_hash = ''
                num = random.choice("78")
                while counter < 7:
                    random_letter = random.choice(string.hexdigits)
                    url_hash += random_letter
                    counter += 1
                return BASE_URL + url_hash + '.jpg'
        
        
        while True:
            img_url = await  get_url()
            r = requests.get(img_url, allow_redirects=False) 
            autoc = 5
            # print(r.status_code)
            

            if r.url == 'https://i.imgur.com/removed.png':
                img_url = await get_url()
                r = requests.get(img_url)

            if r.status_code == 302:
                contador += 1
                # print(contador)
                img_url = await get_url()
                r = requests.get(img_url)

            else:
                if count == quantidade-1:
                    log.info('Saida final')
                    cabou = (datetime.datetime.now() - TimeTotal)
                    await ctx.send(f'{ctx.author.name} levou {cabou} e foram {contador} tentativas FBBlock {img_url}')
                    break
                else:
                    log.info('Saida secundaria')
                    cabou = (datetime.datetime.now() - startTime)
                    await ctx.send(f'{ctx.author.name} levou {cabou} e foram {contador} tentativas FBBlock {img_url}')
                    break
        log.info('Saida Loop')
        count += 1
