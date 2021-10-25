# -*- coding: utf-8 -*-
import string, random, requests, asyncio, typing as t, datetime
from collections import defaultdict
from somali.logger import log
 
description = "Comando para mandar links aleatiros do imgur, CUIDADO pode vir NSFW,"
usage = 'digite o comando, tendo a opção de adicionar um número de 2 a 5 para ditar a quantidade de links por vez'

async def command(ctx, quantidade: str = ""):
    # print(type(quantidade), quantidade)
    if quantidade.isdigit() == True:
        quantidade = int(quantidade)
    else:
        quantidade = 1
    if ctx.author.name != "mr_chuw":
        comecar = datetime.datetime.now()
        count = 0
        contar = 1
        if quantidade > 5:
            quantidade = 5
        while count < quantidade and 5 > count:
            contador = 1
            BASE_URL = 'https://i.imgur.com/'
            while True:
                url = ''.join(random.choices(string.hexdigits, k=5))
                url = BASE_URL + url + '.jpg'
                cabou = (datetime.datetime.now() - comecar)
                r = requests.get(url, allow_redirects=False)
                cabou = (datetime.datetime.now() - comecar)
            
                while r.status_code == 302:
                    contador += 1
                    break

                else:
                    if count == quantidade-1:
                        cabou = (datetime.datetime.now() - comecar)
                        await ctx.send(f'{ctx.author.name} FBBlock {url} levou {cabou} segundos {contar}º em {contador} tentativa(s)')
                        break
                    else:
                        await ctx.send(f'{ctx.author.name} FBBlock {url} o {contar}º em {contador} tentativa(s)')
                        break
                    
            contar += 1
            count += 1
    else:
        comecar = datetime.datetime.now()
        count = 0
        contar = 1
        while count < quantidade:
            contador = 1
            BASE_URL = 'https://i.imgur.com/'
            while True:
                url = ''.join(random.choices(string.hexdigits, k=5))
                url = BASE_URL + url + '.jpg'
                cabou = (datetime.datetime.now() - comecar)
                # print('pre-requeste',cabou)
                r = requests.get(url, allow_redirects=False)
                cabou = (datetime.datetime.now() - comecar)
                # print('pos-requeste',cabou)
                while r.status_code == 302:
                    contador += 1
                    break

                else:
                    if count == quantidade-1:
                        cabou = (datetime.datetime.now() - comecar)
                        # print('mandando', cabou)
                        await ctx.send(f'{ctx.author.name} FBBlock {url} levou {cabou} segundos {contar}º em {contador} tentativa(s)')
                        break
                    else:
                        await ctx.send(f'{ctx.author.name} FBBlock {url} o {contar}º em {contador} tentativa(s)')
                        break
                    
            contar += 1
            count += 1





# async def command(ctx, quantidade: int = 1):
#     comecar = datetime.datetime.now()
#     count = 0
#     contar = 1
#     if quantidade > 5:
#         quantidade = 5
#     while count < quantidade and 5 > count:
#         contador = 1
#         BASE_URL = 'https://i.imgur.com/'
#         while True:
#             url = ''.join(random.choices(string.hexdigits, k=5))
#             url = BASE_URL + url + '.jpg'
#             cabou = (datetime.datetime.now() - comecar)
#             # print('pre-requeste',cabou)
#             r = requests.get(url, allow_redirects=False)
#             # http = urllib3.PoolManager()
#             # resp = http.urlopen('GET', url, redirect=False)
#             cabou = (datetime.datetime.now() - comecar)
#             # print('pos-requeste',cabou)
        
#             while r.status_code == 302:
#                 contador += 1
#                 break
#                 # img_url = get_url()
#                 # r = requests.get(img_url)

#             else:
#                 if count == quantidade-1:
#                     cabou = (datetime.datetime.now() - comecar)
#                     # print('mandando', cabou)
#                     await ctx.send(f'{ctx.author.name} FBBlock {url} levou {cabou} segundos {contar}º em {contador} tentativa(s)')
#                     break
#                 else:
#                     await ctx.send(f'{ctx.author.name} FBBlock {url} o {contar}º em {contador} tentativa(s)')
#                     break
                
#         contar += 1
#         count += 1

        # def get_url():
        #     counter = 0
        #     url_hash = ''
        #     num = random.randint(5, 6)
        #     while counter < 1:
        #         # random_letter = random.choice(string.hexdigits)
        #         # url_hash += random_letter
        #         url_hash = ''.join(random.choices(string.hexdigits, k=5))
        #         counter += 1
            
        #     return BASE_URL + url_hash + '.jpg'



        # while True:
        #     img_url = get_url()
        #     r = requests.get(img_url, allow_redirects=False)
        #     # http = urllib3.PoolManager()
        #     # resp = http.urlopen('GET', url, redirect=False)
        
        #     while r.status_code == 302:
        #         contador += 1
        #         img_url = get_url()
        #         r = requests.get(img_url)

        #     else:
                # if count == quantidade-1:
                #     cabou = (datetime.datetime.now() - comecar)
                #     await ctx.send(f'{ctx.author.name} FBBlock {img_url} levou {cabou} segundos {contar}º em {contador} tentativa(s)')
                #     break
                # else:
                #     await ctx.send(f'{ctx.author.name} FBBlock {img_url} o {contar}º em {contador} tentativa(s)')
                #     break
                
        # contar += 1
        # count += 1