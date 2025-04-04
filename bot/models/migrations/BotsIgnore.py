from tortoise import Tortoise

from .tools import HelpMigration


async def migrate_bots_ids_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))
    existing_columns = await helper.get_existing_columns("bots_ids")
    sql_commands = []

    if "ativo" in existing_columns and "active" not in existing_columns:
        sql_commands.append("ALTER TABLE bots_ids CHANGE COLUMN ativo active BOOLEAN;")

    if sql_commands:
        for sql in sql_commands:
            await helper.conn.execute_script(sql)
        print("Migrations executed:", sql_commands)
    # else:
    #     print("Nothing to migrate.")


async def migrate_bots_ids():
    await migrate_bots_ids_to_v2()
