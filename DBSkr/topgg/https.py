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
from typing import Union, Dict, Sequence

from .api import Api
from .models import Bot, Search, Stats, VotedUser, User, Vote
from .enums import WidgetType
from .widget import Widget


class HttpClient:
    def __init__(self, token: str, session: aiohttp.ClientSession = None):
        self.token = token
        self.requests = Api(token=token, session=session)
        self.session = session

    async def bot(self, bot_id: int) -> Bot:
        path = "/bots/{bot_id}".format(bot_id=bot_id)

        result = await self.requests.get(path=path)
        return Bot(result)

    async def search(self,
                     sort: str = None,
                     search=None,
                     fields: Sequence[str] = "",
                     limit: int = 50,
                     offset: int = 0) -> Search:

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
        data = {
            "userId": str(user_id)
        }
        path = "/bots/{bot_id}/check".format(bot_id=bot_id)
        result = await self.requests.get(path=path, query=data)
        return Vote(result)

    async def votes(self, bot_id: int) -> VotedUser:
        path = "/bots/{bot_id}/votes".format(bot_id=bot_id)
        result = await self.requests.get(path=path)
        return VotedUser(result)

    async def stats(self, bot_id: int,
                    guild_count: Union[int, list] = None,
                    shard_id: int = None,
                    shard_count: int = None) -> Stats:
        path = "/bots/{bot_id}/stats".format(bot_id=bot_id)

        if guild_count is not None:
            data = {
                "server_count": guild_count,
                "shard_id": shard_id,
                "shard_count": shard_count
            }
            result = await self.requests.post(path=path, data=data)
        else:
            result = await self.requests.get(path=path)
        return Stats(result)

    async def users(self, user_id: int) -> User:
        path = "/users/{user_id}".format(user_id=user_id)

        self.requests.version = 2
        result = await self.requests.get(path=path)
        return User(result)

    def widget(self, bot_id: int, widget_type: WidgetType = None) -> Widget:
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
