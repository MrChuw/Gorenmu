# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

import twitchio
from twitchio import eventsub

from bot.models import Channel, TwitchTokens
from bot.models import User as UserModel

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.utils import Config


class TokensHandler:
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        self.config: Config = bot.config

    async def setup_conduit(self) -> None:
        tokens = await TwitchTokens.all()
        subs: list[eventsub.SubscriptionPayload] = []
        for token in tokens:
            await token.fetch_related("user")
            user: UserModel = token.user

            subs += [
                eventsub.ChatMessageSubscription(
                    broadcaster_user_id=str(user.id), user_id=str(self.config.BotConfig.bot_id)
                ),
                eventsub.StreamOnlineSubscription(broadcaster_user_id=str(user.id)),
            ]

        subs += [
            eventsub.ChatMessageSubscription(
                broadcaster_user_id=str(self.config.BotConfig.dev_userid), user_id=str(self.config.BotConfig.bot_id)
            ),
            eventsub.StreamOnlineSubscription(broadcaster_user_id=str(self.config.BotConfig.dev_userid)),
            eventsub.WhisperReceivedSubscription(
                broadcaster_user_id=str(self.config.BotConfig.bot_id), user_id=str(self.config.BotConfig.bot_id)
            ),
        ]

        resp: twitchio.MultiSubscribePayload = await self.bot.multi_subscribe(subs)
        if resp.errors:
            for err in resp.errors:
                if err.error.extra["status"] == 409:
                    continue
                else:
                    self.bot.log.warning(
                        f"Failed to subscribe {err.subscription.user_id}, " f"type: {err.subscription.type}"
                    )

    async def event_oauth_authorized(self, payload: twitchio.authentication.UserTokenPayload) -> None:
        await self.add_token(payload.access_token, payload.refresh_token)
        if not payload.user_id:
            return

        if payload.user_id == str(self.config.BotConfig.bot_id):
            return

        subs: list[eventsub.SubscriptionPayload] = [
            eventsub.ChatMessageSubscription(
                broadcaster_user_id=payload.user_id, user_id=str(self.config.BotConfig.bot_id)
            ),
            eventsub.StreamOnlineSubscription(broadcaster_user_id=payload.user_id),
        ]

        resp: twitchio.MultiSubscribePayload = await self.bot.multi_subscribe(subs)
        if resp.errors:
            self.bot.log.warning("Failed to subscribe to: %r, for user: %s", resp.errors, payload.user_id)

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        resp = await super(type(self.bot), self.bot).add_token(token, refresh)

        user = await UserModel.get_user_or_none(
            ctx_bot=self.bot, user_id=resp.user_id if resp.user_id.isnumeric() else int(resp.user_id), translations=None
        )
        if not user:
            user = await UserModel.create(name=resp.login, id=resp.user_id)
            await Channel.get_or_create(user=user)
            await self.bot.ChannelHandler.load_channels()

        token_db = await TwitchTokens.get_or_none(user=user)
        if (token and token_db) and (token_db.token != token or token_db.refresh != refresh):
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
