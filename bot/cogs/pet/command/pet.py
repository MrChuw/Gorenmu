from __future__ import annotations

from typing import TYPE_CHECKING

from bot.apis import Emotes
from bot.ext import ChatMessage, Context, Response, commands
from bot.models import Cookies, Pets, User
from bot.utils import RandomUtils, SessionsCaches, StringTools

from .translations import PetType, Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class PetCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, parent=self)
        self.StringTools: StringTools = StringTools()
        self.RandomUtils: RandomUtils = RandomUtils()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.Emotes: Emotes = Emotes(bot, self.SessionsCaches.Emotes.session)
        self.prohibited_name = ["buy", "list", "name", "sell"]

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    async def component_before_invoke(self, ctx: Context) -> None:
        self.translations.ctx_set(ctx)

    @commands.command(name="teste", aliases=[])
    async def teste(self, ctx: Context, *, name: str = "") -> Response:
        teste = self.translations.PetList.get_pet("troll")

        return self.translations.Exceptions.echo(f"{teste.specie} | {teste.price} | {teste.emoji}")

    @commands.group(name="pet", aliases=[])
    async def pet(self, ctx: Context, *, name: str = "") -> Response:
        if not (user := await User.get_user(ctx, self.translations, name)):
            return self.translations.Exceptions.user_not_found_name(name)
        await user.fetch_related("pets")
        pets = await ctx.user.pets.all()
        if not pets:
            return self.translations.PetList.no_pets()
        pet_db = next((p for p in pets if (p.name or p.specie).lower() == name.lower()), None)
        if not pet_db:
            mention = self.translations.SupportTools.LanguageContext.mention(ctx.author.name, ctx.author.name)
            return self.translations.PetList.pet(mention, self.translations.PetList.get_formatted_pets(pets))
        emote = await self.RandomUtils.pick_dynamic(self.Emotes.get_pat(ctx, 1), "😚", self.bot)
        return self.translations.Pet.pet_pat(name, self.translations.PetList.get_pet(pet_db.specie).emoji, emote)

    @pet.command("buy")
    async def pet_buy(self, ctx: Context, *, specie: str = "") -> Response:
        translations = self.translations.PetBuy
        # TODO: testar isso
        specie_inner, name = self.StringTools.extract_and_remove_field(specie, "user")
        if (name and not specie) or not specie:
            pets = ", ".join([f"{pet.emoji} {pet.specie} ({pet.price})" for pet in self._pet_list(ctx, user_name=name)])
            return translations.pet_list(pets)

        specie_inner, pet_name = self.StringTools.extract_and_remove_field(specie, "pet_name")
        if pet_name and pet_name in self.prohibited_name:
            pet_name = f"_{pet_name}"
        specie = specie_inner.lower()
        if not (cookies := await Cookies.get_cookie(ctx, self.translations, user=ctx.user, none=True)):
            return translations.no_cookies()

        for pet in self._pet_list(ctx):
            if pet.specie == specie:
                price = pet.price
                if cookies.stocked < price:
                    return translations.not_enough_cookies(specie, price - cookies.stocked)
                await cookies.reduce_update(price)
                pet_db = await Pets.create_pet(specie=pet.specie, user=ctx.user, name=pet_name)
                return translations.pet_buy(pet.specie, pet.emoji, pet_db.id)
        return translations.not_found(specie)

    @pet.command("list")
    async def pet_list(self, ctx: Context, *, name: str = "") -> Response:
        translation = self.translations.PetList
        name: str = self.StringTools.str2name(name, ctx.author.name)
        if name.lower() == ctx.bot.bot_user.name.lower():
            return translation.bot_name()
        if name == ctx.author.name:
            user = ctx.user
        else:
            user = await User.get_or_none(name=name)
            if not user:
                return self.translations.Exceptions.user_not_found_name(name)
        user_pets = await user.pets.all()
        if user and not user.mention and name.lower() != ctx.author.name.lower():
            return translation.mention_denied(name)
        mention = self.translations.SupportTools.LanguageContext.mention(ctx.author.name, name)
        if len(user_pets) > 0:
            return translation.pet(mention, self.translations.PetList.get_formatted_pets(user_pets, show_id=True))
        if name == ctx.author.name:
            return translation.no_pets()
        return translation.user_no_pets(mention)

    @pet.command("name")
    async def pet_name(self, ctx: Context, *, pet_id: str, pet_name: str) -> Response:
        translations = self.translations.PetName
        if not self.StringTools.string_validator(pet_name):
            return translations.invalid_name(pet_name, 32)
        if not pet_id.isnumeric():
            return translations.invalid_id(pet_id)
        await ctx.user.fetch_related("pets")
        pets = await ctx.user.pets.all()
        if not pets:
            return self.translations.PetList.no_pets()
        for pet in pets:
            if pet.id == int(pet_id):
                await pet.update_name(pet_name)
                return translations.pet_renamed(pet_id, pet_name)
        return translations.invalid_id(pet_id)

    @pet.command("sell")
    async def pet_sell(self, ctx: Context, *, name: str, pet_id: str, price: str) -> Response:
        translations = self.translations.PetSell
        name: str = self.StringTools.str2name(name)
        if await self.bot.cache.get(name, namespace="pet_sell"):
            return self.translations.GenericWait.already_in_action("pet_sell", name, ctx.author.name), None
        if not price.isnumeric():
            return translations.price_not_int(price)
        price = int(price)
        if name.lower() == ctx.bot.bot_user.name.lower():
            return translations.bot_name()
        if name == ctx.author.name:
            return translations.yourself()
        if not (target := await User.get_or_none(name=name)):
            return self.translations.Exceptions.user_not_found_name(name)
        if not (user_pets := await ctx.user.pets.all()):
            return translations.no_pets()
        pet_db = next((p for p in user_pets if p.id == int(pet_id)), None)
        if not pet_db:
            return translations.pet_not_find(pet_db.id)
        if price < (min_price := self.translations.PetList.get_pet(pet_db.specie).price // 3):
            return translations.price_third(price, min_price)
        await target.fetch_related("cookies")
        if (target_cookies := (await target.cookies)[0]).stocked < price:
            return translations.not_enough_cookies(target.name, price)
        try:
            await self.bot.cache.set(name, ctx.author.name, namespace="pet_sell", ttl=11)
            await ctx.simple_response(ctx, translations.start(name, pet_db.name))
            msg = await self.bot.CommandHandler.wait_for_message(
                predicate=self.generic_wait, timeout=30, ctx=ctx, target_name=name
            )
            text = msg.text.lower()
            if text in self.translations.GenericWait.accept():
                await pet_db.change_owner(target)
                await target_cookies.reduce_update(price)
                await ctx.user.fetch_related("cookies")
                await (await ctx.user.cookies)[0].receive_update(price)
                return translations.sold(name, ctx.author.name)
            if text in self.translations.GenericWait.reject():
                return translations.refused(ctx.author.name, name)
            return translations.timeout(name)
        except TimeoutError:
            return translations.timeout(name)
        except Exception as e:
            ctx.bot.log.error(e)
            await ctx.bot.CommandHandler.send_bug(ctx, e)
            return self.translations.Exceptions.error()
        finally:
            await ctx.bot.cache.delete(name, namespace="pet_sell")

    async def generic_wait(self, payload: ChatMessage, ctx: Context, target_name: str) -> bool:
        # return True
        if payload.chatter.id == str(self.bot.bot_id) or payload.source_broadcaster is not None:
            return False
        if payload.chatter.name.lower() != target_name:
            return False
        if payload.broadcaster.name.lower() != ctx.broadcaster.name.lower():
            return False
        return payload.text.lower() in self.translations.GenericWait.accept() + self.translations.GenericWait.reject()

    def _pet_list(self, ctx: Context, *, user_name: str | None = None, limit: int = 6) -> list[PetType]:
        all_pets = self.translations.PetList.get_pets().list_all()

        with self.RandomUtils.temp_seed(user_name or ctx.user.name.lower(), daily=True):
            weights = [max(1, 10000 // pet.price) for pet in all_pets]

            selected_pets = []
            available_pets = list(all_pets)
            available_weights = list(weights)

            for _ in range(min(limit, len(all_pets))):
                picked = self.RandomUtils.random_choices(available_pets, w=available_weights, k=1)[0]
                selected_pets.append(picked)
                idx = available_pets.index(picked)
                available_pets.pop(idx)
                available_weights.pop(idx)

        return sorted(selected_pets, key=lambda k: k.price)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(PetCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
