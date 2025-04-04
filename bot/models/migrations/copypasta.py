from tortoise import Tortoise

from .tools import HelpMigration


async def migrate_copypasta_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))
    existing_columns = await helper.get_existing_columns("copypasta")
    sql_commands = []

    if "visivel" in existing_columns and "visible" not in existing_columns:
        sql_commands.append("ALTER TABLE copypasta CHANGE COLUMN visivel visible BOOLEAN;")

    if sql_commands:
        for sql in sql_commands:
            await helper.conn.execute_script(sql)
        print("Migrations executed:", sql_commands)
    # else:
    #     print("Nothing to migrate.")


async def migrate_copypasta():
    await migrate_copypasta_to_v2()
