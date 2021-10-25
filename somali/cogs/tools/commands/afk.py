# -*- coding: utf-8 -*-
from somali.cogs.tools import afks
from somali.database.models import Afk
from somali.utils import checks

description = "Informe que você está se ausentando do chat"
aliases = list(afks.keys())[1:]
extra_checks = [checks.allowed, checks.banword]


async def command(ctx, *, content: str = ""):
    if content and len(content) > 400:
        ctx.response = "essa mensagem é muito comprida"
    else:
        invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
        afk_type = afks[invoke_by]
        await Afk.create(
            user_id=ctx.author.id,
            alias=invoke_by,
            content=content,
        )
        ctx.response = f"você {afk_type.afk}: {content or afk_type.emoji}"
