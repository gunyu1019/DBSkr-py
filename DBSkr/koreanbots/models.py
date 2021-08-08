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

from datetime import datetime
from typing import Optional

from .enums import *
from .flags import BotFlagModel, UserFlagModel
from ..assets import DiscordAvatar, ImageURL


class BaseKoreanBots:
    def __init__(self, data: dict):
        self.data: dict = data

        self.code: int = self.data.get("code")
        self.version: int = self.data.get("version")


class Bot(BaseKoreanBots):
    """ KoreanBots의 디스코드 봇 정보를 담아내는 모델입니다.

    Attributes
    ------------
    id: str
        디스코드 봇의 ID 입니다.
    discriminator: str
        디스코드 봇의 태그 입니다.
    avatar: DiscordAvatar
        디스코드 봇의 프로필 사진 입니다.
    name: str
        디스코드 봇의 이름 입니다.
    flags: BotFlagModel
        KoreanBots에 등재된 봇의 Flag 값 입니다.
    library: str
        디스코드 봇에 사용된 라이브러리 정보 입니다.
    prefix: str
        디스코드 봇의 접두어 입니다.
    prefix: str
        디스코드 봇의 접두어 입니다.
    votes: int
        KoreanBots에 등재된 봇에 대해 하트를 누른 갯수 입니다.
    servers: int
        디스코드 봇을 사용 중인 서버 갯수 입니다.
    intro: str
        디스코드 봇의 간단한 소개문 입니다.
    desc: str
        디스코드 봇의 설명문 입니다.
    categories: List[Category]
        디스코드 봇의 카테고리 입니다.
    status: Status
        디스코드 봇의 상태 입니다.
    state: State
        KoreanBots에 등재된 봇의 상태 입니다.
    owners: List[Union[User, str]]
        디스코드 봇의 소유자입니다.
    website: Optional[str]
        디스코드 봇의 웹사이트입니다.
    github: Optional[str]
        디스코드 봇의 깃허브입니다.
    invite: Optional[str]
        디스코드 봇의 초대링크입니다.
    support: Optional[str]
        디스코드 봇의 서포트 서버 초대링크입니다.
    vanity: Optional[str]
        디스코드 봇의 VANITY 주소 입니다.
    background: Optional[ImageURL]
        디스코드 봇의 백그라운드 사진입니다.
    banner: Optional[ImageURL]
        디스코드 봇의 배너입니다.
    """
    def __init__(self, data: dict):
        super().__init__(data)

        _data = data.get("data")
        self.id: str = _data.get("id")
        self.discriminator: str = _data.get("tag")
        self.avatar: DiscordAvatar = DiscordAvatar(user_id=self.id, avatar=_data.get("avatar"))
        self.name: str = _data.get("name")
        self.flags: BotFlagModel = BotFlagModel(_data.get("flags", 0))
        self.library: str = _data.get("lib")
        self.prefix: str = _data.get("prefix")
        self.votes: int = _data.get("votes")
        self.servers: int = _data.get("servers")
        self.intro: str = _data.get("intro")
        self.desc: str = _data.get("desc")
        self.categories: list = [get_value(Category, x) for x in _data.get("category")]
        self.status: Status = get_value(Status, _data.get("status"))
        self.state: State = get_value(State, data.get("state"))

        self.owners: list = [User(i) if isinstance(i, dict) else i for i in _data.get("owners", [])]

        # Optional Data
        self.website: Optional[str] = _data.get("web")
        self.github: Optional[str] = _data.get("git")
        self.invite: Optional[str] = _data.get("url")
        self.support: Optional[str] = "https://discord.gg/" + _data.get("discord")

        # For Premium (Optional Data)
        self.vanity: Optional[str] = _data.get("vanity")
        self.background: Optional[ImageURL] = ImageURL(url=_data.get("bg")) if _data.get("bg") is not None else None
        self.banner: Optional[ImageURL] = ImageURL(url=_data.get("banner")) if _data.get("bg") is not None else None

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name + "#" + self.discriminator


class Bots(BaseKoreanBots):
    """ KoreanBots의 검색된 정보값이 포함되어 있습니다.

    Attributes
    ------------
    type: str
        검색 유형입니다.
    current: int
        현재 페이지를 나타냅니다.
    total: int
        검색된 모든 페이지를 나타냅니다.
    results: List[Bot]
        검색된 결과가 들어있습니다.
    """
    def __init__(self, data: dict):
        super().__init__(data)
        self.type: str = data.get("data", {}).get("type")
        self.current: int = data.get("currentPage")
        self.total: int = data.get("totalPage")

        _data = []
        for i in data.get("data"):
            _data.append(Bot(i))

        self.results: list = _data

    def __len__(self):
        return len(self.results)


class Stats(BaseKoreanBots):
    """ KoreanBots에 디스코드 봇 정보를 반영한 후 반환되는 값입니다.

    Attributes
    ------------
    message: str
        KoreanBots에서 회신한 메세지입니다.
    """
    def __init__(self, data: dict):
        super().__init__(data)
        self.message: str = data.get("message")


class Vote(BaseKoreanBots):
    """ KoreanBots에 하트 정보에 대한 값입니다.

    Attributes
    ------------
    voted: bool
        하트 여부를 반환합니다.
    last_vote: datetime
        마지막으로 하트를 준 시간을 반환합니다.
    """
    def __init__(self, data: dict):
        super().__init__(data)

        _data = data.get("data")
        last_vote = _data.get("lastVote")
        self.voted: bool = _data.get("voted", False)
        self.last_vote: datetime = datetime.fromtimestamp(last_vote)

    def __eq__(self, other):
        return self.voted == other

    def __ne__(self, other):
        return not self.__eq__(other)


class User(BaseKoreanBots):
    """ KoreanBots에 등록된 사용자 정보에 대한 값입니다.

    Attributes
    ------------
    id: str
        사용자의 ID 입니다.
    discriminator: str
        사용자의 태그 입니다.
    name: str
        사용자의 이름 입니다.
    github: Optional[str]
        사용자의 깃허브 입니다.
    bots: List[Union[Bot, dict]]
        사용자가 소유하고 있는 디스코드 봇입니다.
    flags: UserFlagModel
        KoreanBots에 등록된 사용자의 Flag 값 입니다.
    """
    def __init__(self, data: dict):
        super().__init__(data)

        _data = data.get("data", data)
        self.id: str = _data.get("id")
        self.flags: UserFlagModel = UserFlagModel(_data.get("flags", 0))
        self.github: Optional[str] = _data.get("github")
        self.discriminator: str = _data.get("tag")
        self.name: str = _data.get("username")
        self.bots: list = [Bot(i) if isinstance(i, dict) else i for i in _data.get("bots", [])]

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name + "#" + self.discriminator
