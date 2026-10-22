from __future__ import annotations

from typing import TYPE_CHECKING

from bot.apis import Emotes
from bot.ext import ChatMessage, Context, Response, commands
from bot.utils import RandomUtils, SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


# TODO: Change to random utils
# TODO: If the user has location set, check the temps and change the penis comand.


class InteractiveCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()
        self.RandomUtils: RandomUtils = RandomUtils()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.Emotes: Emotes = Emotes(bot, self.SessionsCaches.Emotes.session)

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
            return Response(ctx, success=False, response=name[0])
        if isinstance(name, Response):
            return name
        try:
            await self.bot.cache.set(name, ctx.author.name, namespace="fight", ttl=11)
            await ctx.simple_response(ctx, translations.start(name))
            message = await self.bot.CommandHandler.wait_for_message(
                predicate=self.bot.CommandHandler.generic_wait,
                timeout=10,
                ctx=ctx,
                target_name=name,
                generic_wait=self.translations.GenericWait,
            )
            if message.text.lower() in self.translations.GenericWait.accept():
                response = translations.options(name, ctx.author.name or "")
            elif message.text.lower() in self.translations.GenericWait.reject():
                response = translations.refused(ctx.author.name or "", name)
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
        emote = await self.RandomUtils.pick_dynamic(self.Emotes.get_hug(ctx, 1), "🤗", self.bot)
        return translations.options(user=name, emote=emote)

    @commands.command(name="kiss", aliases=[])
    async def kiss(self, ctx: Context, arg: str) -> Response:
        translations = self.translations.Kiss
        name = await self.generic_prepare(ctx, arg, "kiss", translations)
        emote = await self.RandomUtils.pick_dynamic(self.Emotes.get_kiss(ctx, 1), "😘", self.bot)
        return name if isinstance(name, Response) else translations.options(user=name, emote=emote)

    @commands.command(name="ship", aliases=["love"])
    async def ship(self, ctx: Context, *, arg: str) -> Response:
        translations = self.translations.Ship
        name1, name2 = await self.generic_prepare_2_names(ctx, arg, translations)
        if isinstance(name1, Response):
            return name1
        if name1 == name2:
            return translations.yourself()
        if not name1:
            return translations.forgot_option1()
        if not name2:
            return translations.forgot_option2()

        percentage = self.RandomUtils.get_seeded_percentage(
            name1.lower(), name2.lower(), time_basis=self.RandomUtils.TimeBasis.WEEKLY
        )
        emojis = ["😭", "😥", "💔", "😢", "😐", "😊", "❤", "💕", "💘", "😍", "PogChamp ❤"]
        emoji = self.RandomUtils.pick_by_percentage(emojis, percentage)
        ship_name = name1[: len(name1) // 2 + 1] + name2[len(name2) // 2 + 1 :]
        return await translations.options(user1=name1, user2=name2, ship=ship_name, percentage=percentage, emoji=emoji)

    @commands.command(name="pat", aliases=[])
    async def pat(self, ctx: Context, *, arg: str) -> Response:
        translations = self.translations.Pat
        name = await self.generic_prepare(ctx, arg, "pat", translations)
        if isinstance(name, Response):
            return name
        if name == ctx.author.name:
            return translations.yourself()
        emote = await self.RandomUtils.pick_dynamic(self.Emotes.get_pat(ctx, 1), "😚", self.bot)
        return await translations.options(name, emote)

    @commands.command(name="penis", aliases=[])
    async def penis(self, ctx: Context, *, arg: str | None = None) -> Response:
        translations = self.translations.Penis
        if not arg:
            arg = ctx.author.name or ""
        name = await self.generic_prepare(ctx, arg, "penis", translations)
        if isinstance(name, Response):
            return name
        percentage = self.RandomUtils.get_seeded_percentage(name.lower(), time_basis=self.RandomUtils.TimeBasis.DAILY)
        length = self.RandomUtils.map_percentage_to_range(percentage, min_value=5, max_value=32)
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
        percentage = self.RandomUtils.get_seeded_percentage(
            name.lower(), time_basis=self.RandomUtils.TimeBasis.SECOND_30
        )
        emote = await self.RandomUtils.pick_dynamic_by_percentage(
            self.Emotes.get_hit(ctx, 1), "👋", percentage, self.bot
        )
        return await translations.options(name, percentage, emote)

    @commands.command(name="tuck", aliases=[])
    async def tuck(self, ctx: Context, *, arg: str) -> Response:
        translations = self.translations.Tuck
        name = await self.generic_prepare(ctx, arg, "tuck", translations)
        if isinstance(name, Response):
            return name
        percentage = self.RandomUtils.get_seeded_percentage(
            name.lower(), time_basis=self.RandomUtils.TimeBasis.SECOND_30
        )
        emoji1 = await self.RandomUtils.pick_dynamic_by_percentage(
            self.Emotes.get_okay(ctx, 1), "🙂", percentage, self.bot
        )
        percentage = self.RandomUtils.get_seeded_percentage(
            name.lower(), time_basis=self.RandomUtils.TimeBasis.SECOND_30
        )
        emoji2 = await self.RandomUtils.pick_dynamic_by_percentage(
            self.Emotes.get_bed(ctx, 1), "🛏", percentage, self.bot
        )
        if name == ctx.author.name:
            return translations.yourself(emoji2)
        return await translations.options(name, emoji1, emoji2)

    async def generic_wait(self, payload: ChatMessage, ctx: Context, target_name: str) -> bool:
        # return True
        if payload.chatter.id == self.bot.bot_id or payload.source_broadcaster is not None:
            return False
        if (payload.chatter.name or "").lower() != target_name:
            return False
        if (payload.broadcaster.name or "").lower() != (ctx.broadcaster.name or "").lower():
            return False
        return payload.text.lower() in self.translations.GenericWait.accept() + self.translations.GenericWait.reject()

    async def generic_prepare(self, ctx: Context, arg: str, action: str, translation) -> str | Response:
        name = self.StringTools.str2name_or(arg)
        quick_responses: dict[str, Response] = {
            (ctx.bot.bot_user.name or "").lower(): translation.bot_nick(),
            (ctx.author.name or "").lower(): translation.yourself(action),
        }
        if name in quick_responses:
            return quick_responses[name]
        if await self.bot.cache.get(name, namespace=action):
            return self.translations.GenericWait.already_in_action(action, name, ctx.author.name or "")
        return name

    async def generic_prepare_2_names(
        self, ctx: Context, arg: str, translation
    ) -> tuple[str | None, None] | tuple[str | None, str | None]:
        name1, name2, _ = self.StringTools.safe_split(arg, 3)
        name1 = self.StringTools.str2name_or(name1 or "")
        name2 = self.StringTools.str2name_or(name2 or "")
        quick_responses = {(ctx.bot.bot_user.name or "").lower(): translation.bot_nick()}
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
