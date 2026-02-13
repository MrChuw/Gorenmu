from __future__ import annotations

import asyncio
import random
import string
from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.models import Imgur, ImgurAggregate
from bot.utils import SessionsCaches, TimeTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class ImgurCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, parent=self)
        self.TimeTools: TimeTools = TimeTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.UploadThings: UploadThings = UploadThings(bot)
        self.hexa_digits = string.digits + string.ascii_letters
        bot.disable_default.append("imgur")

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="imgur", aliases=["imgur7"])
    async def imgur(self, ctx: Context, *, args: str = "") -> Response:
        translation = self.translations.Imgur
        imgur_type = 5 if ctx.invoke_by == "imgur" else 7

        requested_amount = int(args) if args.isdigit() else 1
        max_amount = 100 if imgur_type == 5 else 10
        requested_amount = min(requested_amount, max_amount)

        timeout = self.TimeTools.Timeout.timeout(250 + ((requested_amount // 500) * 120))
        time_start = asyncio.get_event_loop().time()
        try:
            async with timeout:
                all_links = await self.fetch_imgur_links(requested_amount, imgur_type)
        except TimeoutError:
            return translation.took_too_long(round(timeout.duration(), 2))
        except Exception as e:
            await self.bot.CommandHandler.send_bug(ctx, e)
            self.bot.log.error(e)
            all_links = []

        if not all_links:
            return translation.took_too_long(1)

        links_requested = all_links[:requested_amount]

        await Imgur.bulk_create(
            [
                Imgur(user=ctx.user, link=link.replace("https://i.imgur.com/", "").replace(".jpg", ""))
                for link in all_links
            ]
        )

        embed_url = None
        try:
            if len(all_links) > 1:
                embed_url = await self.UploadThings.send_imgur(all_links, self.SessionsCaches.Imgur.session)
                await ImgurAggregate.create(link=embed_url, user=ctx.user)
        except Exception as e:
            await self.bot.CommandHandler.send_bug(ctx, e)
            self.bot.log.error(e)
            embed_url = None

        time_end = self.translations.SupportTools.TimeTools.Humanize().precisedelta(
            asyncio.get_event_loop().time() - time_start, minimum_unit="microseconds"
        )

        display_links = [link.replace("https://i.imgur.com/", "https://ri.mrchuw.com.br/") for link in links_requested]
        responses = [translation.time(time_end)]

        if embed_url:
            responses.append(" ".join(display_links[:9]))
            responses.append(translation.all_images(embed_url))
        else:
            responses.append(" ".join(display_links[:10]))

        return translation.links(responses=responses)

    async def generate(self, amount: int, k: int):
        urls = [
            "https://i.imgur.com/" + "".join(random.choices(self.hexa_digits, k=k)) + ".jpg" for _ in range(amount + 10)
        ]
        tasks = [
            asyncio.create_task(self.SessionsCaches.Imgur.session.head(url=url, allow_redirects=False)) for url in urls
        ]
        return await asyncio.gather(*tasks)

    async def fetch_imgur_links(self, amount: int, k: int = 5) -> list[str]:
        links = []
        reserve_amount = amount

        while len(links) < amount:
            urls = await self.generate(amount=reserve_amount, k=k)
            for url in urls:
                if url.status == 200:
                    links.append(f"{url.url}")
                elif url.status in [429, 503]:
                    return links

            if len(links) < amount:
                reserve_amount = int(reserve_amount * 0.2) if amount >= 1001 else int(reserve_amount * 0.5)
                reserve_amount = max(reserve_amount, 1)

        return links


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(ImgurCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
