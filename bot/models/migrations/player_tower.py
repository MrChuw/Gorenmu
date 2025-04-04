from tortoise import Tortoise
from .tools import HelpMigration


async def migrate_player_torre_to_player_tower():
    helper = HelpMigration(Tortoise.get_connection("default"))

    if await helper.table_exists("historico_de_nicks"):
        print("Renaming table 'historico_de_nicks' to 'player_tower'...")
        await helper.conn.execute_script("RENAME TABLE historico_de_nicks TO player_tower;")



async def migrate_player_tower():
    await migrate_player_torre_to_player_tower()
