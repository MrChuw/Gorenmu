from tortoise import Tortoise

from .tools import HelpMigration


async def migrate_bug_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))
    existing_columns = await helper.get_existing_columns("bug")
    sql_commands = []

    if "visto" in existing_columns and "viewed" not in existing_columns:
        sql_commands.append("ALTER TABLE bug CHANGE COLUMN visto viewed BOOLEAN DEFAULT FALSE;")

    if "resposta" in existing_columns and "response" not in existing_columns:
        sql_commands.append("ALTER TABLE bug CHANGE COLUMN resposta response TEXT DEFAULT NULL;")

    if "resposta_enviada" in existing_columns and "reminded" not in existing_columns:
        sql_commands.append("ALTER TABLE bug CHANGE COLUMN resposta_enviada reminded BOOLEAN DEFAULT FALSE;")

    if sql_commands:
        for sql in sql_commands:
            await helper.conn.execute_script(sql)
        print(sql_commands)
    # else:
    #     print("Nothing to migrate.")


async def migrate_bug():
    await migrate_bug_to_v2()
