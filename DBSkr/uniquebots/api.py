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
import json
import time

log = logging.getLogger()


class GraphQL:
    def __init__(self, query: str, variables: dict = None):
        self.query = query
        self.variables = variables

    def get(self):
        _key_type = {int: "Int", str: "String", bool: "boolean"}
        if self.variables is not None:
            _key = [("${}: {}!".format(i, _key_type.get(type(self.variables.get(i))))) for i in self.variables.keys()]
            key = ", ".join(_key)

            return json.dumps({
                "query": "query(%s)" % key + self.query,
                "variables": self.variables
            }, indent=4)
        else:
            return json.dumps({
                "query": self.query
            }, indent=4)

    def set_variables(self, _variables: dict):
        self.variables = _variables


class Api:
    def __init__(self,
                 token: str = None,
                 session: aiohttp.ClientSession = None,
                 loop: asyncio.AbstractEventLoop = None,
                 refresh_session: int = 300):
        self.BASE = "https://uniquebots.kr/graphql"
        self.token = token
        self.loop = loop
        if session is not None:
            self.session = session
        else:
            self.session = aiohttp.ClientSession(loop=self.loop)

        self._session_start = time.time()
        self.refresh_session_period = refresh_session

    async def close(self):
        await self.session.close()

    async def refresh_session(self):
        await self.session.close()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self._session_start = time.time()

    async def get_session(self):
        if not self.session:
            await self.refresh_session()
        elif 0 <= self.refresh_session_period <= time.time() - self._session_start:
            await self.refresh_session()
        return self.session

    async def requests(self, data: GraphQL, **kwargs):
        headers = {
            'Content-Type': 'application/json'
        }

        if self.token is not None:
            headers['Authorization'] = 'Bot ' + self.token

        if 'headers' in kwargs:
            kwargs['headers'].update(headers)
        else:
            kwargs['headers'] = headers

        session = await self.get_session()
        async with session.request("POST", self.BASE, data=data.get(), **kwargs) as response:
            if response.content_type == "application/json":
                data = await response.json()
            else:
                fp_data = await response.text()
                data = json.loads(fp_data)

            log.debug(f'POST {self.BASE} returned {response.status}')

            if response.status == 200:
                return data
