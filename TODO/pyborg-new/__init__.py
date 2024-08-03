import asyncio

import click
from tortoise import Tortoise

from models import Mensage_log


# logger.stop()


#  self.words https://im.mrchuw.com.br/197387.png
# self.lines https://im.mrchuw.com.br/8fe0d0.png

def custom_get_app_dir(app_name):
    custom_path = "./pyborg_stuff"
    return custom_path


# Sobrescreve a função padrão
click.get_app_dir = custom_get_app_dir


# Inicializando o banco de dados SQLite
async def init_sqlite():
    # await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"sqlite_db": ["models_sql"]})
    await Tortoise.init({
            "connections": {
                "sqlite_db": "mysql://gorenmu:gorenmu_password@127.0.0.1:3308/gorenmu",
            },
            "apps": {
                "models_sqlite": {"models": ["models_sql"], "default_connection": "sqlite_db",}
            }})
    await Tortoise.generate_schemas()


# Conectando ao banco de dados MySQL
async def init_mysql():
    await Tortoise.init(db_url='mysql://gorenmu:gorenmu_password@127.0.0.1:3307/gorenmu', modules={"models": ["models"]})


async def init_db():
    await Tortoise.init({
            "connections": {
                "sqlite_db": "mysql://gorenmu:gorenmu_password@127.0.0.1:3308/gorenmu",
                "mysql_db": "mysql://gorenmu:gorenmu_password@127.0.0.1:3307/gorenmu"
            },
            "apps": {
                "models_sqlite": {"models": ["models_sql"], "default_connection": "sqlite_db",},
                "models_mysql": {"models": ["models"], "default_connection": "mysql_db",}
            }})




# Função para obter mensagens iniciais do MySQL
async def get_initial_messages(limit):
    messages = await Mensage_log.all().limit(limit).values_list('content', flat=True)
    return list(messages)


# Função para obter mensagens adicionais do MySQL
async def get_additional_messages(start, limit):
    messages = await Mensage_log.all().offset(start).limit(limit).values_list('content', flat=True)
    return list(messages)



async def main():
    # await init_sqlite()
    # await init_mysql()
    await init_db()

    from pyborg_new import filter_messages, pyborg
    # from pyborg.pyborg import pyborg

    teste = pyborg()

    # teste.words, teste.lines = teste.load_brain_json("pyborg_stuff/brains/06-15-24-auto-458b.pyborg.json")



    from models_sql import Word

    #
    # word = await Word.filter(word="o").first().prefetch_related('lines')
    #
    # teset1 = await word.line_set
    #
    # teste2 = await word.greb_lines_and_indexs()
    #
    # line = await Line.all().first().prefetch_related('words')
    #
    # teste1 = await line.words


    start = 1000
    batch_size = 1000
    messages = filter_messages(await get_initial_messages(start), teste)

    for _ in range(10):
        start += batch_size
        await teste.learn(messages)
        messages = await get_additional_messages(start, batch_size)
        # if len(messages) == 0:
        messages = filter_messages(messages, teste)

    start += batch_size

    async def treinar(start, batch_size):
        for _ in range(10):
            messages = filter_messages(await get_additional_messages(start, batch_size), teste)
            await teste.learn(messages)
            start += batch_size
        return start

    # import nltk
    # nltk.download('averaged_perceptron_tagger')
    # nltk.download('universal_tagset')

    # json_data = networkx_demo(teste)

    # pprint(json_data)

    # return

    while True:
        # string = input("digita ai: ")
        string = await Word.random_word()
        if string == "exit":
            break
        if string.startswith("learn") or string == "learn":
            if len(string.split()) == 1:
                batch_size = 1000
            else:
                batch_size = int(string.split()[1])
            start = await treinar(start, batch_size)

        print(await teste.reply(string))

    ...


asyncio.run(main())


