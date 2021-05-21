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


class Bots:
    def __init__(self, data):
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
        self.guilds: list = data.get("guilds")
        self.date: datetime = datetime.fromisoformat(data.get("date", "1970-01-01T00:00:00").strip("Z"))
        self.certified: bool = data.get("certifiedBot")
        self.vanity: Optional[str] = data.get("vanity")
        self.points: int = data.get("points")
        self.month_points: int = data.get("monthlyPoints")
        self.donate: str = data.get("donatebotguildid")

        self.shard_count: Optional[int] = data.get("shard_count")
        self.guild_count: Optional[int] = data.get("server_count")

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


class Vote:
    def __int__(self, data):
        self.voted: bool = data.get("voted")

    def __eq__(self, other):
        return self.voted == other

    def __ne__(self, other):
        return not self.__eq__(other)


class Search:
    def __init__(self, data):
        self.results = [Bots(i) for i in data.get("results")]
        self.limit = data.get("limit")
        self.offset = data.get("offset")
        self.count = data.get("count")
        self.total = data.get("total")

    def __len__(self):
        return len(self.results)


class Users:
    def __init__(self, data):
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


class VotedUser:
    def __init__(self, data):
        self.name = data.get("username")
        self.id = data.get("id")

        avatar = data.get("avatar")
        avatar = avatar.lstrip("https://cdn.discordapp.com/avatars/{}/".format(self.id))
        avatar = avatar.split(".")[0]
        self.avatar = DiscordAvatar(user_id=self.id, avatar=avatar)
