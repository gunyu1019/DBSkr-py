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
from datetime import datetime

from ..assets import DiscordAvatar


class BaseTopgg:
    def __init__(self, data: dict):
        self.data: dict = data


class Bot(BaseTopgg):
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
    library: str
        디스코드 봇에 사용된 라이브러리 정보 입니다.
    prefix: str
        디스코드 봇의 접두어 입니다.
    votes: int
        Top.gg에 등재된 봇에 대해 투표를 누른 갯수 입니다.
    servers: int
        디스코드 봇을 사용 중인 서버 갯수 입니다.
    shard_count: int
        디스코드 봇 샤드 갯수 입니다.
    month_votes: int
        Top.gg에 등재된 봇에 대해 투표를 누른 갯수 입니다. (한달 마다 갱신됩니다.)
    representative_guilds: str
        디스코드 봇이 대표하는 서버입니다.
    intro: str
        디스코드 봇의 간단한 소개문 입니다.
    desc: str
        디스코드 봇의 설명문 입니다.
    date: str
        Top.gg에 디스코드 봇이 등재된 날짜 입니다.
    categories: List[Category]
        디스코드 봇의 카테고리 입니다.
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
    donate: str
        디스코드 봇의 후원 ID입니다.
    avatar_hash: Optional[str]
        디스코드 봇의 아바타 해시값 입니다.
    verified: bool
        디스코드 봇이 인증되었다는 유/무를 반환합니다.
    """
    def __init__(self, data):
        super().__init__(data)
        self.id: str = data.get("id", data.get("clientid"))
        self.name: str = data.get("username")
        self.discriminator: str = data.get("discriminator")
        self.avatar: DiscordAvatar = DiscordAvatar(user_id=self.id, avatar=data.get("defAvatar"))
        self.library: str = data.get("lib")
        self.prefix: str = data.get("prefix")
        self.intro: str = data.get("shortdesc")
        self.desc: str = data.get("longdesc")
        self.categories: list = data.get("tag")
        self.owners: list = data.get("owners")
        self.representative_guilds: list = data.get("guilds")
        self.date: datetime = datetime.fromisoformat(data.get("date", "1970-01-01T00:00:00").strip("Z"))
        self.verified: bool = data.get("certifiedBot")
        self.vanity: Optional[str] = data.get("vanity")
        self.votes: int = data.get("points")
        self.month_votes: int = data.get("monthlyPoints")
        self.donate: str = data.get("donatebotguildid")

        self.shard_count: Optional[int] = data.get("shard_count")
        self.servers: Optional[int] = data.get("server_count")

        # Optional
        self.avatar_hash: Optional[str] = data.get("avatar")
        self.website: Optional[str] = data.get("website")
        self.support: Optional[str] = "https://discord.gg/" + data.get("support")
        self.github: Optional[str] = data.get("github")
        self.invite: Optional[str] = data.get("invite")

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name + "#" + self.discriminator


class Stats(BaseTopgg):
    """ Top.gg에 디스코드 봇 정보를 반영한 후 반환되는 값입니다.

    Attributes
    ------------
    servers: int
        디스코드 봇을 사용 중인 서버 갯수 입니다.
    shards: list
        디스코드 봇의 샤드 ID 값입니다.
    shard_count: int
        디스코드 봇 샤드 갯수 입니다.
    """
    def __init__(self, data):
        super().__init__(data)
        self.servers: Optional[int] = data.get("server_count")
        self.shards: Optional[list] = data.get("shards")
        self.shard_count: Optional[int] = data.get("shard_count")


class Vote(BaseTopgg):
    """ Top.gg에 하트 정보에 대한 값입니다.

    Attributes
    ------------
    voted: bool
        하트 여부를 반환합니다.
    """
    def __init__(self, data):
        super().__init__(data)
        self.voted: bool = data.get("voted")

    def __eq__(self, other):
        return self.voted == other

    def __ne__(self, other):
        return not self.__eq__(other)


class Search(BaseTopgg):
    """ Top.gg에 검색 정보에 대한 값입니다.

    Attributes
    ------------
    results: List[Bot]
        검색된 디스코드 봇의 이름이 포함됩니다.
    count: int
        한 페이지에 검색된 디스코드 봇들의 갯수 입니다.
    total: int
        검색된 총 페이지 입니다.
    limit: int
        불러올 봇의 양의 갯수가 포함됩니다.
    offset: int
        건너 뛸 디스코드 봇의 갯수가 포함됩니다.
    """
    def __init__(self, data):
        super().__init__(data)
        self.results: list = [Bot(i) for i in data.get("results")]
        self.limit: int = data.get("limit")
        self.offset: int = data.get("offset")
        self.count: int = data.get("count")
        self.total: int = data.get("total")

    def __len__(self):
        return len(self.results)


class User(BaseTopgg):
    """ Top.gg에 등록된 사용자 정보에 대한 값입니다.

    Attributes
    ------------
    id: str
        사용자의 ID 입니다.
    discriminator: str
        사용자의 태그 입니다.
    name: str
        사용자의 이름 입니다.
    avatar: DiscordAvatar
        디스코드 봇의 프로필 사진 입니다.
    github: Optional[str]
        사용자의 깃허브 입니다.
    youtube: Optional[str]
        사용자의 유튜브 입니다.
    reddit: Optional[str]
        사용자의 레딧 입니다.
    twitter: Optional[str]
        사용자의 트위터 입니다.
    instagram: Optional[str]
        사용자의 인스타그램 주소 입니다.
    bio: Optional[str]
        사용자의 bio 정보입니다.
    banner: Optional[str]
        사용자의 배너 주소입니다.
    avatar_hash: Optional[str]
        사용자의 아바타 해시값 입니다.
    color: Optional[str]
        사용자의 고유 색상값 입니다.
    staff: bool
        사용자가 스태프인지 확인합니다.
    web_mod: bool
        사용자가 웹 모더레이터인지 확인합니다.
    mod: bool
        사용자가 모더레이터인지 확인합니다.
    certified: bool
        인증된 사용자인지 확인합니다.
    supporter: bool
        사용자가 서포터인지 확인합니다.
    """
    def __init__(self, data):
        super().__init__(data)
        self.id: str = data.get("id")
        self.name: str = data.get("username")
        self.discriminator: str = data.get("discriminator")
        self.avatar: DiscordAvatar = DiscordAvatar(user_id=self.id, avatar=data.get("defAvatar"))

        # Optional
        self.bio: Optional[str] = data.get("bio")
        self.banner: Optional[str] = data.get("banner")
        self.avatar_hash: Optional[str] = data.get("avatar")
        self.color: Optional[str] = data.get("color")

        # Boolean Data
        self.staff: bool = data.get("admin")
        self.web_mod: bool = data.get("webMod")
        self.mod: bool = data.get("mod")
        self.certified: bool = data.get("certifiedDev")
        self.supporter: bool = data.get("supporter")

        # Social Data
        social = data.get("social", dict())
        self.youtube: Optional[str] = social.get("youtube")
        self.reddit: Optional[str] = social.get("reddit")
        self.twitter: Optional[str] = social.get("twitter")
        self.instagram: Optional[str] = social.get("instagram")
        self.github: Optional[str] = social.get("github")


class VotedUser(BaseTopgg):
    """ 투표한 사용자에 대한 값입니다.

    Attributes
    ------------
    id: str
        사용자의 ID 입니다.
    name: str
        사용자의 이름 입니다.
    avatar: DiscordAvatar
        디스코드 봇의 프로필 사진 입니다.
    """
    def __init__(self, data):
        super().__init__(data)
        self.name: str = data.get("username")
        self.id: str = data.get("id")

        avatar = data.get("avatar")
        avatar = avatar.lstrip("https://cdn.discordapp.com/avatars/{}/".format(self.id))
        avatar = avatar.split(".")[0]
        self.avatar = DiscordAvatar(user_id=self.id, avatar=avatar)
