from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from clickhouse_connect import create_async_client
from janus import Queue
from loguru import logger
from nltk.tokenize import WhitespaceTokenizer
from urlextract import URLExtract

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context
    from bot.ext.commands import User
    from bot.models import Channel as ChannelModel


# --- 1. MODELO DE DADOS ---


@dataclass
class MarkovEntry:
    scope: str
    user_id: int
    channel_id: int
    ngram_size: int
    prefix: str
    next_word: str
    count: int = 1

    def to_list(self):
        return [
            self.scope,
            self.user_id,
            self.channel_id,
            self.ngram_size,
            self.prefix,
            self.next_word,
            self.count,
        ]


# --- 2. ORM CLICKHOUSE ---


class MarkovORM:
    def __init__(
        self,
        bot: Gorenmu,
        host="localhost",
        port=15342,
        username="user",
        password="SuperSecretPassword",
        database="default",
    ):
        self.bot = bot
        self.config = {"host": host, "port": port, "username": username, "password": password, "database": database}
        self.client = None
        self.table = "markov_data"

    async def setup_database(self):
        if not self.client and not self.bot.mock:
            self.client = await create_async_client(**self.config)

        if not self.bot.mock:
            await self.client.command(f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
                scope LowCardinality(String) CODEC(ZSTD(3)),
                user_id UInt64 CODEC(ZSTD(1)),
                channel_id UInt64 CODEC(ZSTD(1)),
                ngram_size UInt8 CODEC(ZSTD(1)),
                prefix String CODEC(ZSTD(8)),
                next_word String CODEC(ZSTD(8)),
                count UInt64 CODEC(ZSTD(1)),
                created_at DateTime DEFAULT now() CODEC(DoubleDelta, ZSTD(1))
            ) ENGINE = SummingMergeTree(count)
            ORDER BY (scope, ngram_size, prefix, next_word);
            """)

    async def insert_batch(self, entries: list[MarkovEntry]):
        if not entries:
            return
        try:
            await self.client.insert(
                self.table,
                [e.to_list() for e in entries],
                column_names=[
                    "scope",
                    "user_id",
                    "channel_id",
                    "ngram_size",
                    "prefix",
                    "next_word",
                    "count",
                ],
            )
        except Exception as e:
            logger.error(f"Erro Clickhouse Insert: {e}")

    async def get_transition(
        self, prefix: str, scope: str, user_id: int, channel_id: int, ngram_size: int
    ) -> str | None:
        query = f"""
            SELECT next_word, sum(count) as weight FROM {self.table}
            WHERE prefix = %s AND scope = %s AND user_id = %s AND channel_id = %s AND ngram_size = %s
            GROUP BY next_word ORDER BY weight DESC LIMIT 25
        """
        try:
            res = await self.client.query(query, [prefix, scope, user_id, channel_id, ngram_size])
            if not res.result_rows:
                return None
            words, weights = zip(*[(r[0], r[1]) for r in res.result_rows], strict=False)
            return random.choices(words, weights=weights, k=1)[0]
        except Exception as e:
            logger.error(f"Erro Clickhouse Query: {e}")
            return None

    async def check_transition_exists(
        self, prefix: str, next_word: str, scope: str, user_id: int, channel_id: int, ngram_size: int
    ) -> bool:
        query = f"""
            SELECT count() FROM {self.table}
            WHERE prefix = %s AND next_word = %s AND scope = %s AND user_id = %s AND channel_id = %s AND ngram_size = %s
        """
        res = await self.client.query(query, [prefix, next_word, scope, user_id, channel_id, ngram_size])
        return res.result_rows[0][0] > 0


class MarkovProcessor:
    def __init__(self, bot_self):
        self.bot: Gorenmu = bot_self
        self.bots_ids = bot_self.bots_ids
        self.orm: MarkovORM | None = None
        self.queue: Queue | None = None
        self.url_extractor = URLExtract()
        self.tokenizer = WhitespaceTokenizer()

    async def train_message(self, message: str, channel: ChannelModel, user: User) -> dict[str, Any]:
        if user.id in self.bots_ids or self.url_extractor.find_urls(message):
            return {"processed": False}

        words = self.tokenizer.tokenize(message)
        if len(words) < 3:
            return {"processed": False, "reason": "short"}

        batch_to_insert = []
        for n in [3, 4]:
            full_seq = (["<s>"] * (n - 1)) + words + ["</s>"]

            for i in range(len(full_seq) - n):
                prefix = " ".join(full_seq[i : i + (n - 1)])
                next_word = " ".join(full_seq[i + 1 : i + n])
                if not next_word or "</s>" in prefix:
                    continue

                batch_to_insert.append(MarkovEntry("channel", 0, channel.user_id, n, prefix, next_word))
                batch_to_insert.append(MarkovEntry("user", user.id, 0, n, prefix, next_word))
                batch_to_insert.append(MarkovEntry("user_channel", user.id, channel.user_id, n, prefix, next_word))

        await self.orm.insert_batch(batch_to_insert)
        return {"processed": True}

    async def generate(
        self,
        seed: str | None = None,
        channel: ChannelModel | None = None,
        user: User | None = None,
        max_length: int = 30,
    ) -> str:
        uid, cid = (user.id if user else 0), (channel.user_id if channel else 0)
        scope = "user_channel" if (channel and user) else ("channel" if channel else "user")

        output = []

        if seed:
            trigger = seed.strip()
            if await self.orm.check_transition_exists("<s> <s>", trigger, scope, uid, cid, 3):
                output = ["<s>", "<s>", trigger]
            elif await self.orm.check_transition_exists("<s>", trigger, scope, uid, cid, 2):
                output = ["<s>", trigger]
            else:
                output = trigger.split()
        else:
            start = await self.orm.get_transition("<s> <s>", scope, uid, cid, 3) or await self.orm.get_transition(
                "<s>", scope, uid, cid, 2
            )
            if start:
                output = start.split()

        if not output:
            return ""

        for _ in range(max_length):
            next_block = None

            if len(output) >= 2:
                prefix = " ".join(output[-2:])
                next_block = await self.orm.get_transition(prefix, scope, uid, cid, 3)

            if not next_block and len(output) >= 1:
                prefix = output[-1]
                next_block = await self.orm.get_transition(prefix, scope, uid, cid, 2)

            if not next_block or "</s>" in next_block:
                break

            new_words = next_block.split()
            output.append(new_words[-1])

        clean_output = [w for w in output if w not in ("<s>", "</s>")]

        return " ".join(clean_output)

    async def put_markov_queue(self, ctx: Context):
        if not self.queue:
            return
        await self.queue.async_q.put((ctx.message.text, ctx.bot.channels[ctx.channel.name], ctx.user))

    async def markov_worker(self):
        self.queue = Queue()
        self.orm = MarkovORM(self.bot)
        # await self.orm.setup_database()

        while True:
            try:
                message, channel, user = await self.queue.async_q.get()
                try:
                    await self.train_message(message=message, channel=channel, user=user)
                except Exception as e:
                    logger.exception(f"Erro ao processar mensagem Markov no worker: {e}")
                finally:
                    self.queue.async_q.task_done()
            except asyncio.CancelledError:
                break

    async def setup(self):
        if not self.bot.mock:
            self.bot.MarkovTask = asyncio.create_task(self.markov_worker(), name="markov_worker")

    async def teardown(self) -> None:
        self.bot.MarkovTask.cancel()
