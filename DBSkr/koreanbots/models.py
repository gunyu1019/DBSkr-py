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
        data = data.get("data")
        self.id: str = data.get("id")
        self.discriminator: str = data.get("tag")
        self.avatar: DiscordAvatar = DiscordAvatar(user_id=self.id, avatar=data.get("avatar"))
        self.name: str = data.get("name")
        self.flags: BotFlagModel = BotFlagModel(data.get("flags", 0))
        self.library: str = data.get("lib")
        self.prefix: str = data.get("prefix")
        self.votes: int = data.get("votes")
        self.servers: int = data.get("servers")
        self.intro: str = data.get("intro")
        self.desc: str = data.get("desc")
        self.categories: list = [get_value(Category, x) for x in data.get("category")]
        self.status: Status = get_value(Status, data.get("status"))
        self.state: State = get_value(State, data.get("state"))

        self.owners: list = [User(i) if isinstance(i, dict) else i for i in data.get("owners")]

        # Optional Data
        self.website: Optional[str] = data.get("web")
        self.github: Optional[str] = data.get("git")
        self.invite: Optional[str] = data.get("url")
        self.support: Optional[str] = "https://discord.gg/" + data.get("discord")

        # For Premium (Optional Data)
        self.vanity: Optional[str] = data.get("vanity")
        self.background: Optional[ImageURL] = ImageURL(url=data.get("bg"))
        self.banner: Optional[ImageURL] = ImageURL(url=data.get("banner"))

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name + "#" + self.discriminator


class Stats(BaseKoreanBots):
    def __init__(self, data: dict):
        super().__init__(data)
        self.message: str = data.get("message")


class Vote(BaseKoreanBots):
    def __init__(self, data: dict):
        self.data = data
        super().__init__(data)

        data = data.get("data")
        last_vote = data.get("lastVote")
        self.voted: bool = data.get("voted", False)
        self.last_vote: datetime = datetime.fromtimestamp(last_vote)

    def __eq__(self, other):
        return self.voted == other

    def __ne__(self, other):
        return not self.__eq__(other)


class User(BaseKoreanBots):
    def __init__(self, data: dict):
        super().__init__(data)
        data = data.get("data")
        self.id: str = data.get("id")
        self.flags: UserFlagModel = UserFlagModel(data.get("flags", 0))
        self.github: Optional[str] = data.get("github")
        self.discriminator: str = data.get("tag")
        self.name: str = data.get("username")
        self.bots: list = [Bot(i) if isinstance(i, dict) else i for i in data.get("bots")]

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name + "#" + self.discriminator
