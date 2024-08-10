# -*- coding: utf-8 -*-
import asyncio
import datetime
from bot.bot import Gorenmu
from bot.models import User, Channel
from bot.utils import Check, Role
from typing import Dict, Any, List, Tuple, Optional, Coroutine, Callable
from bot.ext.commands import Bucket, check, Context, cooldown, base_decorator, helper, usage, command
from bot.translations import EnUsTranslations, EnUsDecorators, Response



@base_decorator(EnUsDecorators.Admin.Nada)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([Check.banword])
@command(name='nada', aliases=[])
async def command(ctx: Context, *, args, ) -> Response:
    translations = ctx.translations.Admin.Nada()
    teste = datetime.datetime.now(datetime.timezone.utc)

    return translations.nada.format_response(ctx, args, success=True, handle=None, response_list=[])
