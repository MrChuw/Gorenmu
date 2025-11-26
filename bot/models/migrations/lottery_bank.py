from tortoise import Tortoise

from .tools import HelpMigration


async def migrate_lottery_bank_to_v2():
    helper = HelpMigration(Tortoise.get_connection("default"))

    if await helper.table_exists("loterica_banco"):
        print("Renaming table 'loterica_banco' to 'lottery_bank'...")
        await helper.conn.execute_script("RENAME TABLE loterica_banco TO lottery_bank;")

    existing_columns = await helper.get_existing_columns("lottery_bank")
    sql_commands = []

    if "quantidade" in existing_columns and "quantity" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery_bank CHANGE COLUMN quantidade quantity INT;")

    if "encerrada_em" in existing_columns and "closed_in" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery_bank CHANGE COLUMN encerrada_em closed_in DATETIME;")

    if "encerrada" in existing_columns and "closed" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery_bank CHANGE COLUMN encerrada closed BOOLEAN;")

    if "acumulado" in existing_columns and "accumulated" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery_bank CHANGE COLUMN acumulado accumulated BOOLEAN;")

    if "numeros_sorteados" in existing_columns and "drawn_numbers" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery_bank CHANGE COLUMN numeros_sorteados drawn_numbers JSON;")

    if "quantidade_acumulada" in existing_columns and "accumulated_quantity" not in existing_columns:
        sql_commands.append("ALTER TABLE lottery_bank CHANGE COLUMN quantidade_acumulada accumulated_quantity INT;")

    if sql_commands:
        for sql in sql_commands:
            await helper.conn.execute_script(sql)
        print("Migrations executed:", sql_commands)
    # else:
    #     print("Nothing to migrate.")


async def migrate_lottery_bank():
    await migrate_lottery_bank_to_v2()
