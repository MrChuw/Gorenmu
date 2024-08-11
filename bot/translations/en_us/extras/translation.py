from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.ext.commands import Context
    from bot.models import User

mention_dict = {"en-us": "you",
                "pt-br": "você"}

class BaseTranslation:
    ctx: Context

    # TODO: adicionar um fallback para o idioma padrão caso não tenha a tradução.

    @staticmethod
    def mention(ctx: Context, user: User, name: str) -> str:
        return (
            mention_dict[user.language] if user.name == ctx.author.name else f"@{name}"
        )
        # if user.language is not None:
        #     pass  # if user.language == "pt-br":
        #     return "você" if user.name == ctx.author.name else f"@{name}"
        # if user.language == "en-us":
        #     return "you" if user.name == ctx.author.name else f"@{name}"

    @staticmethod
    def remind_mention(ctx: Context, user: User, name: str, invoke_by: str) -> str:
        return (
            mention_dict[user.language]
            if name == ctx.author.name
            else (
                user.nickname or f"@{name}"
                if invoke_by in ["remind", "lembrete", "remember"]
                else mention_dict[user.language]
            )
        )
