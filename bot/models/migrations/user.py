from tortoise import Tortoise

from .tools import HelpMigration


async def migrate_user_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))
    existing_columns = await helper.get_existing_columns("user")
    sql_commands = []

    if "apelido" in existing_columns and "nickname" not in existing_columns:
        sql_commands.append("ALTER TABLE user CHANGE COLUMN apelido nickname VARCHAR(32) NULL;")

    if "language" not in existing_columns:
        sql_commands.append("ALTER TABLE user ADD COLUMN language VARCHAR(32) NULL;")

    if "timezone" not in existing_columns:
        sql_commands.append("ALTER TABLE user ADD COLUMN timezone VARCHAR(50) NOT NULL DEFAULT 'UTC';")

    if "city_hidden" not in existing_columns:
        sql_commands.append("ALTER TABLE user ADD COLUMN city_hidden BOOLEAN DEFAULT TRUE NOT NULL;")

    if sql_commands:
        for sql in sql_commands:
            await helper.conn.execute_script(sql)
        print(sql_commands)
    # else:
    #     print("Nothing to migrate.")


async def migrate_user():
    await migrate_user_to_v2()
