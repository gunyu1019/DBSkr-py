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

import logging
import aiohttp
import asyncio
import json
import time

from .errors import *

log = logging.getLogger(__name__)


class Api:
    def __init__(self,
                 token: str,
                 session: aiohttp.ClientSession = None,
                 loop: asyncio.AbstractEventLoop = None,
                 refresh_session: int = 300):
        self.BASE = "https://top.gg/api"
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

    async def requests(self, method: str, path: str, **kwargs):
        url = "{}{}".format(self.BASE, path)
        headers = {
            'Content-Type': 'application/json'
        }
        if self.token is not None:
            headers['Authorization'] = self.token

        if 'headers' in kwargs:
            kwargs['headers'].update(headers)
        else:
            kwargs['headers'] = headers

        for tries in range(5):
            session = await self.get_session()
            async with session.request(method, url, **kwargs) as response:
                if response.content_type == "application/json":
                    data = await response.json()
                else:
                    fp_data = await response.text()
                    data = json.loads(fp_data)
                log.debug(f'{method} {url} returned {response.status}')

                if response.status == 429:
                    retry_after = float(response.headers.get('retry-after'))

                    log.warning(f"Rate limited. Retry in {retry_after} seconds | Tries: {tries}")
                    await asyncio.sleep(retry_after)
                    continue

                if 200 <= response.status < 300:
                    return data
                elif response.status == 400:
                    raise BadRequests(response, data)
                elif response.status == 401:
                    raise Unauthorized(response, data)
                elif response.status == 403:
                    raise Forbidden(response, data)
                elif response.status == 404:
                    raise NotFound(response, data)
                else:
                    raise HTTPException(response, data)
        raise TooManyRequests(response, data)

    async def get(self, path: str, **kwargs):
        return await self.requests("GET", path, **kwargs)

    async def post(self, path: str, **kwargs):
        return await self.requests("POST", path, **kwargs)
