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

import aiohttp

from . import koreanbots
from . import topgg
from . import uniquebots

from .models import *


class HttpClient:
    def __init__(self,
                 session: aiohttp.ClientSession = None,
                 koreanbots_token: str = None,
                 topgg_token: str = None,
                 uniquebots_token: str = None):
        self.koreanbots_token = koreanbots_token
        self.topgg_token = topgg_token
        self.uniquebots_token = uniquebots_token

        if koreanbots_token is None:
            self.koreanbots_http = koreanbots.HttpClient(token=self.koreanbots_token, session=session)
        if topgg_token is None:
            self.topgg_http = topgg.HttpClient(token=self.koreanbots_token, session=session)
        if uniquebots_token is None:
            self.uniquebots_http = uniquebots.HttpClient(token=self.koreanbots_token, session=session)

    async def bot(self, bot_id: int):
        kbots = await self.koreanbots_http.bot(bot_id=bot_id)
        tbots = await self.topgg_http.bot(bot_id=bot_id)
        ubots = await self.uniquebots_http.bot(bot_id=bot_id)
        return WebsiteBot(koreanbots=kbots, topgg=tbots, uniquebots=ubots)

    async def stats(self, bot_id: int, guild_count: int):
        kbots = await self.koreanbots_http.stats(bot_id=bot_id, guild_count=guild_count)
        tbots = await self.topgg_http.stats(bot_id=bot_id, guild_count=guild_count)
        ubots = await self.uniquebots_http.stats(bot_id=bot_id, guild_count=guild_count)
        return WebsiteStats(koreanbots=kbots, topgg=tbots, uniquebots=ubots)

    async def vote(self, bot_id: int, user_id: int):
        kbots = await self.koreanbots_http.vote(bot_id=bot_id, user_id=user_id)
        tbots = await self.topgg_http.vote(bot_id=bot_id, user_id=user_id)
        ubots = await self.uniquebots_http.vote(bot_id=bot_id, user_id=user_id)
        return WebsiteVote(koreanbots=kbots, topgg=tbots, uniquebots=ubots)

    async def votes(self, bot_id: int):
        tbots = await self.topgg_http.votes(bot_id=bot_id)
        ubots = await self.uniquebots_http.votes(bot_id=bot_id)
        return WebsiteVotes(topgg=tbots, uniquebots=ubots)

    async def users(self, user_id: int):
        kbots = await self.koreanbots_http.users(user_id=user_id)
        tbots = await self.topgg_http.users(user_id=user_id)
        ubots = await self.uniquebots_http.users(user_id=user_id)
        return WebsiteUser(koreanbots=kbots, topgg=tbots, uniquebots=ubots)
