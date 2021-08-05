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

import io
import os

from typing import Union

from aiohttp import ClientSession
from urllib import parse

from . import errors


class Assets:
    """ KoreanBots 클라이언트, top.gg 클라이언트, UniqueBots 클라이언트로 부터 들어온 이미지 자료를 나타냅니다."""
    def __init__(self, cls, support_format: list, session: ClientSession = None):
        self._class = cls
        self._support_format: list = support_format
        if session is None:
            session = ClientSession()
        self.session = session

    def __str__(self):
        return self.url()

    def __eq__(self, other):
        return self.url() == other.url()

    def __ne__(self, other):
        return not self.__eq__(other)

    async def read(self) -> bytes:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        이 에셋의 콘텐츠값을 바이트로 불러옵니다.

        Returns
        -------
        :class:`bytes`:
            에셋의 콘텐츠가 리턴됩니다.
        """
        query = self._class.query
        async with self.session.get(self.url(), query=query) as resp:
            if resp.status == 200:
                return await resp.read()
            elif resp.status == 404:
                raise errors.NotFound("에셋을 찾을 수 없습니다.")
            else:
                raise errors.HTTPException("에셋을 찾는데 실패하였습니다.")

    async def save(self, fp: Union[str, bytes, os.PathLike, io.BufferedIOBase], seek_begin: bool = True):
        """
        본 함수는 코루틴(비동기)함수 입니다.

        이 에셋을 파일로 저장합니다.

        Parameters
        ----------
        fp: Union[str, bytes, os.PathLike, io.BufferedIOBase]
            이 첨부 파일을 저장할 파일 형식 또는 사용할 파일 이름입니다.
            파일 이름이 전달되면 해당 파일 이름으로 파일이 작성되고 저장합니다.
        seek_begin: Optional[bool]
            파일을 저장한 후, 첫번째 파일로 불러옵니다.

        Returns
        -------
        int:
            작성된 크기가 리턴됩니다.
        """
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
        """
        이 에셋의 CDN 링크를 불러옵니다.

        Parameters
        ----------
        format: Optional[str]
            불러올 링크의 포맷을 설정합니다.

        Returns
        -------
        str:
            이 에셋의 CDN 서버의 링크를 반환합니다.
        """
        if format is None:
            format = self._support_format[0]
        elif format not in self._support_format and format is not None:
            raise errors.InvalidArgument(f"format must be one of {self._support_format}")

        if hasattr(self._class, "query"):
            query = self._class.query
            _query = str()

            if isinstance(query, dict):
                for i in query.keys():
                    _query += i + "=" + query[i] + "&"
                _query = _query.lstrip("&")
            else:
                _query = query

            if len(query) != 0:
                url = "{}{}.{}?{}".format(self._class.BASE, self._class.path, format, _query)
            else:
                url = "{}{}.{}".format(self._class.BASE, self._class.path, format)
        else:
            url = "{}{}.{}".format(self._class.BASE, self._class.path, format)

        return url


class DiscordAvatar(Assets):
    """ 디스코드 사용자 혹은 봇의 아이콘을 저장합니다."""
    def __init__(self, user_id: Union[int, str], avatar: str, session: ClientSession = None, size: int = None):
        self.path = "/avatars/{}/{}".format(user_id, avatar)
        if size is not None:
            self.query = {
                "size": size
            }

        self.BASE = "https://cdn.discordapp.com"
        super().__init__(self, support_format=['png', 'jpg', 'webp'], session=session)


class ImageURL(Assets):
    """ KoreanBots 클라이언트, top.gg 클라이언트, UniqueBots 클라이언트로 부터 들어온 이미지 자료를 저장합니다.
    주로 저장되는 데이터는 백그라운드 사진, 배너 사진 등이 있습니다.
    """
    def __init__(self, url: str, session: ClientSession = None):
        http = parse.urlparse(url)
        self.path = http.path

        _slice = self.path.split(".")
        _link = _slice[0:-1]
        _format = _slice[-1]
        self.path = ".".join(_link)
        self.BASE = http.scheme + "://" + http.netloc
        self.query = http.query
        super().__init__(self, support_format=[_format], session=session)
