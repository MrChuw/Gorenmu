# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import io
import random
import re
from string import ascii_letters, digits
from typing import Any,  TYPE_CHECKING

import numpy as np
import pandas as pd
from aiohttp_client_cache import CachedSession
from loguru import logger
from PIL import Image
from bot.apis.deeptranslator.deep_translator import GoogleTranslator
from bot.ext.commands import Context

if TYPE_CHECKING:
    from bot.models import Channel
    from bot.bot import Gorenmu


class TimeTools:
    def __init__(self, bot):
        self.bot: Gorenmu = bot


    @staticmethod
    def find_time(content: str, pattern_time: re.Pattern) -> dict[str, int]:
        # Match cada um dos elementos de content a PATTERN_TIME e adiciona ao match_dict
        match_dict = {}
        for match in pattern_time.finditer(content):
            for k, v in match.groupdict().items():
                if v:
                    match_dict[k] = int(v)
        return match_dict

    @staticmethod
    def from_match_to_datetime( match_dict: dict) -> pd.Timedelta:
        match_dict = {k: int(v) if v else 0 for k, v in match_dict.items()}
        now = pd.Timestamp.now()
        delta = pd.DateOffset(years=match_dict.get("years", 0), months=match_dict.get("months", 0),
                              weeks=match_dict.get("weeks", 0), days=match_dict.get("days", 0),
                              hours=match_dict.get("hours", 0), minutes=match_dict.get("minutes", 0),
                              seconds=match_dict.get("seconds", 0), milliseconds=match_dict.get("milliseconds", 0),
                              microseconds=match_dict.get("microseconds", 0), )
        return now + delta - now


    # TODO: Refazer isso.
    def find_date(self, data: str) -> dict[Any, Any] | None:
        padrao1, padrao2 = (r"\b\d{1,2}/\d{1,2}/\d{2,4}(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?\b",
                            r"\b(?:\d{1,2}:\d{2}(?::\d{2})?\s+)?\d{1,2}/\d{1,2}/\d{2,4}\b",)
        padrao_horas = r"\b\d{1,2}:\d{2}(?::\d{2})?\b"
        correspondencias = re.findall(padrao1, data) or re.findall(padrao2, data) or re.findall(padrao_horas, data)
        if correspondencias:
            correspondencias = correspondencias[0].split()
            if len(correspondencias) == 1 and ":" in correspondencias[0]:
                data_hora = correspondencias[0].split(":")
                if len(data_hora) == 2:
                    for _ in range(3):
                        data_hora.append("00")
                elif len(data_hora) == 3:
                    data_hora.append("00")
                    data_hora.append("00")
                data_hora = [int(i) for i in data_hora]
                match_dict = dict(zip(["hours", "minutes", "seconds", "milliseconds", "microseconds"], data_hora))
                return match_dict
            if len(correspondencias) == 1 and "/" in correspondencias[0]:
                correspondencias.append("12:00:00")
            if len(correspondencias[0].split("/")[-1]) == 2:
                tempo_split = correspondencias[0].split("/")
                tempo_split[2] = "20" + tempo_split[2]
                correspondencias[0] = "/".join(tempo_split)
            elif len(correspondencias[1].split("/")[-1]) == 2:
                tempo_split = correspondencias[1].split("/")
                tempo_split[2] = "20" + tempo_split[2]
                correspondencias[1] = "/".join(tempo_split)

            if "/" in correspondencias[0] and len(correspondencias) == 2:
                data_data = correspondencias[0].split("/")
                data_hora = correspondencias[1].split(":")
            elif len(correspondencias) == 2 and "/" in correspondencias[1]:
                data_data = correspondencias[1].split("/")
                data_hora = correspondencias[0].split(":")
            else:
                data_data = correspondencias[0].split("/")
                data_hora = ["00", "00", "00", "00", "00"]

            if len(data_hora) == 2:
                for _ in range(3):
                    data_hora.append("00")
            elif len(data_hora) == 3:
                data_hora.append("00")
                data_hora.append("00")

            data_data = [int(i) for i in data_data]
            data_hora = [int(i) for i in data_hora]

            match_dict = dict(
                    zip(["days", "months", "years", "hours", "minutes", "seconds", "milliseconds", "microseconds", ],
                        data_data + data_hora, )
            )

            return match_dict
        return None

    def from_match_to_date(self, match_dict: dict) -> pd.Timestamp:
        delta = pd.DateOffset(year=match_dict.get("years", 0), month=match_dict.get("months", 0),
                              day=match_dict.get("days", 0), hour=match_dict.get("hours", 0),
                              minute=match_dict.get("minutes", 0), second=match_dict.get("seconds", 0),
                              microsecond=match_dict.get("microseconds", 0), )

        return pd.Timestamp.now() + delta


