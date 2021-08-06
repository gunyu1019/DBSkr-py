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

from typing import Union, Dict, Sequence, List

from .enums import WidgetType
from .errors import *
from .https import HttpClient
from .models import Stats, Vote, VotedUser, Bot, User, Search
from .widget import Widget

log = logging.getLogger(__name__)


class Client:
    """ discord.py 에 있는 `discord.Client`를 기반으로 한 Top.gg 클라이언트에 연결됩니다.
    이 클래스를 통하여 Top.gg API에 연결됩니다.

    일부 옵션은 `discord.Client`를 통하여 전달될 수 있습니다.

    Parameters
    ----------
    bot: discord.Client
        discord.py의 클라이언트입니다.
        Client 대신 `AutoShardedClient`, `Bot`, `AutoShardedBot`를 넣을 수도 있습니다.
    token: Optional[str]
        Top.gg 에서 발급받은 봇의 토큰 키값 입니다. 데이터를 반영하거나 불러올 때 토큰 값이 사용됩니다.
    session: Optional[aiohttp.ClientSession]
        HttpClient 를 위한 aiohttp 의 ClientSession 클래스 입니다.
        기본값은 None이며, 자동으로 ClientSession을 생성하게 됩니다.
    loop: Optional[asyncio.AbstractEventLoop]
        비동기를 사용하기 위한 asyncio.AbstractEventLoop 입니다.
        기본값은 None이거나 bot 오브젝트가 들어왔을 때에는 bot.loop 입니다.
        기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.
    autopost: Optional[bool]
        자동으로 길드 정보를 등록된 토큰 값을 통하여 전송할지 설정합니다. 기본값은 False 입니다.
    autopost_interval: Optional[int]
        `autopost` 를 활성화하였을 때 작동하는 매개변수 입니다. 초단위로 주기를 설정합니다.
        기본값은 3600초(30분) 간격으로 설정됩니다. 만약 설정할 경우 무조건 900분(15분) 이상 설정해야합니다.
    """
    def __init__(self,
                 bot: discord.Client, token: str = None,
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
            if self.autopost_interval < 900:
                raise ClientException("topgg must be greater than or equal to 900 seconds(15 minutes)")

            self.autopost_task = self.loop.create_task(self._auto_post())

    async def _auto_post(self):
        """
        본 함수는 코루틴(비동기)함수 입니다.

        `discord.Client`의 .guilds 값에 있는 목록의 갯수를 읽어서 `stats()`를 통하여 Top.gg API로 자동으로 보냅니다.
        본 함수가 정상적으로 작동하기 위해서는 토큰 값이 필수로 필요합니다.
        """
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            try:
                log.info('Autoposting guild count to topgg.')
                if isinstance(self.client, discord.AutoShardedClient):
                    shard_id = self.client.shard_id
                    shard_count = self.client.shard_count
                    await self.stats(shard_count=shard_count, shard_id=shard_id)
                else:
                    await self.stats()
            except TooManyRequests:
                log.warning("Failed autopost guild count to topgg. (Too Many Requests(429))")
                pass
            await asyncio.sleep(self.autopost_interval)

    def guild_count(self) -> int:
        """`discord.Client`의 .guilds 값에 있는 목록의 갯수를 읽어옵니다."""
        return len(self.client.guilds)

    async def stats(self,
                    guild_count: Union[int, list] = None,
                    shard_id: int = None,
                    shard_count: int = None) -> Stats:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        봇 정보를 수신하거나 발신합니다.

        Parameters
        ----------
        guild_count: Optional[Union[int, list]]
            서버 갯수가 포함되어 있습니다.
            값이 비어있을 경우 `.guild_count`를 통하여 불러옵니다.
        shard_id: Optional[int]
            (Shard를 사용할 때만 해당됩니다.) 샤드의 ID 값이 포함됩니다.
        shard_count: Optional[int]
            (Shard를 사용할 때만 해당됩니다.) 샤드의 갯수가 포함됩니다.

        Returns
        -------
        Stats:
            Top.gg로 부터 들어온 봇 상태 정보가 포함되어 있습니다.
        """
        if guild_count is None:
            guild_count = self.guild_count()
        return await self.http.stats(bot_id=self.client.user.id, guild_count=guild_count,
                                     shard_id=shard_id, shard_count=shard_count)

    async def vote(self, user_id: int) -> Vote:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        `user_id`에 들어있는 사용자가 봇에 투표를 누른 여부에 대하여 불러옵니다.

        Parameters
        ----------
        user_id: int
            유저 ID 값이 포함되어 있습니다.

        Returns
        -------
        Vote:
            Top.gg로 부터 들어온 사용자 투표 정보에 대한 정보가 포함되어 있습니다.
        """
        return await self.http.vote(bot_id=self.client.user.id, user_id=user_id)

    async def votes(self) -> List[VotedUser]:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        투표를 누른 사용자 목록을 모두 불러옵니다.

        Returns
        -------
        List[VotedUser]:
            Top.gg로 부터 투표 누른 사용자 목록에 대한 정보가 포함되어 있습니다.
        """
        return await self.http.votes(bot_id=self.client.user.id)

    async def bot(self, bot_id: int = None) -> Bot:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        봇 정보를 불러옵니다.

        Parameters
        ----------
        bot_id: Optional[int]
            봇 ID 값이 포함됩니다. 봇 ID 값이 포함되질 않을 경우, 자신의 봇 ID가 들어갑니다.

        Returns
        -------
        Bot:
            Top.gg로 부터 들어온 봇 정보가 포함되어 있습니다.
        """
        if bot_id is None:
            bot_id = self.client.user.id
        return await self.http.bot(bot_id=bot_id)

    async def search(self,
                     sort: str = None,
                     search: Dict[str, str] = None,
                     fields: Sequence[str] = None,
                     limit: int = 50,
                     offset: int = 0) -> Search:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        Top.gg에서 봇을 검색합니다.

        Parameters
        ----------
        sort: Optional[str]
            정렬이 되는 기준이 포함됩니다.
        search: Optional[Dict[int]]
            검색할 디스코드 봇의 이름이 포함됩니다.
        fields: Sequence[str]
            표시할 쉼표로 구분된 필드 목록입니다. search 값에 ","로 구분을 할 경우 해당 값이 사용됩니다.
        limit: Optional[int]
            불러올 봇의 양의 갯수가 포함됩니다. 기본 값은 50개입니다. 최댓 값은 500개 입니다.
        offset: Optional[int]
            건너 뛸 디스코드 봇의 갯수가 포함됩니다. 기본 값은 0입니다.

        Returns
        -------
        Search:
            Top.gg로 부터 들어온 봇 정보가 포함되어 있습니다.
        """
        return await self.http.search(sort=sort, search=search, fields=fields, limit=limit, offset=offset)

    async def users(self, user_id: int) -> User:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        사용자 정보를 불러옵니다.

        Parameters
        ----------
        user_id: int
            사용자 ID 값이 포함됩니다.

        Returns
        -------
        User
            Top.gg로 부터 들어온 사용자 정보가 포함되어 있습니다.
        """
        return await self.http.users(user_id=user_id)

    def widget(self, bot_id: int = None, widget_type: WidgetType = None) -> Widget:
        """
        Top.gg를 통하여 디스코드 봇의 위젯 값을 불러옵니다.

        Parameters
        ----------
        widget_type: WidgetType
            위젯 유형값이 포함됩니다.
        bot_id: Optional[int]
            위젯에 사용되는 디스코드 봇 ID가 포함됩니다.

        Returns
        -------
        Widget:
            Top.gg의 위젯이 들어간 Assets 값이 리턴됩니다.
        """
        if bot_id is None:
            bot_id = self.client.user.id
        return self.http.widget(widget_type=widget_type, bot_id=bot_id)
