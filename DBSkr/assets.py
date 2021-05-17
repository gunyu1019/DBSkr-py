import io
import os

from typing import Union
from aiohttp import ClientSession


class Assets:
    def __init__(self, cls, support_format: list, session: ClientSession = None):
        self._class = cls
        self._support_format: list = support_format
        if session is None:
            session = ClientSession()
        self.session = session

    async def read(self):
        query = self._class.query
        async with self.session.get(self.url(), query=query) as resp:
            if resp.status == 200:
                return await resp.read()

    async def save(self, fp: Union[str, bytes, os.PathLike, io.BufferedIOBase], seek_begin: bool = True):
        data = await self.read()
        if isinstance(fp, io.BufferedIOBase):
            written = fp.write(data)
            if seek_begin:
                fp.seek(0)
            return written
        else:
            with open(fp, 'wb') as f:
                return f.write(data)

    def url(self, format: str = None):
        if format is None:
            format = self._support_format[0]

        if hasattr(self._class, "query"):
            query = self._class.query
            _query = str()

            for i in query.keys():
                _query += i + "=" + query[i]
            if len(query) != 0:
                url = "{}{}.{}?{}".format(self._class.BASE, self._class.path, format, _query)
            else:
                url = "{}{}.{}".format(self._class.BASE, self._class.path, format)
        else:
            url = "{}{}.{}".format(self._class.BASE, self._class.path, format)

        return url
