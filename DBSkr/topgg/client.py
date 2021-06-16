"""MIT License

Copyright (c) 2021 gunyu1019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import aiohttp
import logging
import discord

from typing import Union, Dict, Sequence

from .enums import WidgetType
from .errors import *
from .https import HttpClient
from .models import Stats, Vote, VotedUser, Bot, User, Search
from .widget import Widget

log = logging.getLogger(__name__)


class Client:
    def __init__(self,
                 bot: discord.Client, token: str = None,
                 session: aiohttp.ClientSession = None,
                 loop: asyncio.ProactorEventLoop = None,
                 autopost: bool = True,
                 autopost_interval: int = 3600):
        self.token = token
        self.bot = bot
        self.http = HttpClient(token=token, session=session)

        self.autopost = autopost
        self.autopost_interval: int = autopost_interval
        self.loop = loop
        if self.loop is not None:
            self.loop = self.bot.loop

        if autopost:
            if self.autopost_interval < 900:
                raise ClientException("topgg must be greater than or equal to 900 seconds(15 minutes)")

            self.autopost_task = self.loop.create_task(self._auto_post())

    async def _auto_post(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                log.info('Autoposting guild count to topgg.')
                if isinstance(self.bot, discord.AutoShardedClient):
                    shard_id = self.bot.shard_id
                    shard_count = self.bot.shard_count
                    await self.stats(shard_count=shard_count, shard_id=shard_id)
                else:
                    await self.stats()
            except TooManyRequests:
                log.warning("Failed autopost guild count to topgg. (Too Many Requests(429))")
                pass
            await asyncio.sleep(self.autopost_interval)

    def guild_count(self) -> int:
        return len(self.bot.guilds)

    async def stats(self,
                    guild_count: Union[int, list] = None,
                    shard_id: int = None,
                    shard_count: int = None) -> Stats:
        if guild_count is None:
            guild_count = self.guild_count()
        return await self.http.stats(bot_id=self.bot.user.id, guild_count=guild_count,
                                     shard_id=shard_id, shard_count=shard_count)

    async def vote(self, user_id: int) -> Vote:
        return await self.http.vote(bot_id=self.bot.user.id, user_id=user_id)

    async def votes(self) -> VotedUser:
        return await self.http.votes(bot_id=self.bot.user.id)

    async def bot(self, bot_id: int = None) -> Bot:
        if bot_id is None:
            bot_id = self.bot.user.id
        return await self.http.bot(bot_id=bot_id)

    async def search(self,
                     sort: str = None,
                     search: Dict[str, str] = None,
                     fields: Sequence[str] = None,
                     limit: int = 50,
                     offset: int = 0) -> Search:
        return await self.http.search(sort=sort, search=search, fields=fields, limit=limit, offset=offset)

    async def users(self, user_id: int) -> User:
        return await self.http.users(user_id=user_id)

    def widget(self, bot_id: int, widget_type: WidgetType = None) -> Widget:
        if bot_id is None:
            bot_id = self.bot.user.id
        return self.http.widget(widget_type=widget_type, bot_id=bot_id)
