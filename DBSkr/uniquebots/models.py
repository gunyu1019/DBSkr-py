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
from .enums import Status, get_value


class Bot:
    def __init__(self, data):
        data = data.get("data")
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.trusted: bool = data.get("trusted")
        self.verified: bool = data.get("discordVerified")
        self.guild_count: int = data.get("guilds")
        self.status: Status = get_value(Status, data.get("status"))
        self.intro: str = data.get("brief")
        self.desc: str = data.get("description")
        self.prefix: str = data.get("prefix")
        self.library: str = data.get("library", {}).get("name")
        self.premium: bool = data.get("premium")

        self.owners = [User(i) for i in data.get("owners")]

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


class Category:
    def __init__(self, category_id: str, name: str):
        self.id = category_id
        self.name = name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


class User:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.name = data.get("tag")

        self.bots = [Bot(i) for i in data.get("bots")]

        avatar = data.get("avatarURL")
        avatar = avatar.lstrip("https://cdn.discordapp.com/avatars/{}/".format(self.id))
        avatar = avatar.split(".")[0]
        self.avatar = DiscordAvatar(user_id=self.id, avatar=avatar)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.name
