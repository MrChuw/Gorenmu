# -*- coding: utf-8 -*-

import pytest


class Params:
    decorators = [
        pytest.param(
            "en",
            "Bet your daily cookie for a chance to win more.",
            "To use: {}cookie slotmachine (all can be used to bet all unclaimed cookies quickly)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Aposte seus cookies para tentar ganhar mais.",
            "Para usar: {}cookie slotmachine "
            "(all pode ser usado para apostar todos os cookies não coletados rapidamente)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    on_cooldown = [
        pytest.param(
            "en",
            r"You're still on cooldown, wait \d+\.\d{2} seconds until the next batch! ⌛",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            r"Você ainda está em cooldown, espere \d+\.\d{2} segundos até o próximo lote! ⌛",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    invalid_amount = [
        pytest.param(
            "en",
            " You used your last available cookie and lost everything. "
            "The next one is available in 6 hours. PoroSad",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            " Você usou seu último cookie disponível e perdeu tudo. " "O próximo está disponível em 6 horas. PoroSad",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bunch_unredeemed_one = [
        pytest.param(
            "en", " You have used 1 unredeemed cookie(s) and lost everything. ", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            " Você usou 1 cookie(s) não resgatado(s) e perdeu tudo.  PoroSad",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bunch_unredeemed_all = [
        pytest.param(
            "en",
            " You have used all 5 unredeemed cookie(s) and lost everything. The next one is available in 6 hours.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            " Você usou todos 5 cookie(s) não resgatado(s) e perdeu tudo. "
            "O próximo está disponível em 6 horas. PoroSad",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bunch_unredeemed_one_win_3 = [
        pytest.param(
            "en",
            "[ 🍍 | 🍌 | 🍌 | 🍉 | 🍓 ] You have used 1 unredeemed cookie(s) and earned 3 cookies. ",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "[ 🍍 | 🍌 | 🍌 | 🍉 | 🍓 ] Você usou 1 cookie(s) não resgatado(s) e ganhou 3 cookies.  PogChamp",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bunch_unredeemed_one_win_6 = [
        pytest.param(
            "en",
            "[ 🥑 | 🍋 | 🍋 | 🍋 | 🍉 ] You have used 1 unredeemed cookie(s) and earned 6 cookies. ",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "[ 🥑 | 🍋 | 🍋 | 🍋 | 🍉 ] Você usou 1 cookie(s) não resgatado(s) e ganhou 6 cookies.  PogChamp",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bunch_unredeemed_one_win_12 = [
        pytest.param(
            "en",
            "[ 🍓 | 🍓 | 🍓 | 🍓 | 🍇 ] You have used 1 unredeemed cookie(s) and earned 12 cookies. ",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "[ 🍓 | 🍓 | 🍓 | 🍓 | 🍇 ] Você usou 1 cookie(s) não resgatado(s) e ganhou 12 cookies.  PogChamp",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bunch_unredeemed_one_win_30 = [
        pytest.param(
            "en",
            "[ 🍇 | 🍇 | 🍇 | 🍇 | 🍇 ] You have used 1 unredeemed cookie(s) and earned 30 cookies. ",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "[ 🍇 | 🍇 | 🍇 | 🍇 | 🍇 ] Você usou 1 cookie(s) não resgatado(s) e ganhou 30 cookies.  PogChamp",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bunch_unredeemed_one_win_3_emotes = [
        pytest.param(
            "en",
            "[ ppL | ppL | chuw | catJAM | 🍌 ] You have used 1 unredeemed cookie(s) and earned 3 cookies.  "
            "PogChamp",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "[ ppL | ppL | chuw | catJAM | 🍌 ] Você usou 1 cookie(s) não resgatado(s) e ganhou 3 cookies.  "
            "PogChamp",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bunch_unredeemed_one_win_6_emotes = [
        pytest.param(
            "en",
            "[ papaoRun | papaoRun | papaoRun | 🥔 | COPIUM ] "  # NOQA
            "You have used 1 unredeemed cookie(s) and earned 6 cookies.  PogChamp",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "[ papaoRun | papaoRun | papaoRun | 🥔 | COPIUM ] "  # NOQA
            "Você usou 1 cookie(s) não resgatado(s) e ganhou 6 cookies.  PogChamp",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bunch_unredeemed_one_win_12_emotes = [
        pytest.param(
            "en",
            "[ GIGACHAD | GIGACHAD | GIGACHAD | GIGACHAD | NOOOO ] "  # NOQA
            "You have used 1 unredeemed cookie(s) and earned 12 cookies.  PogChamp",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "[ GIGACHAD | GIGACHAD | GIGACHAD | GIGACHAD | NOOOO ] "  # NOQA
            "Você usou 1 cookie(s) não resgatado(s) e ganhou 12 cookies.  PogChamp",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    bunch_unredeemed_one_win_30_emotes = [
        pytest.param(
            "en",
            "[ papaoRun | papaoRun | papaoRun | papaoRun | papaoRun ] "  # NOQA
            "You have used 1 unredeemed cookie(s) and earned 30 cookies.  PogChamp",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "[ papaoRun | papaoRun | papaoRun | papaoRun | papaoRun ] "  # NOQA
            "Você usou 1 cookie(s) não resgatado(s) e ganhou 30 cookies.  PogChamp",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]
