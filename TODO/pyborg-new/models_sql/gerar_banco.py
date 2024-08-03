from tortoise import fields
from tortoise.models import Model
from tortoise import Tortoise
from tortoise import run_async
import asyncio
import random
import string
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model

class Line(Model):
    hashval = fields.BigIntField(pk=True, index=True)
    content = fields.TextField()
    num_context = fields.IntField()
    words = fields.ManyToManyField('models_sqlite.Word', related_name='line_set')

    class Meta:
        table = "line"

class Word(Model):
    id = fields.IntField(pk=True)
    word = fields.CharField(max_length=255)
    lines = fields.ManyToManyField('models_sqlite.Line', related_name='word_line')
    indexs = fields.JSONField(default=[])

    class Meta:
        table = "word"


async def init_db():
    # Configuração do Tortoise ORM
    await Tortoise.init({
        'connections': {
            'models_sqlite':"mysql://gorenmu:gorenmu_password@127.0.0.1:3308/gorenmu",
        },
        'apps': {
            'models_sqlite': {'models': ['__main__'], 'default_connection': 'models_sqlite',}
        }
    })

    # Inicializa as tabelas no banco de dados
    await Tortoise.generate_schemas()

    # quantidade = 10
    #
    # num_lines = quantidade
    # num_words = quantidade * 3
    #
    # # Create random Word instances
    # word_instances = []
    # for _ in range(num_words):
    #     word_text = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
    #     word = await Word.create(word=word_text)
    #     word_instances.append(word)
    #
    # # Create random Line instances and associate random words
    # for _ in range(num_lines):
    #     line_content = ' '.join(random.choices([w.word for w in word_instances], k=random.randint(3, 10)))
    #     line_hashval = random.randint(1, 1000000000)
    #     line_num_context = random.randint(1, 10)
    #     line = await Line.create(hashval=line_hashval, content=line_content, num_context=line_num_context)
    #
    #     # Associate random words to the line
    #     num_line_words = random.randint(1, min(num_words, 10))  # number of words in the line
    #     selected_words = random.sample(word_instances, num_line_words)
    #     for index, word in enumerate(selected_words):
    #         await LineWord.create(line=line, word=word, index=index)
    #
    # while True:
    #     await asyncio.sleep(0.1)
    #     line = await Line.all()
    #     word = await Word.all()
    #     line_word = await LineWord.all()
    #     teste = await line_word[0].line
    #     teste2 = await line_word[0].word
    #     teste3 = await line[0].words
    #     teste4 = await word[0].lines
    #     break


run_async(init_db())