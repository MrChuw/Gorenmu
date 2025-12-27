from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Enter the command and a city to get the weather forecast.",
            "To use: +weather (location)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Digite o comando e uma cidade para obter a previsão do tempo.",
            "Para usar: +weather (localização)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    location: ClassVar[list] = [
        pytest.param(
            "en",
            "Fortaleza, Ceará, Brazil. Clear 🌙, temperature of 24.1 °C, maximum of 35.3 °C and "
            "apparent temperature of 15.0 °C,  1012.0 hPa, 62%, 3.4km/h north",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Fortaleza, Ceará, Brazil. Céu limpo 🌙, temperatura de 24.1 °C, máxima de 35.3 °C e "
            "aparente de 15.0 °C,  1012.0 hPa, 62%, 3.4km/h norte",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    no_city: ClassVar[list] = [
        pytest.param("en", "city \"fortaleza, ceara\" not found.", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "cidade \"fortaleza, ceara\" não encontrada.", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    no_forecast: ClassVar[list] = [
        pytest.param("en", 'Weather not found for "fortaleza, ceara".', marks=pytest.mark.en, id="en"),
        pytest.param(
            "pt_BR", 'Não foi encontrado o tempo para "fortaleza, ceara".', marks=pytest.mark.pt_BR, id="pt_BR"
        ),
    ]
