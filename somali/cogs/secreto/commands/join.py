# -*- coding: utf-8 -*-
from somali.utils import roles
from somali import config, log
from somali.apis import Twitch
from somali.bots import TwitchBot
import sys, os , sqlite3
from somali.database.models.channel import Channel
from somali.cogs.basics.routines.new_channels import routine

# aliases = [""]
description = "Comando para mandar o boto para canais apos reiniciar, precisa de 'nick'"
extra_checks = [roles.owner]


async def command(ctx, name: str):
    bot: TwitchBot = TwitchBot(config)
    cu = "{}"
    name = name.lower()
    id = await Twitch.account_id(name)
    # try:
    #     print("Tentando entrar")
    #     ctx.bot.add_channel(name, id)
    #     # await ctx.bot.adiciona()
    # except:
    #     print("Falhou")


    try:
        sqliteConnection = sqlite3.connect('/home/pi/Desktop/Bots/Oboto/db.sqlite3')
        cursor = sqliteConnection.cursor()
        log.info("Successfully Connected to SQLite")

        sql1 = f'''INSERT INTO "main"."user"("id", "name")VALUES ({id}, '{name}');'''
        sql2 = f'''INSERT INTO "main"."channel"("banwords", "disabled", "prefix", "user_id")VALUES ('{cu}', '{cu}', '+', '{id}');'''

        try:
            try:
                count1 = cursor.execute(sql1)
            except:
                log.info("Failed to insert data into sqlite table")
            
        finally:
            try:
                count1 = cursor.execute(sql2)
            except:
                log.info("Failed to insert data into sqlite table")

        sqliteConnection.commit()
        log.info("Record inserted successfully into SqliteDb_developers table ")
        cursor.close()

    except sqlite3.Error as error:
        log.info("Failed to insert data into sqlite table")
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            ctx.response = f"Entrei em {name} com sucesso, agora é so reinicar."
            log.info("The SQLite connection is closed")
            log.info("Tentando reinicar")
            await ctx.bot.adiciona()
            
