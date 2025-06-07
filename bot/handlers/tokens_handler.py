# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

import twitchio
from twitchio import eventsub

from bot.models import TwitchTokens, User as UserModel

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.utils import Config


class TokensHandler:
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        self.config: Config = bot.config

    async def setup_hook(self) -> None:
        tokens = await TwitchTokens.all()
        for token in tokens:
            await token.fetch_related("user")
            user: UserModel = token.user
            subscription = eventsub.ChatMessageSubscription(
                broadcaster_user_id=str(user.id), user_id=str(self.config.BotConfig.bot_id)
            )
            await self.bot.subscribe_websocket(payload=subscription)
            subscription = eventsub.StreamOnlineSubscription(broadcaster_user_id=str(user.id))
            await self.bot.subscribe_websocket(payload=subscription)

        subscription = eventsub.ChatMessageSubscription(
            broadcaster_user_id=str(self.config.BotConfig.dev_userid), user_id=str(self.config.BotConfig.bot_id)
        )
        await self.bot.subscribe_websocket(payload=subscription)

        subscription = eventsub.StreamOnlineSubscription(broadcaster_user_id=str(self.config.BotConfig.dev_userid))
        await self.bot.subscribe_websocket(payload=subscription)

        subscription = eventsub.WhisperReceivedSubscription(
            broadcaster_user_id=str(self.config.BotConfig.bot_id), user_id=str(self.config.BotConfig.bot_id)
        )
        await self.bot.subscribe_websocket(subscription)

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        resp = await super(type(self.bot), self.bot).add_token(token, refresh)

        user = await UserModel.get(id=resp.user_id)
        token_db = await TwitchTokens.get_or_none(user=user)
        if token and token_db.token != token or token_db.refresh != refresh:
            token_db.token = token
            token_db.refresh = refresh
            await token_db.save()
        if not token_db:
            token_db = await TwitchTokens.create(user=user, token=token, refresh=refresh)  # NOQA

        self.bot.log.info(f"Added token to the database for user: {resp.user_id}")
        return resp

    async def load_tokens(self, path: str | None = None) -> None:  # NOQA
        tokens = await TwitchTokens.all()
        for token in tokens:
            await self.add_token(token=token.token, refresh=token.refresh)
