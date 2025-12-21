from __future__ import annotations

import asyncio
from collections import Counter
from typing import TYPE_CHECKING

from janus import Queue
from loguru import logger
from urlextract import URLExtract

from bot.ext import Context

if TYPE_CHECKING:
    from bot.ext.commands import User
    from bot.models import Channel as ChannelModel
    from bot.models import MarkovChannels, MarkovUserChannel, MarkovUsers


class MarkovProcessor:
    def __init__(self, bot_self):
        self.bots_ids = bot_self.bots_ids
        self.message_queue: Queue | None = None
        from nltk.tokenize import WhitespaceTokenizer

        from bot.models import MarkovChannels, MarkovUserChannel, MarkovUsers

        self.MarkovChannels = MarkovChannels
        self.MarkovUserChannel = MarkovUserChannel
        self.MarkovUsers = MarkovUsers
        self.whitespace_tokenizer = WhitespaceTokenizer()
        self.url_extractor = URLExtract()

    @staticmethod
    def is_repetitive(message: str, threshold: float = 0.6) -> bool:
        most_common_word_count = Counter(message.split()).most_common(1)[0][1]
        return most_common_word_count / len(message.split()) > threshold

    async def put_markov_queue(self, ctx: Context):
        await self.message_queue.async_q.put((ctx.message.text, ctx.bot.channels[ctx.channel.name], ctx.user))

    async def _get_current_state(self, curr_state: str, **kwargs):
        channel = kwargs.get("channel")
        user = kwargs.get("user")
        if channel and user:
            return await self.MarkovUserChannel.filter(curr_state=curr_state, channel=channel, user=user).first()
        elif channel:
            return await self.MarkovChannels.filter(curr_state=curr_state, channel=channel).first()
        elif user:
            return await self.MarkovUsers.filter(curr_state=curr_state, user=user).first()
        return None

    async def _create_state(self, curr_state: str, next_state: dict[str, int], **kwargs):
        channel = kwargs.get("channel")
        user = kwargs.get("user")
        try:
            if channel and user:
                await self.MarkovUserChannel.create(
                    curr_state=curr_state,
                    transition=next_state,
                    channel=channel,
                    user=user,
                )
            elif channel:
                await self.MarkovChannels.create(curr_state=curr_state, transition=next_state, channel=channel)
            elif user:
                await self.MarkovUsers.create(curr_state=curr_state, transition=next_state, user=user)
        except Exception as e:
            logger.error(e)

    @staticmethod
    async def _sort_save(curr_state: MarkovUserChannel | MarkovChannels | MarkovUsers, next_state: str):
        if next_state in curr_state.transition:
            curr_state.transition[next_state] += 1
            curr_state.transition = dict(sorted(curr_state.transition.items(), key=lambda x: x[1], reverse=True))
        else:
            curr_state.transition[next_state] = 1
        try:
            if curr_state:
                await curr_state.save()
        except Exception as e:
            logger.error(e)

    async def train_and_save_to_database(self, message, channel: ChannelModel, user: User, ngram=3):
        if self.url_extractor.find_urls(text=message):
            return

        words = self.whitespace_tokenizer.tokenize(text=message)
        words = ["<s>", *words, "</s>"]

        for i in range(len(words) - ngram + 1):
            await asyncio.sleep(0)
            curr_state = " ".join(words[i : i + ngram])
            next_state = " ".join(words[i + ngram : i + ngram + ngram])

            # Channel
            if user.id not in self.bots_ids:
                existing_curr_state = await self._get_current_state(curr_state=curr_state, channel=channel)
                if not existing_curr_state:
                    await self._create_state(
                        curr_state=curr_state,
                        next_state={next_state: 1},
                        channel=channel,
                    )
                else:
                    await self._sort_save(curr_state=existing_curr_state, next_state=next_state)

            # User
            existing_curr_state = await self._get_current_state(curr_state=curr_state, user=user)
            if not existing_curr_state:
                await self._create_state(curr_state=curr_state, next_state={next_state: 1}, user=user)
            else:
                await self._sort_save(curr_state=existing_curr_state, next_state=next_state)

            # User per channel
            existing_curr_state = await self._get_current_state(curr_state=curr_state, channel=channel, user=user)
            if not existing_curr_state:
                await self._create_state(
                    curr_state=curr_state,
                    next_state={next_state: 1},
                    channel=channel,
                    user=user,
                )

            else:
                await self._sort_save(curr_state=existing_curr_state, next_state=next_state)

            if "</s>" in next_state:
                break

    async def process_message(self):
        self.message_queue = Queue()
        while True:
            try:
                message, channel, user = await self.message_queue.async_q.get()

                words = self.whitespace_tokenizer.tokenize(text=message)
                if not self.is_repetitive(message) and len(words) <= 3:
                    return

                if self.message_queue.async_q.qsize() > 100:
                    logger.info(f"Queue size: {self.message_queue.async_q.qsize()}")

                await self.train_and_save_to_database(message, channel, user)

                self.message_queue.async_q.task_done()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error(e)
