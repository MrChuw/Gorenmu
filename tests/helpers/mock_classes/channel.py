from datetime import date, datetime


class MockChannel:
    def __init__(
        self,
        channel_id: int,
        channel_name: str,
        banwords: list = (),
        disabled: list = (),
        created_at: date | None = None,
        updated_at: date | None = None,
        online: bool = "",
        prefix: str = "",
    ):
        if not created_at:
            created_at = datetime.strptime("2025-01-01 06:00", "%Y-%m-%d %H:%M")
        if not updated_at:
            updated_at = datetime.strptime("2025-01-01 12:00", "%Y-%m-%d %H:%M")
        self.id: int = channel_id
        self.name: str = channel_name
        self.banwords: list = banwords
        self.disabled: list = disabled
        self.created_at: date = created_at
        self.updated_at: date = updated_at
        self.online: bool = online
        self.prefix: str = prefix
