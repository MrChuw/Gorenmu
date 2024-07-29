from re import S
import requests, pprint, json, bs4, aiohttp
from dataclasses import dataclass


@dataclass
class Manga:
    async def get_manga(manga):
        from bot.bot import Bot

        url = f"https://www.mangaupdates.com/search.html?search={manga.replace(' ', '+')}"

        soup = await Bot.get("normal")

        # soup = bs4.BeautifulSoup(r.text, "html.parser")

        # Find <a href="https://www.mangaupdates.com/series.html?id=" alt="Series Info">One Piece</a>
        classe1 = soup.find_all("div", class_="row no-gutters")

        # Grab de 6th element
        classe1_1 = classe1[6]

        # Find all <a> </a>1
        classe1_2 = classe1_1.find_all("a")

        # Find all <a alt="Series Info" href=
        series = []
        for classes in classe1_2:
            if classes.has_attr("alt"):
                if classes["alt"] == "Series Info":
                    series.append(classes)

        for serie in series:
            if manga.title() == serie.string.title():
                # print(serie["href")
                serie_name = serie.string
                # Printa tudo do link depois do "="
                serie_id = serie["href"][serie["href"].find("=") + 1 :]
        return serie_name, serie_id
