from datetime import datetime
from typing import Optional

from .enums import *
from .models import BaseKoreanBots


class Bot(BaseKoreanBots):
    def __init__(self, data: dict):
        super().__init__(data)
        data = data.get("data")
        self.id: str = data.get("id")
        self.tag: str = data.get("tag")
        self.avatar: str = data.get("avatar")
        self.name: str = data.get("name")
        self.flags: BotFlag = get_value(BotFlag, data.get("flags"), 0)
        self.library: str = data.get("lib")
        self.prefix: str = data.get("prefix")
        self.votes: int = data.get("votes")
        self.servers: int = data.get("servers")
        self.intro: str = data.get("intro")
        self.desc: str = data.get("desc")
        self.categories: list = [get_value(Category, x) for x in data.get("category")]
        self.status: Status = get_value(Status, data.get("status"))
        self.state: State = get_value(State, data.get("state"))

        # Optional Data
        self.website: Optional[str] = data.get("web")
        self.github: Optional[str] = data.get("git")
        self.custom_invite: Optional[str] = data.get("url")
        self.discord: Optional[str] = "https://discord.gg/" + data.get("discord")

        # For Premium (Optional Data)
        self.vanity: Optional[str] = data.get("vanity")
        self.background: Optional[str] = data.get("bg")
        self.banner: Optional[str] = data.get("banner")


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
