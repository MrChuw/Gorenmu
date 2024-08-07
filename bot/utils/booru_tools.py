# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import time

import numpy as np
from aiohttp_client_cache import RedisBackend, SQLiteBackend
from bs4 import BeautifulSoup
from yarl import URL

from bot.apis import booru
from bot.ext.commands import Context
from bot.utils import Selenium


class BooruTools:
    # TODO: Linha de baixo.
    #  NO FUTURO COLOCAR PARA QUE TODOS OS LINKS QUE VÊM COMO RESPOSTA SEJAM SALVOS NO BANCO DE DADOS, E SO GERAR MAIS SE NÃO TIVER MAIS NENHUM LINK NÃO JA ENVIADO.
    #  EXEMPLO: SALVAR TODAS AS INFOS DOS JSON, MAIS UM CAMPO DE "JA ENVIADO" COMO BOOL SE O LINK JA FOI ENVIADO OU NÃO E O CAMPO DE QUAL BOORU PERTENCE.
    #  ANTES DE GERAR UMA IMAGEM VERIFICA NO BANCO DE DADOS SE NÃO TÊM NENHUM LINK QUE AINDA NÃO FOI ENVIADO E SE TIVER ENVIA AO INVEZ DE GERAR IMAGEM NOVAS.
    #  Talvez usar o bagulho que envia as imagens para o im.mrchuw.com.br para enviar daqui tbm?

    def __init__(self, cache: SQLiteBackend | RedisBackend):
        self.Booru = booru.Booru
        self.boorus = {0: self.Booru().gelbooru(cache), 1: self.Booru().rule34(cache), 2: self.Booru().tbib(cache),
                       3: self.Booru().safebooru(cache), 4: self.Booru().xbooru(cache),
                       5: self.Booru().realbooru(cache), 6: self.Booru().hypnohub(cache),
                       7: self.Booru().danbooru(cache), 9: self.Booru().yandere(cache),
                       10: self.Booru().konachan(cache), 11: self.Booru().konachan_net(cache),
                       13: self.Booru().e621(cache), 14: self.Booru().e926(cache), 15: self.Booru().derpibooru(cache),
                       16: self.Booru().furbooru(cache), 17: self.Booru().paheal(cache),
                       18: self.Booru().behoimi(cache),
                       }
        self.tags_permitidas = {"booru": 10, "glbo": 10, "dnbo": 10, "rule34": 10, "rlbo": 10, "tbibo": 10, "xbbo": 10,
                                "sfbo": 10, "ynbo": 10, "Knbo": 10, "hybo": 10, "e621bo": 10, "e926bo": 10, "dpbo": 1,
                                "fubo": 1, "bhbo": 10, "phbo": 3, "knnbo": 6, "atfbo": 20,
                                }
        self.seconds = {"booru": 15, "glbo": 15, "dnbo": 15, "rule34": 15, "rlbo": 15, "tbibo": 15, "xbbo": 15,
                        "sfbo": 15, "ynbo": 15, "knbo": 15, "hybo": 15, "e621bo": 15, "e926bo": 15, "dpbo": 15,
                        "fubo": 15, "bhbo": 15, "phbo": 15, "knnbo": 15, "atfbo": 15,
                        }

    @staticmethod
    async def annoying(url: URL, booru_number: int):
        url = url.human_repr()
        driver = await Selenium.prepare_driver()
        if booru_number == 7:
            driver.get(url)
            await asyncio.sleep(2)
            url = driver.page_source
            soup = BeautifulSoup(url, "html.parser")
            img_tag = soup.find("picture").find("img")
            src_url = img_tag.get("src")
            driver.close()
            return URL(src_url)

    async def generate_img_link(self, args: str, booru_number: int):
        chosen_booru = self.Booru()
        if args is not None:
            res = await chosen_booru.search(self.boorus[booru_number], query=args)
        else:
            res = await chosen_booru.search(self.boorus[booru_number], query="")
        if res is None:
            return None
        return self.boorus[booru_number].from_dict_list(res)

    async def parse(self, amount: int, dicio: dict, ctx: Context, booru_number: int):
        images = []
        images_preview = []
        final_images = []
        previews_finals = []
        image: URL
        image_preview: URL
        image_attributes = ["large_file_url", "file_url", "view_url", "source", "url", "@file_url"]
        preview_attributes = ["preview_url", "preview_file_url", "thumb", "small", "sample_url"]

        img: URL | None = None
        img_preview: URL | None = None

        for i in range(amount):
            random = np.random.choice(len(dicio))
            resolve = dicio.pop(random)

            for atribute in image_attributes:
                if not getattr(resolve, atribute, None):
                    continue
                else:
                    img = getattr(resolve, atribute)
                    break
            if not img:
                if booru_number == 7:
                    img = await self.annoying(resolve.post_url, booru_number)
                if booru_number in [13, 14]:
                    img = resolve.file.url

            for atribute in preview_attributes:
                if not getattr(resolve, atribute, None):
                    continue
                else:
                    img_preview = getattr(resolve, atribute)
                    break
            if not img_preview:
                if booru_number in [13, 14]:
                    img_preview = resolve.preview.preview.url
                if booru_number == 15:
                    img_preview = resolve.representations.thumb

            images.append(img)
            images_preview.append(img_preview)
            img = None
            img_preview = None

        tasks = []
        for image, image_preview in zip(images, images_preview):
            if image:
                tasks.append(
                        ctx.bot.UploadThings.shortener(image.human_repr(), ctx.bot, ctx.bot.BooruCachedSession.cache)
                )
            else:
                tasks.append(ctx.bot.UploadThings.shortener(None, ctx.bot, ctx.bot.BooruCachedSession.cache))

            if image_preview:
                tasks.append(ctx.bot.UploadThings.shortener(image_preview.human_repr(), ctx.bot,
                                                            ctx.bot.BooruCachedSession.cache
                                                            )
                )
            else:
                tasks.append(ctx.bot.UploadThings.shortener(None, ctx.bot, ctx.bot.BooruCachedSession.cache))

        results = await asyncio.gather(*tasks)

        for i in range(0, len(results), 2):
            final_images.append(results[i])
            previews_finals.append(results[i + 1])

        return final_images, previews_finals

    async def selection(self, args: str, booru_number: int, start_time: float, invoke_by: str, seconds: int,
                        amount: int, ctx: Context, ):
        image = None
        preview = None
        res: int | dict = 0
        attempts = 0
        while not image or not preview:
            elapsed_time = time.time() - start_time
            if invoke_by == "booru" and attempts == 11:
                return None, None
            if elapsed_time > seconds:
                return ctx.translations.SupportTools.Humanize.Humanize.precisedelta(elapsed_time), "error"
            try:
                res = await self.generate_img_link(args=args, booru_number=booru_number)
            except Exception as e:
                ctx.bot.log.error(e)
            if res is None:
                return None, None
            try:
                image, preview = await self.parse(amount=amount, dicio=res, ctx=ctx, booru_number=booru_number)
            except Exception as e:
                ctx.bot.log.error(e)
        return image, preview

    async def responder(self, ctx: Context, args: str, booru_number, start_time, invoke_by, seconds, amount):
        if invoke_by != "booru":
            await ctx.simple_response(ctx, ctx.translations.NSFW.Boru().pls_wait)
        img, img_preview = await self.selection(args=args, booru_number=booru_number, start_time=start_time,
                                                invoke_by=invoke_by, seconds=seconds, amount=amount, ctx=ctx
                                                )

        if img_preview == "error":
            return None, False, img

        response_final = None
        response = None
        if img is None and img_preview is None:
            return None, None, False

        for i in range(amount):
            if img[i]:
                response = f"Original: {img[i]}"

            if img_preview[i]:
                if response:
                    response = f"{response} || Preview: {img_preview[i]}"
                else:
                    response = f"Preview: {img_preview[i]}"

            if response:
                if response_final:
                    response_final = response_final + " " + response
                else:
                    response_final = response
        if response_final:
            return img, img_preview, response_final + " "

        return None, None, False
