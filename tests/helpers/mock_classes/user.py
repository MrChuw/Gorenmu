from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...


class MockUser:
    def __init__(
        self,
        user_id: int = 1234567,
        name: str = "xxcoolnickxx",
        color: str = "",
        channel: str = "",
        saved_color: str = "",
        city: str = "",
        ping: str = "",
        mention: bool = True,
        block: bool = False,
        sponsor: bool = True,
        apelido: str = "",
        content: str = "",
        created_at: date = "",
        updated_at: date = "",
        nick_history: dict | None = None,
    ):
        if nick_history is None:
            nick_history = []
        self.id: int = user_id
        self.name: str = name
        self.color: str = color
        self.channel: str = channel
        self.saved_color: str = saved_color
        self.city: str = city
        self.ping: str = ping
        self.mention: bool = mention
        self.block: bool = block
        self.sponsor: bool = sponsor
        self.apelido: str = apelido
        self.content: str = content
        self.nick_history: list = nick_history
        self.created_at: date = created_at
        self.updated_at: date = updated_at
        self.profile_image: str = ""
