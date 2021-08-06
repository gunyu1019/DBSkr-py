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

from .api import Api
from .models import Bot, Vote, Bots, Stats, User
from .enums import WidgetType, WidgetStyle
from .widget import Widget


class HttpClient:
    """ KoreanBots의 Http 클라이언트를 선언합니다.
     이 클래스를 통하여 KoreanBots API에 연결됩니다.

    Parameters
    ----------
    token: Optional[str]
        KoreanBots 에서 발급받은 봇의 토큰 키값 입니다. 일부 데이터를 반영하거나 불러올 때 토큰 값이 사용될 수 있습니다.
    session: Optional[aiohttp.ClientSession]
        HttpClient 를 위한 aiohttp 의 ClientSession 클래스 입니다.
        기본값은 None이며, 자동으로 ClientSession을 생성하게 됩니다.
    loop: Optional[asyncio.AbstractEventLoop]
        비동기를 사용하기 위한 asyncio.AbstractEventLoop 입니다.
        기본값은 None 입니다.
        기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.
    """
    def __init__(self,
                 token: str = None,
                 session: aiohttp.ClientSession = None,
                 loop: asyncio.AbstractEventLoop = None):
        self.token = token
        self.loop = loop
        self.requests = Api(token=token, session=session, loop=loop)
        self.session = session

    async def bot(self, bot_id: int) -> Bot:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        봇 정보를 불러옵니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.

        Returns
        -------
        Bot:
            KoreanBots로 부터 들어온 봇 정보가 포함되어 있습니다.
        """
        path = "/bots/{bot_id}".format(bot_id=bot_id)

        self.requests.version = 2
        result = await self.requests.get(path=path)
        return Bot(result)

    async def search(self, query: str, page: int = 1) -> Bots:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        KoreanBots에서 봇을 검색합니다.

        Parameters
        ----------
        query: str
            봇 ID 값이 포함됩니다. 봇 ID 값이 포함되질 않을 경우, 자신의 봇 ID가 들어갑니다.
        page: Optional[int]
            페이지 수가 포함됩니다.

        Returns
        -------
        Bots:
            KoreanBots로 부터 들어온 봇 정보가 포함되어 있습니다.
        """
        params = {
            "query": query,
            "page": page
        }
        path = "/v2/search/bots"

        self.requests.version = 2
        result = await self.requests.get(path=path, query=params)
        return Bots(result)

    async def new(self) -> Bots:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        KoreanBots에 새롭게 추가된 디스코드 봇을 불러옵니다.

        Returns
        -------
        Bots:
            KoreanBots로 부터 들어온 봇 정보가 포함되어 있습니다.
        """
        path = "/v2/list/bots/new"

        self.requests.version = 2
        result = await self.requests.get(path=path)
        return Bots(result)

    async def votes(self, page: int = 1) -> Bots:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        하트 수가 많은 순으로 디스코드 봇을 불러옵니다.

        Parameters
        ----------
        page: Optional[int]
            페이지 수가 포함됩니다.

        Returns
        -------
        Bots:
            KoreanBots로 부터 들어온 봇 정보가 포함되어 있습니다.
        """
        params = {
            "page": page
        }
        path = "/v2/list/bots/new"

        self.requests.version = 2
        result = await self.requests.get(path=path, query=params)
        return Bots(result)

    async def stats(self, bot_id: int, guild_count: int) -> Stats:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        봇 정보를 수신하거나 발신합니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.
        guild_count: Optional[int]
            서버 갯수가 포함되어 있습니다.
            값이 비어있을 경우 `.guild_count`를 통하여 불러옵니다.
        Returns
        -------
        Stats:
            KoreanBots로 부터 들어온 봇 상태 정보가 포함되어 있습니다.
        """
        data = {
            "servers": guild_count
        }
        path = "/bots/{bot_id}/stats".format(bot_id=bot_id)

        self.requests.version = 2
        result = await self.requests.post(path=path, json=data)
        return Stats(result)

    async def vote(self, bot_id: int, user_id: int) -> Vote:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        `user_id`에 들어있는 사용자가 봇에 하트를 누른 여부에 대하여 불러옵니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.
        user_id: int
            유저 ID 값이 포함되어 있습니다.

        Returns
        -------
        Vote:
            KoreanBots로 부터 들어온 사용자 투표 정보에 대한 정보가 포함되어 있습니다.
        """
        data = {
            "userID": str(user_id)
        }
        path = "/bots/{bot_id}/vote".format(bot_id=bot_id)

        self.requests.version = 2
        result = await self.requests.get(path=path, query=data)
        return Vote(result)

    def widget(self,
               widget_type: WidgetType,
               bot_id: int,
               style: WidgetStyle = None,
               scale: float = None,
               icon: bool = None
               ) -> Widget:
        """
        KoreanBots를 통하여 디스코드 봇의 위젯 값을 불러옵니다.

        Parameters
        ----------
        widget_type: WidgetType
            위젯 유형값이 포함됩니다.
        bot_id: int
            위젯에 사용되는 디스코드 봇 ID가 포함됩니다.
        style: WidgetStyle
            위젯에 디자인 값이 들어갑니다.
        scale: float
            위젯의 사이즈 값이 들어갑니다. (0.5 ~ 3.0 값 내로만 조정이 가능합니다.)
            기본 값은 1.0 입니다.
        icon: bool
            위젯에 디스코드 봇 아이콘 포함 유무를 선택할 수 있습니다.
            기본 값은 False 입니다.

        Returns
        -------
        Widget:
            KoreanBots의 위젯이 들어간 Assets 값이 리턴됩니다.
        """
        query = dict()
        if isinstance(widget_type, WidgetType):
            widget_t = widget_type.value
        else:
            widget_t = widget_type

        if isinstance(style, WidgetStyle):
            query['style'] = style.value
        elif isinstance(style, str):
            query['style'] = style

        if scale is not None:
            query['scale'] = scale
        if icon is not None:
            query['icon'] = icon

        path = "/widget/bots/{widget_type}/{bot_id}".format(widget_type=widget_t, bot_id=bot_id)
        return Widget(path=path, query=query, session=self.session)

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
            KoreanBots로 부터 들어온 사용자 정보가 포함되어 있습니다.
        """
        path = "/users/{user_id}".format(user_id=user_id)

        self.requests.version = 2
        result = await self.requests.get(path=path)
        return User(result)
