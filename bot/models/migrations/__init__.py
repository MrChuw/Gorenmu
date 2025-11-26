from .annotation import migrate_annotation
from .bots_ignore import migrate_bots_ids
from .bug import migrate_bug
from .cookie import migrate_cookie
from .copypasta import migrate_copypasta
from .lottery import migrate_lottery
from .lottery_bank import migrate_lottery_bank
from .nick_history import migrate_nick_history
from .player_tower import migrate_player_tower
from .reminder import migrate_reminder
from .suggest import migrate_suggest
from .user import migrate_user
from .wedding import migrate_wedding

# TODO: To finish


async def migrations():
    await migrate_annotation()
    await migrate_bots_ids()
    await migrate_bug()
    await migrate_cookie()
    await migrate_copypasta()
    await migrate_lottery()
    await migrate_lottery_bank()
    await migrate_nick_history()
    await migrate_player_tower()
    await migrate_reminder()
    await migrate_suggest()
    await migrate_user()
    await migrate_wedding()
