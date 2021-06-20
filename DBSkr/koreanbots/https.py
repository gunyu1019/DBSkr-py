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
    def __init__(self,
                 token: str = None,
                 session: aiohttp.ClientSession = None,
                 loop: asyncio.AbstractEventLoop = None):
        self.token = token
        self.loop = loop
        self.requests = Api(token=token, session=session, loop=loop)
        self.session = session

    async def bot(self, bot_id: int) -> Bot:
        path = "/bots/{bot_id}".format(bot_id=bot_id)

        self.requests.version = 2
        result = await self.requests.get(path=path)
        return Bot(result)

    async def search(self, query: str, page: int = 1) -> Bots:
        params = {
            "query": query,
            "page": page
        }
        path = "/v2/search/bots"

        self.requests.version = 2
        result = await self.requests.get(path=path, query=params)
        return Bots(result)

    async def new(self) -> Bots:
        path = "/v2/list/bots/new"

        self.requests.version = 2
        result = await self.requests.get(path=path)
        return Bots(result)

    async def votes(self, page: int = 1) -> Bots:
        params = {
            "page": page
        }
        path = "/v2/list/bots/new"

        self.requests.version = 2
        result = await self.requests.get(path=path, query=params)
        return Bots(result)

    async def stats(self, bot_id: int, guild_count: int) -> Stats:
        data = {
            "servers": guild_count
        }
        path = "/bots/{bot_id}/stats".format(bot_id=bot_id)

        self.requests.version = 2
        result = await self.requests.post(path=path, json=data)
        return Stats(result)

    async def vote(self, bot_id: int, user_id: int) -> Vote:
        data = {
            "userID": str(user_id)
        }
        path = "/bots/{bot_id}/vote".format(bot_id=bot_id)

        self.requests.version = 2
        result = await self.requests.get(path=path, query=data)
        return Vote(result)

    def widget(self, widget_type: WidgetType, bot_id: int,
                     style: WidgetStyle = None, scale: float = None, icon: bool = None) -> Widget:
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
        path = "/users/{user_id}".format(user_id=user_id)

        self.requests.version = 2
        result = await self.requests.get(path=path)
        return User(result)
