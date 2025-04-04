from tortoise import Tortoise

from .tools import HelpMigration


async def migrate_wedding_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))
    existing_columns = await helper.get_existing_columns("wedding")
    sql_commands = []

    if "casados" in existing_columns and "active_marriage" not in existing_columns:
        sql_commands.append("ALTER TABLE wedding CHANGE COLUMN casados active_marriage BOOLEAN;")

    if "quem_separou" in existing_columns and "who_separated" not in existing_columns:
        sql_commands.append("ALTER TABLE wedding CHANGE COLUMN quem_separou who_separated INT;")

    if sql_commands:
        for sql in sql_commands:
            await helper.conn.execute_script(sql)
        print("Migrations executed:", sql_commands)
    # else:
    #     print("Nothing to migrate.")


async def migrate_wedding():
    await migrate_wedding_to_v2()
