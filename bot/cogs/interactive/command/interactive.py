from __future__ import annotations

import datetime
import hashlib
from typing import TYPE_CHECKING

from bot.apis import Emotes
from bot.ext import ChatMessage, Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class InteractiveCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, command=self)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.Emotes: Emotes = Emotes(bot, self.SessionsCaches.Emotes.session)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    # @commands.command(name="interactive", aliases=[])
    # async def interactive(self, ctx: Context, arg: str) -> Response:
    #     name = self.StringTools.str2name_or(arg)
    #
    #     quick_responses = {
    #         ctx.bot.bot_user.name.lower(): self.translations.Interactive.bot_nick("None"),
    #         ctx.author.name.lower(): self.translations.Interactive.yourself("None"),
    #     }
    #     if name in quick_responses:
    #         return quick_responses.get(name)
    #
    #     return self.translations.Exceptions.echo(ctx, arg)

    @commands.command(name="fight", aliases=[])
    async def fight(self, ctx: Context, arg: str) -> Response:
        translations = self.translations.Fight
        name = await self.generic_prepare(ctx, arg, "fight", translations)
        if type(name) is tuple:
            return Response(ctx, success=False, response_string=name)
        try:
            await self.bot.cache.set(name, ctx.author.name, namespace="fight", ttl=11)
            await ctx.simple_response(ctx, translations.start(name))
            message = await self.bot.CommandHandler.wait_for_message(
                predicate=self.generic_wait, timeout=10, ctx=ctx, target_name=name
            )
            if message.text.lower() in self.translations.GenericWait.accept():
                response = translations.options(name, ctx.author.name)
            elif message.text.lower() in self.translations.GenericWait.reject():
                response = translations.refused(ctx.author.name, name)
            else:
                response = translations.timeout(name)
        except TimeoutError:
            response = translations.timeout(name)
        except Exception as e:
            ctx.bot.log.error(e)
            await ctx.bot.CommandHandler.send_bug(ctx, e)
            response = self.translations.Exceptions.error()
        finally:
            await ctx.bot.cache.delete(name, namespace="fight")
        return response or self.translations.Exceptions.error()

    @commands.command(name="hug", aliases=[])
    async def hug(self, ctx: Context, arg: str) -> Response:
        translations = self.translations.Hug
        name = await self.generic_prepare(ctx, arg, "hug", translations)
        if isinstance(name, Response):
            return name
        emote = None
        if not self.bot.mock:
            emote = (await self.Emotes.get_hug(ctx, 1))[0]
        if not emote:
            emote = "🤗"
        return translations.options(user=name, emote=emote)

    @commands.command(name="kiss", aliases=[])
    async def kiss(self, ctx: Context, arg: str) -> Response:
        translations = self.translations.Kiss
        name = await self.generic_prepare(ctx, arg, "kiss", translations)
        emote = (None if self.bot.mock else (await self.Emotes.get_kiss(ctx, 1))[0]) or "🤗"
        return name if isinstance(name, Response) else translations.options(user=name, emote=emote)

    @commands.command(name="ship", aliases=["love"])
    async def ship(self, ctx: Context, *, arg: str) -> Response:
        translations = self.translations.Ship
        name1, name2 = await self.generic_prepare_2_names(ctx, arg, translations)
        if isinstance(name1, Response):
            return name1
        if name1 == name2:
            return translations.yourself()

        seed_string = f"{name1.lower()}{name1.lower()}{datetime.datetime.now().strftime('%Y-%U')}"
        hash_digest = hashlib.sha256(seed_string.encode()).hexdigest()
        percentage = int(hash_digest, 16) % 101
        ship = name1[: len(name1) // 2 + 1] + name2[len(name2) // 2 + 1 :]
        emojis = ["😭", "😥", "💔", "😢", "😐", "😊", "❤", "💕", "💘", "😍", "PogChamp ❤"]
        emoji = emojis[round(percentage / 10)]
        return await translations.options(
            user1=name1,
            user2=name2,
            ship=ship,
            percentage=percentage,
            emoji=emoji,
        )

    @commands.command(name="pat", aliases=[])
    async def pat(self, ctx: Context, *, arg: str) -> Response:
        translations = self.translations.Pat
        name = await self.generic_prepare(ctx, arg, "pat", translations)
        if isinstance(name, Response):
            return name
        if name == ctx.author.name:
            return translations.yourself()
        emote = (None if self.bot.mock else (await self.Emotes.get_pat(ctx, 1))[0]) or "😚"
        return await translations.options(name, emote)

    @commands.command(name="penis", aliases=[])
    async def penis(self, ctx: Context, *, arg: str | None = None) -> Response:
        translations = self.translations.Penis
        if not arg:
            arg = ctx.author.name
        name = await self.generic_prepare(ctx, arg, "penis", translations)
        if isinstance(name, Response):
            return name
        seed = f"{name.lower()}{datetime.datetime.now().strftime('%j')}"
        hash_val = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
        length = (hash_val % 28) + 5
        emoji = "🤏" if length <= 13 else "🍌" if length <= 19 else "🍆"
        return await translations.options(name, length, emoji)

    @commands.command(name="slap", aliases=[])
    async def slap(self, ctx: Context, *, arg: str) -> Response:
        translations = self.translations.Slap
        name = await self.generic_prepare(ctx, arg, "slap", translations)
        if isinstance(name, Response):
            return name
        if name == ctx.author.name:
            return translations.yourself()
        now = datetime.datetime.now()
        seed_string = f"{name.lower()}{now.strftime('%Y-%m-%d-%H-%M')}-{now.second // 30}"
        hash_digest = hashlib.sha256(seed_string.encode()).hexdigest()
        percentage = int(hash_digest, 16) % 101
        emoji = "👋"
        if not self.bot.mock:
            emojis = await self.Emotes.get_hit(ctx, amount=10)
            if len(emojis) > 2:
                emoji = emojis[round(percentage / 10)]
        return await translations.options(name, percentage, emoji)

    @commands.command(name="tuck", aliases=[])
    async def tuck(self, ctx: Context, *, arg: str) -> Response:
        translations = self.translations.Tuck
        name = await self.generic_prepare(ctx, arg, "tuck", translations)
        if isinstance(name, Response):
            return name
        now = datetime.datetime.now()
        seed_string = f"{name.lower()}{now.strftime('%Y-%m-%d-%H-%M-%S')}-{now.second // 30}"
        hash_digest = hashlib.sha256(seed_string.encode()).hexdigest()
        emoji1 = "🙂"
        emoji2 = "🛏"
        if not self.bot.mock:
            base_value = int(hash_digest, 16) % 101
            emojis1 = await self.Emotes.get_okay(ctx, amount=10)
            if emojis1:
                index1 = (base_value * len(emojis1)) // 101
                emoji1 = emojis1[min(index1, len(emojis1) - 1)]

            emojis2 = await self.Emotes.get_bed(ctx, amount=10)
            if emojis2:
                index2 = (base_value * len(emojis2)) // 101
                emoji2 = emojis2[min(index2, len(emojis2) - 1)]
        if name == ctx.author.name:
            return translations.yourself(emoji2)
        return await translations.options(name, emoji1, emoji2)

    async def generic_wait(self, payload: ChatMessage, ctx: Context, target_name: str) -> bool:
        # return True
        if payload.chatter.id == str(self.bot.bot_id) or payload.source_broadcaster is not None:
            return False
        if payload.chatter.name.lower() != target_name:
            return False
        if payload.broadcaster.name.lower() != ctx.broadcaster.name.lower():
            return False
        return payload.text.lower() in self.translations.GenericWait.accept() + self.translations.GenericWait.reject()

    async def generic_prepare(self, ctx: Context, arg: str, action: str, translation):
        name = self.StringTools.str2name_or(arg)
        quick_responses = {
            ctx.bot.bot_user.name.lower(): translation.bot_nick(),
            ctx.author.name.lower(): translation.yourself(action),
        }
        if name in quick_responses:
            return quick_responses.get(name)
        if await self.bot.cache.get(name, namespace=action):
            return self.translations.GenericWait.already_in_action(action, name, ctx.author.name), None
        return name

    async def generic_prepare_2_names(self, ctx: Context, arg: str, translation):
        name1, name2, _ = self.StringTools.safe_split(arg, 3)
        name1 = self.StringTools.str2name_or(name1)
        name2 = self.StringTools.str2name_or(name2)
        quick_responses = {
            ctx.bot.bot_user.name.lower(): translation.bot_nick(),
        }
        if name1 in quick_responses:
            return quick_responses.get(name1), None
        elif name2 in quick_responses:
            return quick_responses.get(name2), None
        if not name2:
            name1, name2 = ctx.author.name, name1

        return name1, name2


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(InteractiveCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
