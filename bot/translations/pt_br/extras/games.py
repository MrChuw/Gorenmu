# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.ext.commands import Context


def fight_option(ctx: Context, name: str) -> list[str]:
    return [
        f"@{name} acaba com @{ctx.author.name}!",
        f"@{name} deixa @{ctx.author.name} desacordado!",
        f"@{name} derrota @{ctx.author.name} facilmente!",
        f"@{name} espanca @{ctx.author.name} sem piedade!",
        f"@{name} não dá chances para @{ctx.author.name} e vence!",
        f"@{name} quase perde, mas derruba @{ctx.author.name}!",
        f"@{name} vence a luta contra @{ctx.author.name}!",
        f"@{name} vence @{ctx.author.name} com dificuldades!",
        f"@{name} vence @{ctx.author.name} em uma luta acirrada!",
        f"@{name} vence @{ctx.author.name} facilmente!",
        f"@{ctx.author.name} acaba com @{name}!",
        f"@{ctx.author.name} deixa @{name} desacordado!",
        f"@{ctx.author.name} derrota @{name} facilmente!",
        f"@{ctx.author.name} espanca @{name} sem piedade!",
        f"@{ctx.author.name} não dá chances para @{name} e vence!",
        f"@{ctx.author.name} quase perde, mas derruba @{name}!",
        f"@{ctx.author.name} vence a luta contra @{name}!",
        f"@{ctx.author.name} vence @{name} com dificuldades!",
        f"@{ctx.author.name} vence @{name} em uma luta acirrada!",
        f"@{ctx.author.name} vence @{name} facilmente!",
    ]
