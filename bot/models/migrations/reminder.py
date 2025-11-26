from tortoise import Tortoise

from .tools import HelpMigration


async def migrate_reminder_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))
    existing_columns = await helper.get_existing_columns("reminder")
    sql_commands = []

    # if "scheduled_for" in existing_columns:
    #     sql_commands.append("ALTER TABLE reminder MODIFY COLUMN scheduled_for DATE NULL;")

    if "enviado" in existing_columns and "sent" not in existing_columns:
        sql_commands.append("ALTER TABLE reminder CHANGE COLUMN enviado sent BOOLEAN DEFAULT FALSE;")

    if sql_commands:
        for sql in sql_commands:
            await helper.conn.execute_script(sql)
        print(sql_commands)
    # else:
    #     print("Nothing to migrate.")


async def migrate_reminder():
    await migrate_reminder_to_v2()
