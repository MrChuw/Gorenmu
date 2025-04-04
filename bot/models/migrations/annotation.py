from tortoise import Tortoise

from .tools import HelpMigration


async def migrate_annotation_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))
    existing_columns = await helper.get_existing_columns("annotation")
    sql_commands = []

    if "title" not in existing_columns:
        sql_commands.append("ALTER TABLE annotation ADD COLUMN title VARCHAR(32) NULL;")

    if "deleted" not in existing_columns:
        sql_commands.append("ALTER TABLE annotation ADD COLUMN deleted BOOLEAN DEFAULT FALSE;")

    if sql_commands:
        for sql in sql_commands:
            await helper.conn.execute_script(sql)
        print(sql_commands)
    # else:
    #     print("Nothing to migrate.")


async def migrate_annotation():
    await migrate_annotation_to_v2()
