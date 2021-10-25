# -*- coding: utf-8 -*-
from somali.database.models import Bug

description = "Reporte um bug que está ocorrendo no Bot"
usage = "digite o comando e o bug que você encontrou"
aliases = ["bg"]


async def command(ctx, *, content: str):
    bug = await Bug.create(
        name=ctx.author.name,
        channel=ctx.channel.name,
        content=content,
    )
    ctx.response = f"seu bug foi reportado 🐛 (ID {bug.id})"
