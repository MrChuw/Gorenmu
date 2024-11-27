# -*- coding: utf-8 -*-
import asyncio
import datetime
from bot.bot import Gorenmu
from bot.models import User, Channel
from bot.utils import Check, Role
from typing import Dict, Any, List, Tuple, Optional, Coroutine, Callable
from bot.ext.commands import Bucket, check, Context, cooldown, base_decorator, helper, usage, command
from bot.translations import EnTranslations, EnDecorators, Response
from bot.bot import Gorenmu
from bot.ext.commands import Command

@base_decorator(EnDecorators.TypeChecking)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', aliases=[''])
async def command(ctx: Context, *, content, ) -> Response:
    translations = ctx.translations.TypeChecking

    return translations.nada.format_response(ctx, content, success=True, handle=None, response_list=[])









