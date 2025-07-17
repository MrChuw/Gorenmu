# -*- coding: utf-8 -*-
from contextlib import AsyncExitStack
from unittest.mock import AsyncMock, MagicMock, patch


class MockBuilder:
    def __init__(self, mock_context):
        self.patches = []
        self.mock_context = mock_context
        self._stack = AsyncExitStack()  # NOQA

    def color_name(self, return_value: str = "Vermilion"):
        self.patches.append(patch("bot.apis.color.Color.name", return_value=return_value))
        return self

    def bot_fetch_user(self, name="mock_user", user_id=1234):
        if name is None:
            mock_fetch = AsyncMock(return_value=None)
        else:
            mock_user = MagicMock()
            mock_user.name = name
            mock_user.id = user_id
            mock_fetch = AsyncMock(return_value=mock_user)
        self.patches.append(patch.object(self.mock_context.bot, "fetch_user", mock_fetch))
        return self

    def bot_fetch_chatters_color(self, return_value: str = "FF4500"):
        mock_color = MagicMock()
        mock_color.hex_clean = return_value
        mock_chatter = MagicMock()
        mock_chatter.color = mock_color if return_value else return_value
        mock_fetch = AsyncMock(return_value=[mock_chatter])
        self.patches.append(patch.object(self.mock_context.bot, "fetch_chatters_color", mock_fetch))
        return self

    async def __aenter__(self):
        for patche in self.patches:
            self._stack.enter_context(patche)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._stack.aclose()
