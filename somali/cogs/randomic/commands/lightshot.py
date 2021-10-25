# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
import requests
import random
import string
from user_agent import generate_user_agent
from time import sleep
import asyncio
import datetime

aliases=['shot']
description = "Comando para mandar links aleatiros do lightshot, CUIDADO pode vir NSFW,"
usage = 'digite o comando, tendo a opção de adicionar um número de 2 a 5 para ditar a quantidade de links por vez'

async def command(ctx, quantidade: int = 1) -> None:
    startTime = datetime.datetime.now()
    count = 0
    contar = 1
    if ctx.author.name != "mr_chuw":
        if quantidade > 5:
            quantidade = 5
        while count < quantidade and 5 > count:
            contador = 1
            link1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            # sr = ''.join(random.sample(link1, 6))
            link = "https://prnt.sc/" + link1
            headers = {"user-agent": generate_user_agent()}
            html = requests.get(link, headers=headers)
            soup = BS(html.text, 'html.parser')
            image_html = soup.find("img", class_="screenshot-image")
            if image_html:
                img_url = image_html.get("src")
                file_path = img_url.split("/")[-1]
                if file_path == "0_173a7b_211be8ff.png":
                    print("No image found at " + link)
                    contador += 1
                    pass

                else:
                    if count == quantidade-1:
                        cabou = (datetime.datetime.now() - startTime)
                        await ctx.send(f'{ctx.author.name} FBBlock {img_url} levou {cabou} segundos {contar}º em {contador} tentativa(s)')
                        break
                    else:
                        await ctx.send(f'{ctx.author.name} FBBlock {img_url} o {contar}º e foram {contador} tentativas')

                count += 1
                contar += 1
    else:
        while count < quantidade:
            await asyncio.sleep(random.randrange(1, 3))
            contador = 1
            link1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            # sr = ''.join(random.sample(link1, 6))
            link = "https://prnt.sc/" + link1
            headers = {"user-agent": generate_user_agent()}
            html = requests.get(link, headers=headers)
            soup = BS(html.text, 'html.parser')
            image_html = soup.find("img", class_="screenshot-image")
            if image_html:
                img_url = image_html.get("src")
                file_path = img_url.split("/")[-1]
                if file_path == "0_173a7b_211be8ff.png":
                    print("No image found at " + link)
                    contador += 1
                    pass

                else:
                    if count == quantidade-1:
                        cabou = (datetime.datetime.now() - startTime)
                        await ctx.send(f'{ctx.author.name} FBBlock {img_url} levou {cabou} segundos {contar}º em {contador} tentativa(s)')
                        break
                    else:
                        await ctx.send(f'{ctx.author.name} FBBlock {img_url} o {contar}º e foram {contador} tentativas')

                count += 1
                contar += 1