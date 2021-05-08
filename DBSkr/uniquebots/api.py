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
import json


class Api:
    def __init__(self, token: str, session: aiohttp.ClientSession = None):
        self.BASE = "https://uniquebots.kr/graphql"
        self.token = token
        if session is not None:
            self.sesion = session
        else:
            self.sesion = aiohttp.ClientSession()

    def close(self):
        self.sesion.close()

    @staticmethod
    def get_graphql(query: dict, variables: dict = None):
        if variables is not None:
            return json.dumps({
                "query": query,
                "variables": variables
            }, indent=4)
        else:
            return json.dumps({
                "query": query
            }, indent=4)

    async def requests(self, data: dict, **kwargs):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bot ' + self.token
        }
        if 'headers' in kwargs:
            kwargs['headers'].update(headers)
        else:
            kwargs['headers'] = headers

        async with self.sesion.request("POST", self.BASE, data=data, **kwargs) as result:
            if result.content_type == "application/json":
                data = await result.json()
            else:
                fp_data = await result.text()
                data = json.loads(fp_data)
