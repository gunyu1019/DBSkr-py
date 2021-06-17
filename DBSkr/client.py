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

import discord
import logging
import aiohttp
import asyncio

from .https import HttpClient
from .enums import WebsiteType
from .errors import ClientException

log = logging.getLogger(__name__)


class Client:
    def __init__(self,
                 bot: discord.Client,
                 koreanbots_token: str = None,
                 topgg_token: str = None,
                 uniquebots_token: str = None,
                 session: aiohttp.ClientSession = None,
                 loop: asyncio.ProactorEventLoop = None,
                 autopost: bool = True,
                 autopost_interval: int = 3600):
        self.koreanbots_token = koreanbots_token
        self.topgg_token = topgg_token
        self.uniquebots_token = uniquebots_token
        self.bot = bot
        self.http = HttpClient(koreanbots_token=koreanbots_token,
                               topgg_token=topgg_token,
                               uniquebots_token=uniquebots_token,
                               session=session)

        self.autopost = autopost
        self.autopost_interval: int = autopost_interval
        self.loop = loop
        if self.loop is not None:
            self.loop = self.bot.loop

        if autopost:
            if self.autopost_interval < 900:
                raise ClientException("autopost_interval must be greater than or equal to 900 seconds(15 minutes)")

            self.autopost_task = self.loop.create_task(self._auto_post())

    async def _auto_post(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            log.info('Autoposting guild count to UniqueBots.')
            await self.stats()
            await asyncio.sleep(self.autopost_interval)

    def guild_count(self) -> int:
        return len(self.bot.guilds)

    async def bot(self, bot_id: int = None, filter: WebsiteType = None):
        if bot_id is None:
            bot_id = self.bot.user.id
        return self.http.bot(bot_id=bot_id, filter=filter)

    async def stats(self, guild_count: int = None, filter: WebsiteType = None):
        if guild_count is None:
            guild_count = self.guild_count()
        return self.http.stats(bot_id=self.bot.user.id, guild_count=guild_count, filter=filter)

    async def vote(self, user_id: int, filter: WebsiteType = None):
        return await self.http.vote(bot_id=self.bot.user.id, user_id=user_id, filter=filter)

    async def votes(self, filter: WebsiteType = None) -> list:
        return await self.http.votes(bot_id=self.bot.user.id, filter=filter)

    async def users(self, user_id: int, filter: WebsiteType = None):
        return await self.http.users(user_id=user_id, filter=filter)
