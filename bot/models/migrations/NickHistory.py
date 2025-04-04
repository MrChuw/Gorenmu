from tortoise import Tortoise

from .tools import HelpMigration


async def migrate_nick_history_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))

    if await helper.table_exists("historico_de_nicks"):
        print("Renaming table 'historico_de_nicks' to 'nick_history'...")
        await helper.conn.execute_script("RENAME TABLE historico_de_nicks TO nick_history;")

    existing_columns = await helper.get_existing_columns("nick_history")


async def migrate_nick_history():
    await migrate_nick_history_to_v2()
