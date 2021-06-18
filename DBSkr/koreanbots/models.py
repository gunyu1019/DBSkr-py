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
    def __init__(self, data: dict):
        super().__init__(data)
        self.message: str = data.get("message")


class Vote(BaseKoreanBots):
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
