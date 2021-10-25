# -*- coding: utf-8 -*-
from somali.utils import roles
import sqlite3
from sqlite3 import Error
from somali import config, log
from somali.apis import Twitch
from somali.bots import TwitchBot
from twitchio.ext.routines import Routine
import sys    
import os
import time
from somali.bots.twitch import TwitchBot

description = "Comando para reiniciar o boto inteiro"
extra_checks = [roles.owner]

async def command(ctx):
    try:
        print("No try do db")
        from somali.database import Database

        db: Database = Database(config.database_url)
    except Exception as e:
        log.critical(e, exc_info=1)
        sys.exit("[CRITICAL] Database constructor failure")
    try:
        print("No try do bot")
        from somali.bots import TwitchBot

        bot: TwitchBot = TwitchBot(config)
    except Exception as e:
        log.critical(e, exc_info=1)
        sys.exit("[CRITICAL] Twitch Bot constructor failure") 

    await db.close()
    time.sleep(3)
    log.info("Tentando reinicar")
    os.execv(sys.executable, ['python3.10'] + sys.argv)