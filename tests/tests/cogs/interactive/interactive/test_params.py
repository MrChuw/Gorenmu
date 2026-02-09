from typing import ClassVar

import pytest


class Params:
    class Hug:
        decorators: ClassVar[list] = [
            pytest.param("en", 'hug someone.', 'To use: +hug (username)', marks=pytest.mark.en, id="en"),
            pytest.param(
                "pt_BR",
                'De um abraço em alguém.',
                'Para usar: +hug (username)',
                marks=pytest.mark.pt_BR,
                id="pt_BR",
            ),
        ]

        yourself: ClassVar[list] = [
            pytest.param("en", 'you tried to hug yourself...', marks=pytest.mark.en, id="en"),
            pytest.param("pt_BR", 'você tentou se abraçar...', marks=pytest.mark.pt_BR, id="pt_BR"),
        ]

        bot_nick: ClassVar[list] = [
            pytest.param("en", '🤗', marks=pytest.mark.en, id="en"),
            pytest.param("pt_BR", '🤗', marks=pytest.mark.pt_BR, id="pt_BR"),
        ]

        another_name: ClassVar[list] = [
            pytest.param("en", 'hugged @another_name! So sweet! 🤗', marks=pytest.mark.en, id="en"),
            pytest.param("pt_BR", 'abraçou @another_name! Que fofura! 🤗', marks=pytest.mark.pt_BR, id="pt_BR"),
        ]

    class Kiss:
        decorators: ClassVar[list] = [
            pytest.param("en", 'kiss someone.', 'To use: +kiss (username)', id="en"),
            pytest.param("pt_BR", 'De um beijinho em alguém.', 'Para usar: +kiss (username)', id="pt_BR"),
        ]
        yourself: ClassVar[list] = [
            pytest.param("en", 'you tried to kiss yourself...', id="en"),
            pytest.param("pt_BR", 'você tentou se beijar...', id="pt_BR"),
        ]
        bot_nick: ClassVar[list] = [
            pytest.param("en", '😳', id="en"),
            pytest.param("pt_BR", '😳', id="pt_BR"),
        ]
        another_name: ClassVar[list] = [
            pytest.param("en", 'You gave @another_name a little kiss 🤗', id="en"),
            pytest.param("pt_BR", 'você deu um beijinho em @another_name 🤗', id="pt_BR"),
        ]

    class Ship:
        decorators: ClassVar[list] = [
            pytest.param("en", 'Ship someone with someone else.', 'To use: +Ship (username1) (username2)', id="en"),
            pytest.param(
                "pt_BR", 'De um shippe alguém com outra pessoa.', 'Para usar: +Ship (username1) (username2)', id="pt_BR"
            ),
        ]
        yourself: ClassVar[list] = [
            pytest.param("en", "a person can't be shipped with themselves.", id="en"),
            pytest.param("pt_BR", "uma pessoa não pode ser shippada com ela mesma...", id="pt_BR"),
        ]
        bot_nick: ClassVar[list] = [
            pytest.param("en", "😳", id="en"),
            pytest.param("pt_BR", "😳", id="pt_BR"),
        ]
        another_name: ClassVar[list] = [
            pytest.param("en", '@another_name & @user2: anotherr2 with 29% love 😢', id="en"),
            pytest.param("pt_BR", '@another_name & @user2: anotherr2 com 29% de amor 😢', id="pt_BR"),
        ]

    class Pat:
        decorators: ClassVar[list] = [
            pytest.param("en", 'Pat someone.', 'To use: +Pat (username)', id="en"),
            pytest.param("pt_BR", 'De um cafuné em alguém.', 'Para usar: +Pat (username)', id="pt_BR"),
        ]
        yourself: ClassVar[list] = [
            pytest.param("en", 'You tried to pat yourself...', id="en"),
            pytest.param("pt_BR", 'você tentou fazer cafuné em si mesmo...', id="pt_BR"),
        ]
        bot_nick: ClassVar[list] = [
            pytest.param("en", "😊", id="en"),
            pytest.param("pt_BR", "😊", id="pt_BR"),
        ]
        another_name: ClassVar[list] = [
            pytest.param("en", 'you gave a pat to @another_name 😚', id="en"),
            pytest.param("pt_BR", 'você fez cafuné em @another_name 😚', id="pt_BR"),
        ]

    class Penis:
        decorators: ClassVar[list] = [
            pytest.param("en", 'FeelsWeirdMan', 'To use: +penis (username)', id="en"),
            pytest.param("pt_BR", 'FeelsWeirdMan', 'Para usar: +penis (username)', id="pt_BR"),
        ]
        yourself: ClassVar[list] = [
            pytest.param("en", 'username has 11cm 🤏', id="en"),
            pytest.param("pt_BR", 'username tem 11cm 🤏', id="pt_BR"),
        ]
        bot_nick: ClassVar[list] = [
            pytest.param("en", 'I only have a pen drive', id="en"),
            pytest.param("pt_BR", 'eu só tenho pen drive', id="pt_BR"),
        ]
        another_name: ClassVar[list] = [
            pytest.param("en", 'another_name has 9cm 🤏', id="en"),
            pytest.param("pt_BR", 'another_name tem 9cm 🤏', id="pt_BR"),
        ]

    class Slap:
        decorators: ClassVar[list] = [
            pytest.param("en", 'Slap someone.', 'To use: +slap (username)', id="en"),
            pytest.param("pt_BR", 'De um tapa em alguém.', 'Para usar: +slap (username)', id="pt_BR"),
        ]
        yourself: ClassVar[list] = [
            pytest.param("en", 'you slapped yourself... 😕', id="en"),
            pytest.param("pt_BR", 'você se deu um tapa... 😕', id="pt_BR"),
        ]
        bot_nick: ClassVar[list] = [
            pytest.param("en", 'go hit your mom 😠', id="en"),
            pytest.param("pt_BR", 'vai bater na mãe 😠', id="pt_BR"),
        ]
        another_name: ClassVar[list] = [
            pytest.param("en", 'you slapped @another_name with 65% force 👋', id="en"),
            pytest.param("pt_BR", 'você deu um tapa em @another_name com 65% força 👋', id="pt_BR"),
        ]

    class Tuck:
        decorators: ClassVar[list] = [
            pytest.param("en", 'Send someone to bed.', 'To use: +tuck (username)', id="en"),
            pytest.param("pt_BR", 'Envie alguém para cama.', 'Para usar: +tuck (username)', id="pt_BR"),
        ]
        yourself: ClassVar[list] = [
            pytest.param("en", 'You went to bed. 🛏', id="en"),
            pytest.param("pt_BR", 'você foi para a cama. 🛏', id="pt_BR"),
        ]
        bot_nick: ClassVar[list] = [
            pytest.param("en", "I can't sleep right now...", id="en"),
            pytest.param("pt_BR", "eu não posso dormir agora...", id="pt_BR"),
        ]
        another_name: ClassVar[list] = [
            pytest.param("en", 'You put @another_name in bed 🙂👉🛏', id="en"),
            pytest.param("pt_BR", 'você colocou @another_name na cama 🙂👉🛏', id="pt_BR"),
        ]
