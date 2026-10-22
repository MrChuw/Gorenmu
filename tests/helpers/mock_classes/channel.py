from datetime import date, datetime


class MockChannel:
    def __init__(
        self,
        channel_id: int = 1234567,
        channel_name: str = "xxcoolchannelxx",
        banwords: list | None = None,
        disabled: list | None = None,
        created_at: date | None = None,
        updated_at: date | None = None,
        online: bool = False,
        prefix: str = "",
    ):
        if not created_at:
            created_at = datetime.strptime("2025-01-01 06:00", "%Y-%m-%d %H:%M")
        if not updated_at:
            updated_at = datetime.strptime("2025-01-01 12:00", "%Y-%m-%d %H:%M")
        self.id: int = channel_id
        self.name: str = channel_name
        self.display_name: str = channel_name
        self.banwords: list = banwords if banwords is not None else []
        self.disabled: list = disabled if disabled is not None else []
        self.created_at: date = created_at
        self.updated_at: date = updated_at
        self.online: bool = online
        self.prefix: str = prefix
