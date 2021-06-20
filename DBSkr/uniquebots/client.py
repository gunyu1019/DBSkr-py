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

from .errors import *
from .https import HttpClient
from .models import Stats, Vote, Bot, User

log = logging.getLogger(__name__)


class Client:
    def __init__(self,
                 bot: discord.Client,
                 token: str = None,
                 session: aiohttp.ClientSession = None,
                 loop: asyncio.AbstractEventLoop = None,
                 autopost: bool = True,
                 autopost_interval: int = 3600):
        self.token = token
        self.client = bot

        self.loop = loop or self.client.loop
        self.http = HttpClient(token=token, session=session, loop=self.loop)

        self.autopost = autopost
        self.autopost_interval: int = autopost_interval

        if autopost:
            if self.autopost_interval < 180:
                raise ClientException("autopost_interval must be greater than or equal to 3 minutes")

            self.autopost_task = self.loop.create_task(self._auto_post())

    async def _auto_post(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            log.info('Autoposting guild count to UniqueBots.')
            await self.stats()
            await asyncio.sleep(self.autopost_interval)

    def guild_count(self) -> int:
        return len(self.client.guilds)

    async def stats(self, guild_count: int = None) -> Stats:
        if guild_count is None:
            guild_count = self.guild_count()
        return await self.http.stats(bot_id=self.client.user.id, guild_count=guild_count)

    async def vote(self, user_id: int) -> Vote:
        return await self.http.vote(bot_id=self.client.user.id, user_id=user_id)

    async def bot(self, bot_id: int = None) -> Bot:
        if bot_id is None:
            bot_id = self.client.user.id
        return await self.http.bot(bot_id=bot_id)

    async def votes(self) -> list:
        return await self.http.votes(bot_id=self.client.user.id)

    async def users(self, user_id: int, filter = None) -> User:
        return await self.http.users(user_id=user_id)
