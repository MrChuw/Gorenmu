# -*- coding: utf-8 -*-
import datetime

from bot.bot import Gorenmu
from bot.ext.commands import base_decorator, Bucket, check, command, Command, Context, cooldown
from bot.translations import BaseDecorators, Response
from bot.utils import Role


@base_decorator(BaseDecorators.Admin.Nada)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([Role.dev])
@command(name='nada', aliases=[])
async def command(ctx: Context, *, args, ) -> Response:
    translations = ctx.translations.Admin.Nada
    teste = datetime.datetime.now(datetime.timezone.utc)

    return translations.nada.format_response(ctx, args, success=True, handle=None, response_list=[])