class ToolsTools:  # TODO: Arrumar as funções que estão aqui dentro.
    def __init__(self, bot):
        self.bot: Gorenmu = bot

    @staticmethod
    async def pixel_generate(cor_hex):
        image_tamanho = (1, 1)
        image = Image.new("RGB", image_tamanho, (int(cor_hex[1:3], 16), int(cor_hex[3:5], 16), int(cor_hex[5:7], 16)), )
        image_io = io.BytesIO()
        image.save(image_io, format="PNG")
        return image_io.getvalue()

    @staticmethod
    async def hyper_translate(content):
        languages = ["af", "sq", "am", "ar", "hy", "as", "ay", "az", "bm", "eu", "be", "bn", "bho", "bs", "bg", "ca",
                     "ceb", "ny", "zh-CN", "zh-TW", "co", "hr", "cs", "da", "dv", "doi", "nl", "EN_US", "eo", "et",
                     "ee", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el", "gn", "gu", "ht", "ha", "haw", "iw", "hi",
                     "hmn", "hu", "is", "ig", "ilo", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "rw", "gom", "ko",
                     "kri", "ku", "ckb", "lo", "la", "lv", "ln", "lt", "lg", "lb", "mk", "mai", "mg", "ms", "ml", "mt",
                     "mi", "mr", "mni-Mtei", "lus", "mn", "my", "ne", "no", "or", "om", "ps", "fa", "pl", "pt", "pa",
                     "qu", "ro", "ru", "sm", "sa", "gd", "nso", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es",
                     "su", "sw", "sv", "tg", "ta", "tt", "te", "th", "ti", "ts", "tr", "tk", "ak", "uk", "ur", "ug",
                     "uz", "vi", "cy", "xh", "yi", "yo", "zu"]

        random_languages = np.random.choice(languages)
        try:
            return await GoogleTranslator(source="auto", target=random_languages).translate(content)
        except Exception as e:
            logger.error(e)
            return content

    @staticmethod
    async def announcement(ctx: Context, content: str, target_channel: str = "all") -> None:
        target_channel = target_channel.lower()
        if target_channel == "all":
            for channel in ctx.bot.channels:
                target_channel: Channel | str = ctx.bot.channels[channel]
                if target_channel.online is not False and "announcement" not in target_channel.disabled:
                    await asyncio.sleep(0.5)
                    await ctx.bot.get_channel(channel).send(content)
        else:
            try:
                canal_canal: Channel = ctx.bot.channels[target_channel]
                if canal_canal.online is not False and "announcement" not in canal_canal.disabled:
                    return await ctx.bot.get_channel(target_channel).send(content)
            except Exception as e:
                logger.error(e)
                return await ctx.simple_response(ctx,
                                                 ctx.translations.Exceptions.ToolsExceptions.announcement.format(e)
                                                 )

    @staticmethod
    async def generate(quantidade: int, k: int, session: CachedSession):
        urls = ["https://i.imgur.com/" + "".join(random.choices(ascii_letters + digits, k=k)) + ".jpg" for _ in
                range(quantidade + 10)]
        tasks = [asyncio.create_task(session.head(url=url, allow_redirects=False)) for url in urls]
        return await asyncio.gather(*tasks)
