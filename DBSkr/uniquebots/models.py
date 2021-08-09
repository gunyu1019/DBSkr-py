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

from typing import Optional

from ..assets import DiscordAvatar


class BaseUniqueBots:
    def __init__(self, data: dict):
        self.data: dict = data


class Bot(BaseUniqueBots):
    """ UniqueBots의 디스코드 봇 정보를 담아내는 모델입니다.

    Attributes
    ------------
    id: str
        디스코드 봇의 ID 입니다.
    avatar: DiscordAvatar
        디스코드 봇의 프로필 사진 입니다.
    name: str
        디스코드 봇의 이름 입니다.
    library: str
        디스코드 봇에 사용된 라이브러리 정보 입니다.
    prefix: str
        디스코드 봇의 접두어 입니다.
    trusted: bool
        UniqueBots에서 해당 디스코드 봇을 신뢰할 수 있는 유/무를 반환합니다.
    verified: bool
        디스코드 봇이 인증되었다는 유/무를 반환합니다.
    servers: int
        디스코드 봇을 사용 중인 서버 갯수 입니다.
    intro: str
        디스코드 봇의 간단한 소개문 입니다.
    desc: str
        디스코드 봇의 설명문 입니다.
    status: Status
        디스코드 봇의 상태 입니다.
    premium: bool
        UniqueBots에서 프리미엄 해텍을 받고 있는 유/무를 반환힙니다.
    owners: List[Union[User, str]]
        디스코드 봇의 소유자입니다.
    votes: List[Union[User, str]]
        UniqueBots에 등재된 봇에 대해 하트를 사용자 목록 입니다.
    website: Optional[str]
        디스코드 봇의 웹사이트입니다.
    github: Optional[str]
        디스코드 봇의 깃허브입니다.
    invite: Optional[str]
        디스코드 봇의 초대링크입니다.
    support: Optional[str]
        디스코드 봇의 서포트 서버 초대링크입니다.
    slug: Optional[str]
        디스코드 봇의 slug 값 입니다.
    """
    def __init__(self, data: dict):
        super().__init__(data=data)

        from .enums import Status, get_value
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.trusted: bool = data.get("trusted")
        self.verified: bool = data.get("discordVerified")
        self.servers: int = data.get("guilds")
        self.status: Status = get_value(Status, data.get("status"))
        self.intro: str = data.get("brief")
        self.desc: str = data.get("description")
        self.prefix: str = data.get("prefix")
        self.library: str = data.get("library", {}).get("name")
        self.premium: bool = data.get("premium")

        self.owners = [User(i) if 'tag' in i else i.get("id") for i in data.get("owners")]
        self.votes = [User(i.get("from")) if "tag" in i.get("from") else i.get("from") for i in data.get("hearts", [])]

        # Optional Data
        self.invite: Optional[str] = data.get("invite")
        self.website: Optional[str] = data.get("website")
        self.support: Optional[str] = data.get("support")
        self.github: Optional[str] = data.get("git")
        self.slug: Optional[str] = data.get("slug")

        avatar = data.get("avatarURL")
        avatar = avatar.lstrip("https://cdn.discordapp.com/avatars/{}/".format(self.id))
        avatar = avatar.split(".")[0]
        self.avatar = DiscordAvatar(user_id=self.id, avatar=avatar)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name


class Stats(BaseUniqueBots):
    """ UniqueBots에 디스코드 봇 정보를 반영한 후 반환되는 값입니다.

    Attributes
    ------------
    guilds: int
        디스코드 봇의 서버 갯수 입니다.
    """
    def __init__(self, data: dict):
        super().__init__(data=data)
        self.guilds: int = data.get("guilds")

    def __eq__(self, other):
        return self.guilds == other if isinstance(other, str) else other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.__str__())

    def __int__(self):
        return self.guilds


class Category:
    def __init__(self, category_id: str, name: str):
        self.id = category_id
        self.name = name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class Vote(BaseUniqueBots):
    """ UniqueBots에 하트 정보에 대한 값입니다.

    Attributes
    ------------
    voted: bool
        하트 여부를 반환합니다.
    """
    def __init__(self, data: dict):
        super().__init__(data=data)

        self.voted: bool = data.get("heartClicked")

    def __eq__(self, other):
        return self.voted == other

    def __ne__(self, other):
        return not self.__eq__(other)


class User(BaseUniqueBots):
    """ UniqueBots에 등록된 사용자 정보에 대한 값입니다.

    Attributes
    ------------
    id: str
        사용자의 ID 입니다.
    desc: str
        사용자에 대한 설명입니다.
    name: str
        사용자의 이름 입니다. 태그와 함께 불러와 집니다.
    admin: bool
        사용자가 관리자가 인지 아닌지 확인합니다.
    bots: List[Union[Bot, dict]]
        사용자가 소유하고 있는 디스코드 봇입니다.
    avatar: DiscordAvatar
        사용자의 프로필 사진입니다.
    """
    def __init__(self, data: dict):
        super().__init__(data=data)

        self.id: str = data.get("id")
        self.name: str = data.get("tag")
        self.desc: str = data.get("description")
        self.admin: bool = data.get("admin", False)

        self.bots: list = [Bot(i) if 'name' in i else i.get('id') for i in data.get("bots", [])]

        avatar = data.get("avatarURL")
        avatar = avatar.lstrip("https://cdn.discordapp.com/avatars/{}/".format(self.id))
        avatar = avatar.split(".")[0]
        self.avatar = DiscordAvatar(user_id=self.id, avatar=avatar)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.name
