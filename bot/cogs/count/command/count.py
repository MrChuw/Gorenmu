# -*- coding: utf-8 -*-
import re
import string

from urlextract import URLExtract

from bot.ext.commands import base_decorator, Bucket, check, command, Context, cooldown
from bot.translations import EnUsDecorators, Response


@base_decorator(EnUsDecorators.Count)
@cooldown(rate=3, per=10, bucket=Bucket.user)
@check([])
@command(name='count', aliases=[''])
async def command(ctx: Context, *, content: str) -> Response:
    if (urls := URLExtract().find_urls(text=content)) and 'type:url' in content:
        content = ""
        cache_session = ctx.bot.SessionsCaches.AdminCachedSession
        for url in urls:
            teste = await cache_session.session.get(url)
            content += f"{await teste.text()} "
    uppercase_count = len(re.findall(r'[A-Z]', content))
    punctuations_count = len(re.findall(f'[{re.escape(string.punctuation)}]', content))
    special_chars_count = len([char for char in re.findall(r'[^\w\s]', content) if char not in string.punctuation])
    return ctx.translations.Count.character_count.format_response(ctx, len(content), punctuations_count,
                                                                  uppercase_count, special_chars_count
                                                                  )
