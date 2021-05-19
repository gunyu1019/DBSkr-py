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

from .errors import *

from datetime import datetime

log = logging.getLogger(__name__)


class Api:
    def __init__(self, token: str, session: aiohttp.ClientSession = None):
        self.BASE = "https://top.gg/api"
        self.token = token
        if session is not None:
            self.sesion = session
        else:
            self.sesion = aiohttp.ClientSession()

    def close(self):
        self.sesion.close()

    async def requests(self, method: str, path: str, **kwargs):
        url = "{}{}".format(self.BASE, path)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.token
        }
        if 'headers' in kwargs:
            kwargs['headers'].update(headers)
        else:
            kwargs['headers'] = headers

        for tries in range(5):
            async with self.sesion.request(method, url, **kwargs) as response:
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
