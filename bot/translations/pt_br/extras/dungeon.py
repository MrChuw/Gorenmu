# -*- coding: utf-8 -*-


# TODO: Adicionar os em inglês como "padrao" e adicionar no extras do inglês tbm.


dungeon_rank_dict: dict[str, dict[str, str | None]] = {
    "vitoria": {"order_by": "wins", "title": "vitórias", "class_": None},
    "vitorias": {"order_by": "wins", "title": "vitórias", "class_": None},
    "vitória": {"order_by": "wins", "title": "vitórias", "class_": None},
    "vitórias": {"order_by": "wins", "title": "vitórias", "class_": None},
    "win": {"order_by": "wins", "title": "vitórias", "class_": None},
    "wins": {"order_by": "wins", "title": "vitórias", "class_": None},
    "derrota": {"order_by": "defeats", "title": "derrotas", "class_": None},
    "derrotas": {"order_by": "defeats", "title": "derrotas", "class_": None},
    "lose": {"order_by": "defeats", "title": "derrotas", "class_": None},
    "losses": {"order_by": "defeats", "title": "derrotas", "class_": None},
    "winrate": {"order_by": "wins", "title": "winrate", "class_": None},
    "guerreiro": {"order_by": "level", "title": "guerreiros", "class_": "w"},
    "guerreiros": {"order_by": "level", "title": "guerreiros", "class_": "w"},
    "guerreira": {"order_by": "level", "title": "guerreiros", "class_": "w"},
    "guerreiras": {"order_by": "level", "title": "guerreiros", "class_": "w"},
    "mago": {"order_by": "level", "title": "magos", "class_": "m"},
    "magos": {"order_by": "level", "title": "magos", "class_": "m"},
    "maga": {"order_by": "level", "title": "magos", "class_": "m"},
    "magas": {"order_by": "level", "title": "magos", "class_": "m"},
    "arqueiro": {"order_by": "level", "title": "arqueiros", "class_": "a"},
    "arqueiros": {"order_by": "level", "title": "arqueiros", "class_": "a"},
    "arqueira": {"order_by": "level", "title": "arqueiros", "class_": "a"},
    "arqueiras": {"order_by": "level", "title": "arqueiros", "class_": "a"},
    "default": {"order_by": "level", "title": "dungeons", "class_": None},
}
