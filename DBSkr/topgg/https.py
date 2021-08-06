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
import asyncio
from typing import Union, Sequence, List

from .api import Api
from .models import Bot, Search, Stats, VotedUser, User, Vote
from .enums import WidgetType
from .widget import Widget


class HttpClient:
    """ Top.gg의 Http 클라이언트를 선언합니다.
     이 클래스를 통하여 top.gg API에 연결됩니다.

    Parameters
    ----------
    token: Optional[str]
        Top.gg 에서 발급받은 봇의 토큰 키값 입니다. 데이터를 반영하거나 불러올 때 토큰 값이 사용됩니다.
    session: Optional[aiohttp.ClientSession]
        HttpClient 를 위한 aiohttp 의 ClientSession 클래스 입니다.
        기본값은 None이며, 자동으로 ClientSession을 생성하게 됩니다.
    loop: Optional[asyncio.AbstractEventLoop]
        비동기를 사용하기 위한 asyncio.AbstractEventLoop 입니다.
        기본값은 None 입니다.
        기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.
    """
    def __init__(self, token: str = None,
                 session: aiohttp.ClientSession = None,
                 loop: asyncio.AbstractEventLoop = None):
        self.token = token
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
            Top.gg로 부터 들어온 봇 정보가 포함되어 있습니다.
        """
        path = "/bots/{bot_id}".format(bot_id=bot_id)

        result = await self.requests.get(path=path)
        return Bot(result)

    async def search(self,
                     sort: str = None,
                     search=None,
                     fields: Sequence[str] = "",
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
        if search is None:
            search = {}

        limit = min(limit, 500)
        fields = ", ".join(fields)
        search = " ".join([f"{field}: {value}" for field, value in search.items()])

        data = {
            "limit": limit,
            "offset": offset,
            "search": search,
            "fields": fields,
            "sort": sort
        }
        path = "/search"

        result = await self.requests.get(path=path, query=data)
        return Search(result)

    async def vote(self, bot_id: int, user_id: int) -> Vote:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        `user_id`에 들어있는 사용자가 봇에 투표를 누른 여부에 대하여 불러옵니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.
        user_id: int
            유저 ID 값이 포함되어 있습니다.

        Returns
        -------
        Vote:
            Top.gg로 부터 들어온 사용자 투표 정보에 대한 정보가 포함되어 있습니다.
        """
        data = {
            "userId": str(user_id)
        }
        path = "/bots/{bot_id}/check".format(bot_id=bot_id)
        result = await self.requests.get(path=path, query=data)
        return Vote(result)

    async def votes(self, bot_id: int) -> List[VotedUser]:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        투표를 누른 사용자 목록을 모두 불러옵니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.

        Returns
        -------
        List[User]:
            Top.gg로 부터 투표 누른 사용자 목록에 대한 정보가 포함되어 있습니다.
        """
        path = "/bots/{bot_id}/votes".format(bot_id=bot_id)
        result = await self.requests.get(path=path)
        return [VotedUser(user) for user in result]

    async def stats(self, bot_id: int,
                    guild_count: Union[int, list] = None,
                    shard_id: int = None,
                    shard_count: int = None) -> Stats:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        봇 정보를 수신하거나 발신합니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.
        guild_count: Optional[Union[int, list]]
            서버 갯수가 포함되어 있습니다.
        shard_id: Optional[int]
            (Shard를 사용할 때만 해당됩니다.) 샤드의 ID 값이 포함됩니다.
        shard_count: Optional[int]
            (Shard를 사용할 때만 해당됩니다.) 샤드의 갯수가 포함됩니다.

        Returns
        -------
        Stats:
            Top.gg로 부터 들어온 봇 상태 정보가 포함되어 있습니다.
        """
        path = "/bots/{bot_id}/stats".format(bot_id=bot_id)

        if guild_count is not None:
            data = {
                "server_count": guild_count,
                "shard_id": shard_id,
                "shard_count": shard_count
            }
            result = await self.requests.post(path=path, json=data)
        else:
            result = await self.requests.get(path=path)
        return Stats(result)

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
        path = "/users/{user_id}".format(user_id=user_id)

        self.requests.version = 2
        result = await self.requests.get(path=path)
        return User(result)

    def widget(self, bot_id: int, widget_type: WidgetType = None) -> Widget:
        """
        Top.gg를 통하여 디스코드 봇의 위젯 값을 불러옵니다.

        Parameters
        ----------
        widget_type: WidgetType
            위젯 유형값이 포함됩니다.
        bot_id: int
            위젯에 사용되는 디스코드 봇 ID가 포함됩니다.

        Returns
        -------
        Widget:
            Top.gg의 위젯이 들어간 Assets 값이 리턴됩니다.
        """
        query = dict()
        if isinstance(widget_type, WidgetType):
            widget_t = widget_type.value
        else:
            widget_t = widget_type

        if widget_type is None:
            path = "/widget/{widget_type}/{bot_id}".format(widget_type=widget_t, bot_id=bot_id)
        else:
            path = "/widget/{bot_id}".format(widget_type=widget_t, bot_id=bot_id)
        return Widget(path=path, query=query, session=self.session)
