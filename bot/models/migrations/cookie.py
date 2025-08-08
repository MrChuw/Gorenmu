from datetime import UTC, datetime, timedelta

from tortoise import Tortoise
from tortoise.expressions import Q

from bot.models import Cookies

from .tools import HelpMigration


async def migrate_cookies_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))
    existing_columns = await helper.get_existing_columns("cookie")
    sql_commands = []

    if "cooldown" not in existing_columns:
        sql_commands.append("ALTER TABLE cookie ADD COLUMN cooldown DATETIME NULL;")

    if "comidos" in existing_columns and "consumed" not in existing_columns:
        sql_commands.append("ALTER TABLE cookie CHANGE COLUMN comidos consumed INT;")

    if "stocked" in existing_columns:
        sql_commands.append("ALTER TABLE cookie MODIFY COLUMN stocked INT DEFAULT 10;")

    if "daily" in existing_columns:
        seed = datetime.now().toordinal()
        now = datetime.now(UTC)

        cookies = await Cookies.exclude(Q(daily=None) | Q(daily=0))

        for cookie in cookies:
            amount = seed - cookie.daily
            cooldown = now - timedelta(hours=6 * amount)
            cookie.cooldown = cooldown
            cookie.daily = 0
            await cookie.save()

    if sql_commands:
        for sql in sql_commands:
            await helper.conn.execute_script(sql)
        print(sql_commands)
    # else:
    #     print("Nothing to migrate.")


async def migrate_cookie():
    await migrate_cookies_to_v2()
