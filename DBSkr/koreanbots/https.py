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

from .api import Api
from .models import *
from .enums import WidgetType


class HttpClient:
    def __init__(self, token: str, session: aiohttp.ClientSession = None):
        self.token = token
        self.requests = Api(token=token, session=session)

    async def bots(self, bot_id: int):
        path = "/v2/bots/{bot_id}".format(bot_id=bot_id)

        self.requests.version = 2
        result = await self.requests.post(path=path)
        return

    async def stats(self, bot_id: int, guild_count: int):
        data = {
            "servers": guild_count
        }
        path = "/v2/bots/{bot_id}/stats".format(bot_id=bot_id)

        self.requests.version = 2
        result = await self.requests.post(path=path, data=data)
        return Stats(result)

    async def vote(self, bot_id: int, user_id: int):
        data = {
            "userID": str(user_id)
        }
        path = "/v2/bots/{bot_id}/vote".format(bot_id=bot_id)

        self.requests.version = 2
        result = await self.requests.post(path=path, data=data)
        return Vote(result)

    async def widget(self, widget_type: WidgetType, bot_id: int):
        if isinstance(widget_type, WidgetType):
            widget_t = widget_type.value
        else:
            widget_t = widget_type

        path = "/widget/bots/{widget_type}/{bot_id}".format(widget_type=widget_t, bot_id=bot_id)

        self.requests.version = 2
        result = await self.requests.post(path=path)
        return

    async def users(self, user_id: int):
        path = "/v2/users/{user_id}".format(user_id=user_id)

        self.requests.version = 2
        result = await self.requests.post(path=path)
        return
