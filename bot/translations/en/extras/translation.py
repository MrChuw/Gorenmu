from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.ext.commands import Context
    from bot.models import User

mention_dict = {"en": "you",
                "pt_br": "você"}


class BaseTranslation:
    ctx: Context


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
























