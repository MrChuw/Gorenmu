# -*- coding: utf-8 -*-
from dataclasses import dataclass
import requests, pprint, json, bs4
from apis import aiorequests
import aiohttp


@dataclass
class Prediction:
    cidade: str
    condicao_do_tempo: str
    temperatura_atual: str
    temperatura_aparente: str
    pressao_atual: str
    humidade: str
    wind: str


async def get(url):
    timeout = aiohttp.ClientTimeout(total=240)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            r = await resp.read()  # or text() in this instance
            soup = bs4.BeautifulSoup(r, "html.parser")
            return soup


async def jsonget(url) -> dict:
    timeout = aiohttp.ClientTimeout(total=240)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            return await resp.json()


@dataclass
class Weather:
    async def predict(self, cidade: str) -> Prediction:
        urlloc = f"https://nominatim.openstreetmap.org/search?q={cidade}&format=json"
        json = await jsonget(urlloc)
        lat = json[0]["lat"]
        lon = json[0]["lon"]

        apiurl = f"https://api.open-meteo.com/v1/forecast?latitude={lat}9&longitude={lon}6&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"

        json = await jsonget(urlloc)
        condicao_do_tempo = json.get("", "")
        temperatura_atual = json.get("temperature", "")
        temperatura_aparente = json.get("", "")
        pressao_atual = json.get("", "")
        humidade = json.get("", "")
        wind = json.get("windspeed", "")
        return Prediction(
            cidade=cidade,
            condicao_do_tempo=condicao_do_tempo,
            temperatura_atual=temperatura_atual,
            temperatura_aparente=temperatura_aparente,
            pressao_atual=pressao_atual,
            humidade=humidade,
            wind=wind,
        )


# &current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m

# &current_weather=true&apparent_temperature,precipitation,rain,visibility&timezone=auto

# &current_weather=true&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,rain,visibility&daily=weathercode&timezone=auto

# url = f"https://www.foreca.pt/Brazil/{cidade}"
# soup = await get(url=url)

# # pega todas as colunas
# colunas = soup.find_all("div", {"class": "column split"})[0]

# # Pega a classe wind
# wind = colunas.find("div", {"class": "obs cf"}).find("div", {"class": "wind"}).text
# wind = wind.lower().replace("kmh", "km/h").replace("o ", "o de ")

# # pega a condicao do tempo
# condicao_do_tempo = colunas.find("div", {"class": "obs cf"}).find("p", {"class": "wx"}).string
# if condicao_do_tempo == "Céu geralmente limpo":
#     condicao_do_tempo = "com o céu limpo"

# # pega a temperatura atual de coluna esquerda
# temperatura_atual = colunas.find("div", {"class": "obs cf"}).find("p", {"class": "u_metrickmh"}).string
# temperatura_atual = temperatura_atual.replace("+", "")


# # pega a temperatura aparente de coluna esquerda
# lista_de_colunas = colunas.find("div", {"class": "obs cf"}).find("p", {"class": "wx"})
# tabela = lista_de_colunas.find_next_siblings()
# elementos_da_tabela = tabela[0].find_all()

# temperatura_aparente = (elementos_da_tabela[1].string.lower()) + " " + elementos_da_tabela[2].string.replace("+", "")

# pressao_atual = (elementos_da_tabela[3].string.lower()) + " " + elementos_da_tabela[5].string
# pressao_atual = pressao_atual.replace("a ", "a de ")

# humidade = (elementos_da_tabela[9].string.lower()) + " " + elementos_da_tabela[11].string
# humidade = humidade.replace("e ", "e de ")


# @dataclass
# class Weather:
#     key: str
#     url: str = "https://api.openweathermap.org/data"
#     version: str = "2.5"

#     async def predict(self, location: str) -> Prediction:
#         url = f"{self.url}/{self.version}/weather"
#         params = {"appid": self.key, "lang": "pt_br", "units": "metric", "q": location}
#         observation = await aiorequests.get(url, params=params)
#         return Prediction(
#             city=observation["name"],
#             country=observation["sys"]["country"],
#             humidity=observation["main"]["humidity"],
#             status=observation["weather"][0]["description"],
#             feels_like=observation["main"]["feels_like"],
#             temp_max=observation["main"]["temp_max"],
#             temp_min=observation["main"]["temp_min"],
#             temp_now=observation["main"]["temp"],
#             wind=observation["wind"]["speed"],
#         )
