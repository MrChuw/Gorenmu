

from tortoise.utils import get_schema_sql
from tortoise import Tortoise, run_async
import asyncio
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()








async def main():

    connection = Tortoise.get_connection("default")

    schema_sql = get_schema_sql(connection, True)

    schema_list = schema_sql.split(";")


    for tabela in schema_list:
        if "CREATE TABLE IF NOT EXISTS `loterica_banco`" in tabela:
            await connection.execute_query("ALTER TABLE loterica_banco RENAME TO lottery_bank")
            await asyncio.sleep(1)
            await connection.execute_query("ALTER TABLE lottery_bank RENAME COLUMN quantidade TO quantity;")
            await connection.execute_query("ALTER TABLE lottery_bank RENAME COLUMN encerrada_em TO closed_in;")
            await connection.execute_query("ALTER TABLE lottery_bank RENAME COLUMN encerrada TO closed;")
            await connection.execute_query("ALTER TABLE lottery_bank RENAME COLUMN acumulado TO accumulated;")
            await connection.execute_query("ALTER TABLE lottery_bank RENAME COLUMN numeros_sorteados TO drawn_numbers;")
            await connection.execute_query("ALTER TABLE lottery_bank RENAME COLUMN quantidade_acumulada TO accumulated_quantity;")
            pass

        if "CREATE TABLE IF NOT EXISTS `user`" in tabela:
            await connection.execute_query("ALTER TABLE user RENAME COLUMN apelido TO nickname;")
            pass

        if "CREATE TABLE IF NOT EXISTS `annotation`" in tabela:
            await connection.execute_query("ALTER TABLE loterica_banco RENAME TO lottery_bank")
            pass

        if "CREATE TABLE IF NOT EXISTS `bots_ids`" in tabela:
            await connection.execute_query("ALTER TABLE bots_ids RENAME COLUMN ativo TO active;")
            pass

        if "CREATE TABLE IF NOT EXISTS `bug`" in tabela:
            await connection.execute_query("ALTER TABLE bug RENAME COLUMN visto TO viewed;")
            await connection.execute_query("ALTER TABLE bug RENAME COLUMN resposta TO response;")
            await connection.execute_query("ALTER TABLE bug RENAME COLUMN resposta_enviada TO reminded;")
            pass

        if "CREATE TABLE IF NOT EXISTS `channel`" in tabela:
            await connection.execute_query("ALTER TABLE channel RENAME COLUMN removido TO removed;")
            pass

        if "CREATE TABLE IF NOT EXISTS `cookie`" in tabela:
            await connection.execute_query("ALTER TABLE cookie RENAME COLUMN comidos TO consumed;")
            await connection.execute_query("ALTER TABLE cookie RENAME COLUMN total TO total;")
            pass

        if "CREATE TABLE IF NOT EXISTS `copypasta`" in tabela:
            await connection.execute_query("ALTER TABLE copypasta RENAME COLUMN visivel TO visible;")
            pass

        if "CREATE TABLE IF NOT EXISTS `historico_de_nicks`" in tabela:
            await connection.execute_query("ALTER TABLE historico_de_nicks RENAME TO nick_history")
            pass

        if "CREATE TABLE IF NOT EXISTS `imgur`" in tabela:
            await connection.execute_query("ALTER TABLE loterica_banco RENAME TO lottery_bank")
            pass

        if "CREATE TABLE IF NOT EXISTS `imgur_agregado`" in tabela:
            await connection.execute_query("ALTER TABLE imgur_agregado RENAME TO imgur_aggregate")
            pass

        if "CREATE TABLE IF NOT EXISTS `lottery`" in tabela:
            await connection.execute_query("ALTER TABLE loterica RENAME TO lottery")
            await asyncio.sleep(1)
            await connection.execute_query("ALTER TABLE lottery RENAME COLUMN apostado TO bet_value;")
            await connection.execute_query("ALTER TABLE lottery RENAME COLUMN numeros TO numbers;")
            await connection.execute_query("ALTER TABLE lottery RENAME COLUMN encerrada TO closed;")
            await connection.execute_query("ALTER TABLE lottery RENAME COLUMN quantidade_ganha TO earned;")
            await connection.execute_query("ALTER TABLE lottery RENAME COLUMN encerrada_em TO closed_in;")
            await connection.execute_query("ALTER TABLE lottery RENAME COLUMN numero_do_sorteio TO draw_id;")
            await connection.execute_query("ALTER TABLE lottery RENAME COLUMN numeros_sorteados TO draw_sorted_numbers;")
            pass

        if "CREATE TABLE IF NOT EXISTS `markov_model_canais`" in tabela:
            await connection.execute_query("ALTER TABLE markov_model_canais RENAME TO markov_channels")
            pass

        if "CREATE TABLE IF NOT EXISTS `markov_model_user_canal`" in tabela:
            await connection.execute_query("ALTER TABLE markov_model_user_canal RENAME TO markov_user_channel")
            pass

        if "CREATE TABLE IF NOT EXISTS `markov_model_usuarios`" in tabela:
            await connection.execute_query("ALTER TABLE markov_model_usuarios RENAME TO markov_users")
            pass

        if "CREATE TABLE IF NOT EXISTS `mensage_logs`" in tabela:
            await connection.execute_query("ALTER TABLE mensage_logs RENAME TO message_logs")
            pass

        if "CREATE TABLE IF NOT EXISTS `pet`" in tabela:
            # await connection.execute_query("ALTER TABLE loterica_banco RENAME TO lottery_bank")
            pass

        if "CREATE TABLE IF NOT EXISTS `player`" in tabela:
            # await connection.execute_query("ALTER TABLE loterica_banco RENAME TO lottery_bank")
            pass

        if "CREATE TABLE IF NOT EXISTS `player_torre`" in tabela:
            await connection.execute_query("ALTER TABLE player_torre RENAME TO player_tower")
            await asyncio.sleep(1)
            await connection.execute_query("ALTER TABLE player_tower RENAME COLUMN encontro TO encounter;")
            await connection.execute_query("ALTER TABLE player_tower RENAME COLUMN andar TO floor;")
            await connection.execute_query("ALTER TABLE player_tower RENAME COLUMN zona TO zone;")
            await connection.execute_query("ALTER TABLE player_tower RENAME COLUMN encontro TO encounter;")
            pass

        if "CREATE TABLE IF NOT EXISTS `reminder`" in tabela:
            await connection.execute_query("ALTER TABLE reminder RENAME COLUMN enviado TO sent;")
            pass

        if "CREATE TABLE IF NOT EXISTS `status`" in tabela:
            await connection.execute_query("ALTER TABLE loterica_banco RENAME TO lottery_bank")
            pass

        if "CREATE TABLE IF NOT EXISTS `suggest`" in tabela:
            await connection.execute_query("ALTER TABLE suggest RENAME COLUMN visto TO viewed;")
            await connection.execute_query("ALTER TABLE suggest RENAME COLUMN resposta TO response;")
            await connection.execute_query("ALTER TABLE suggest RENAME COLUMN resposta_enviada TO reminded;")
            pass

        if "CREATE TABLE IF NOT EXISTS `wedding`" in tabela:
            await connection.execute_query("ALTER TABLE wedding RENAME COLUMN casados TO married;")
            await connection.execute_query("ALTER TABLE wedding RENAME COLUMN quem_separou TO who_separated;")
            pass






async def conectar():
    teste = {
        "connections": {
            "default": f"mysql://{os.getenv('DB_LOGIN')}:{os.getenv('DB_PASSWORD')}@127.0.0.1:"
                       f"3307/{os.getenv('DB_NAME')}"
        },
        "apps": {
            "models": {
                "models": ["models"],  # Substitua pelo caminho para seus modelos
                "default_connection": "default",
            }
        },
    }

    await Tortoise.init(config=teste)

    await main()




run_async(conectar())









