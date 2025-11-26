from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class DicioCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)

    cooldown_rate = 3
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.command(name="dicio", aliases=[])
    async def dicio(self, ctx: Context, *, content) -> Response:
        translations = self.translations.Dicio
        word, lang = self.StringTools.extract_and_remove_field(content, "lang", ctx.user.language or "en")
        word, lang = word.lower(), lang.lower()
        if lang == "languages":
            return translations.all_languages(ctx, translations.languages("languages"))

        json_response = await self.get_word(word, lang)  # NOQA
        if "error" in json_response:
            return translations.error(
                ctx,
                self.bot.config.ApisConfig.dicio_url / "languages",
                self.bot.dev_name,
            )

        if json_response["exist"]:
            exist = translations.exist(ctx)
            url = translations.url(lang, word)
        else:
            exist = translations.not_exist(ctx)
            url = ""

        similar = ", ".join(json_response["suggestions"]) if json_response["suggestions"] else ""

        origin = ", ".join(json_response["stem"]) if json_response["stem"] else word if json_response["exist"] else ""

        return translations.response(ctx, word, exist, similar, origin, url)

    async def get_word(self, word: str, lang: str) -> dict:
        session = self.SessionsCaches.Dicio.session
        lang = self.translations.Dicio.languages(lang)
        response = await session.get(self.bot.config.ApisConfig.dicio_url / lang / word.strip())
        return await response.json()


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(DicioCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA
