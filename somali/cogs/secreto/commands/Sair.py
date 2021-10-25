# -*- coding: utf-8 -*-
from somali.utils import roles
from somali import config, log
from somali.apis import Twitch
from somali.bots import TwitchBot
import sys, os , sqlite3

# aliases = [""]
description = "Comando para mandar o boto para canais apos reiniciar, precisa de 'nick'"
extra_checks = [roles.owner]


async def command(ctx, name: str):
    bot: TwitchBot = TwitchBot(config)
    cu = "{}"
    id = await Twitch.account_id(name)
    try:
        sqliteConnection = sqlite3.connect('/home/pi/Desktop/Bots/Oboto/db.sqlite3')
        cursor = sqliteConnection.cursor()
        log.info("Successfully Connected to SQLite")

        sql2 = f'''DELETE FROM "main"."channel" WHERE user_id = {id};'''
        count1 = cursor.execute(sql2)

        sqliteConnection.commit()
        log.info("Record inserted successfully into SqliteDb_developers table ")
        cursor.close()

    except sqlite3.Error as error:
        log.info("Failed to insert data into sqlite table")
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            ctx.response = f"Sai do canal de {name} com sucesso, agora é so reinicar."
            log.info("The SQLite connection is closed")
            log.info("Tentando reinicar")


