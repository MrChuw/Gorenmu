from tortoise import Tortoise

from .tools import HelpMigration


async def migrate_lottery_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))
    if await helper.table_exists("loterica"):
        print("Renaming table 'loterica' to 'lottery'...")
        await helper.conn.execute_script("RENAME TABLE loterica TO lottery;")

    existing_columns = await helper.get_existing_columns("lottery")
    sql_commands = []

    if "apostado" in existing_columns and "bet_value" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery CHANGE COLUMN apostado bet_value INT;")

    if "numeros" in existing_columns and "numbers" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery CHANGE COLUMN numeros numbers JSON;")

    if "encerrada" in existing_columns and "closed" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery CHANGE COLUMN encerrada closed BOOLEAN;")

    if "quantidade_ganha" in existing_columns and "earned" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery CHANGE COLUMN quantidade_ganha earned INT;")

    if "encerrada_em" in existing_columns and "closed_in" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery CHANGE COLUMN encerrada_em closed_in DATETIME;")

    if "numeros_sorteados" in existing_columns and "draw_sorted_numbers" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery CHANGE COLUMN numeros_sorteados draw_sorted_numbers JSON;")

    if sql_commands:
        for sql in sql_commands:
            await helper.conn.execute_script(sql)
        print("Migrations executed:", sql_commands)
    # else:
    #     print("Nothing to migrate.")


async def migrate_lottery():
    await migrate_lottery_to_v2()
