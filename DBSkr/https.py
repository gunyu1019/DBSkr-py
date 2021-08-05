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
from typing import List

from . import koreanbots
from . import topgg
from . import uniquebots

from .models import *
from .enums import WebsiteType


class HttpClient:
    """ DBSkr의 Http 클라이언트를 선언합니다.
     Http 클라이언트를 통하여 KoreanBots 클라이언트, top.gg 클라이언트, UniqueBots 클라이언트에 연결됩니다.
     이 클래스를 통하여 KoreanBots API와 top.gg API, UniqueBots API에 연결됩니다.

    Parameters
    ----------
    koreanbots_token: Optional[str]
        Koreanbots 에서 발급받은 봇의 토큰 키값 입니다. 해당 값을 설정하지 않을 경우 자동으로 활성화 되지 않습니다.
    topgg_token: Optional[str]
        Top.gg 에서 발급받은 봇의 토큰 키값 입니다. 해당 값을 설정하지 않을 경우 자동으로 활성화 되지 않습니다.
    uniquebots_token: Optional[str]
        UniqueBots 에서 발급받은 봇의 토큰 키값 입니다. 해당 값을 설정하지 않을 경우 자동으로 활성화 되지 않습니다.
    session: Optional[aiohttp.ClientSession]
        HttpClient 를 위한 aiohttp 의 ClientSession 클래스 입니다.
        기본값은 None이며, 자동으로 ClientSession을 생성하게 됩니다.
    loop: Optional[asyncio.AbstractEventLoop]
        비동기를 사용하기 위한 asyncio.AbstractEventLoop 입니다.
        기본값은 None 입니다.
        기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.
    """
    def __init__(self,
                 loop: asyncio.AbstractEventLoop = None,
                 session: aiohttp.ClientSession = None,
                 koreanbots_token: str = None,
                 topgg_token: str = None,
                 uniquebots_token: str = None):
        self.loop = loop
        self.koreanbots_token = koreanbots_token
        self.topgg_token = topgg_token
        self.uniquebots_token = uniquebots_token

        self.koreanbots_http = None
        self.topgg_http = None
        self.uniquebots_http = None
        if koreanbots_token is not None:
            self.koreanbots_http = koreanbots.HttpClient(token=self.koreanbots_token, session=session, loop=loop)
        if topgg_token is not None:
            self.topgg_http = topgg.HttpClient(token=self.topgg_token, session=session, loop=loop)
        if uniquebots_token is not None:
            self.uniquebots_http = uniquebots.HttpClient(token=self.uniquebots_token, session=session, loop=loop)

    async def bot(self, bot_id: int, web_type: List[WebsiteType] = None):
        """
        본 함수는 코루틴(비동기)함수 입니다.

        봇 정보를 불러옵니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.
        web_type: Optional[list[WebsiteType]]
            값을 불러올 웹사이트를 선택하실 수 있습니다. 기본 값은 토큰 유/무에 따른 모든 웹클라이언트에 발송됩니다.
            배열 안에 있는 웹사이트 유형에 따라 일부 정보만 불러올 수 있습니다.
        Returns
        -------
        WebsiteBot:
            웹사이트로 부터 들어온 봇 정보가 포함되어 있습니다.
        """
        if web_type is None:
            web_type = [WebsiteType.koreanbots, WebsiteType.topgg, WebsiteType.uniquebots]
        kbots = None
        tbots = None
        ubots = None

        if self.koreanbots_http is not None and self.koreanbots_token is not None \
                and WebsiteType.koreanbots in web_type:
            kbots = await self.koreanbots_http.bot(bot_id=bot_id)
        if self.topgg_http is not None and self.topgg_token is not None and WebsiteType.topgg in web_type:
            tbots = await self.topgg_http.bot(bot_id=bot_id)
        if self.uniquebots_http is not None and self.uniquebots_token is not None \
                and WebsiteType.uniquebots in web_type:
            ubots = await self.uniquebots_http.bot(bot_id=bot_id)
        return WebsiteBot(koreanbots=kbots, topgg=tbots, uniquebots=ubots)

    async def stats(self, bot_id: int, guild_count: int, web_type: List[WebsiteType] = None):
        if web_type is None:
            web_type = [WebsiteType.koreanbots, WebsiteType.topgg, WebsiteType.uniquebots]
        kbots = None
        tbots = None
        ubots = None

        if self.koreanbots_http is not None and self.koreanbots_token is not None \
                and WebsiteType.koreanbots in web_type:
            kbots = await self.koreanbots_http.stats(bot_id=bot_id, guild_count=guild_count)
        if self.topgg_http is not None and self.topgg_token is not None and WebsiteType.topgg in web_type:
            tbots = await self.topgg_http.stats(bot_id=bot_id, guild_count=guild_count)
        if self.uniquebots_http is not None and self.uniquebots_token is not None \
                and WebsiteType.uniquebots in web_type:
            ubots = await self.uniquebots_http.stats(bot_id=bot_id, guild_count=guild_count)
        return WebsiteStats(koreanbots=kbots, topgg=tbots, uniquebots=ubots)

    async def vote(self, bot_id: int, user_id: int, web_type: List[WebsiteType] = None):
        """
        본 함수는 코루틴(비동기)함수 입니다.

        `user_id`에 들어있는 사용자가 봇에 하트 혹은 투표를 누른 여부에 대하여 불러옵니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.
        user_id: int
            유저 ID 값이 포함되어 있습니다.
        web_type: Optional[List[WebsiteType]]
            값을 불러올 웹사이트를 선택하실 수 있습니다. 기본 값은 토큰 유/무에 따른 모든 웹클라이언트에 발송됩니다.
            배열 안에 있는 웹사이트 유형에 따라 일부 정보만 불러올 수 있습니다.

        Returns
        -------
        WebsiteVote:
            웹사이트로 부터 들어온 사용자 투표 정보에 대한 정보가 포함되어 있습니다.
        """
        if web_type is None:
            web_type = [WebsiteType.koreanbots, WebsiteType.topgg, WebsiteType.uniquebots]
        kbots = None
        tbots = None
        ubots = None

        if self.koreanbots_http is not None and self.koreanbots_token is not None \
                and WebsiteType.koreanbots in web_type:
            kbots = await self.koreanbots_http.vote(bot_id=bot_id, user_id=user_id)
        if self.topgg_http is not None and self.topgg_token is not None and WebsiteType.topgg in web_type:
            tbots = await self.topgg_http.vote(bot_id=bot_id, user_id=user_id)
        if self.uniquebots_http is not None and self.uniquebots_token is not None \
                and WebsiteType.uniquebots in web_type:
            ubots = await self.uniquebots_http.vote(bot_id=bot_id, user_id=user_id)
        return WebsiteVote(koreanbots=kbots, topgg=tbots, uniquebots=ubots)

    async def votes(self, bot_id: int, web_type: List[WebsiteType] = None):
        """
        본 함수는 코루틴(비동기)함수 입니다.

        하트 혹은 투표를 누른 사용자 목록을 모두 불러옵니다.

        Notes
        -----
        koreanbots 에서는 사용자 하트 목록을 불러오지 못합니다. topgg 혹은 uniquebots 모델만 사용이 가능합니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.
        web_type: Optional[List[WebsiteType]]
            값을 불러올 웹사이트를 선택하실 수 있습니다. 기본 값은 토큰 유/무에 따른 모든 웹클라이언트에 발송됩니다.
            배열 안에 있는 웹사이트 유형에 따라 일부 정보만 불러올 수 있습니다.

        Returns
        -------
        WebsiteVotes:
            웹사이트로 부터 들어온 봇 하트 정보가 포함되어 있습니다.
        """
        if web_type is None:
            web_type = [WebsiteType.koreanbots, WebsiteType.topgg, WebsiteType.uniquebots]
        tbots = None
        ubots = None

        if self.topgg_http is not None and self.topgg_token is not None \
                and WebsiteType.topgg in web_type:
            tbots = await self.topgg_http.votes(bot_id=bot_id)
        if self.uniquebots_http is not None and self.uniquebots_token is not None \
                and WebsiteType.uniquebots in web_type:
            ubots = await self.uniquebots_http.votes(bot_id=bot_id)
        return WebsiteVotes(topgg=tbots, uniquebots=ubots)

    async def users(self, user_id: int, web_type: List[WebsiteType] = None):
        """
        본 함수는 코루틴(비동기)함수 입니다.

        사용자 정보를 불러옵니다.

        Parameters
        ----------
        user_id: int
            사용자 ID 값이 포함됩니다.
        web_type: Optional[list[WebsiteType]]
            값을 불러올 웹사이트를 선택하실 수 있습니다. 기본 값은 토큰 유/무에 따른 모든 웹클라이언트에 발송됩니다.
            배열 안에 있는 웹사이트 유형에 따라 일부 정보만 불러올 수 있습니다.

        Returns
        -------
        WebsiteUser
            웹사이트로 부터 들어온 사용자 정보가 포함되어 있습니다.
        """
        if web_type is None:
            web_type = [WebsiteType.koreanbots, WebsiteType.topgg, WebsiteType.uniquebots]
        kbots = None
        tbots = None
        ubots = None

        if self.koreanbots_http is not None and self.koreanbots_token is not None \
                and WebsiteType.koreanbots in web_type:
            kbots = await self.koreanbots_http.users(user_id=user_id)
        if self.topgg_http is not None and self.topgg_token is not None and WebsiteType.topgg in web_type:
            tbots = await self.topgg_http.users(user_id=user_id)
        if self.uniquebots_http is not None and self.uniquebots_token is not None \
                and WebsiteType.uniquebots in web_type:
            ubots = await self.uniquebots_http.users(user_id=user_id)
        return WebsiteUser(koreanbots=kbots, topgg=tbots, uniquebots=ubots)
