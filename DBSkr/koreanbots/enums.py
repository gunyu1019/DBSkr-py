from enum import Enum
from ..enums import get_value


class WidgetType(Enum):
    Vote = "votes"
    Server = "servers"
    Status = "status"


class Category(Enum):
    manage = "관리"
    music = "뮤직"
    stats = "전적"
    game = "게임"
    gambling = "도박"
    logging = "로깅"
    slash = "빗금 명령어"
    dashboard = "웹 대시보드"
    meme = "밈"
    leveling = "레벨링"
    utilities = "유틸리티"
    chat = "대화"
    NSFW = "NSFW"
    search = "검색"
    school = "학교"
    corona = "코로나-19"
    translation = "번역"
    overwatch = "오버워치"
    LOL = "리그 오브 레전드"
    PUBG = "배틀그라운드"
    Minecraft = "마인크래프트"

    def __str__(self):
        return self.name


class Status(Enum):
    online = "online"
    idle = "idle"
    dnd = "dnd"
    streaming = "streaming"
    offline = "offline"


class State(Enum):
    ok = "ok"
    reported = "reported"
    blocked = "blocked"
    private = "private"
    archived = "archived"


class BotFlag(Enum):
    official = 1 << 1
    verification_bot = 1 << 2
    partner = 1 << 3
    discord_verification_bot = 1 << 4
    premium = 1 << 5
    first_hackathon_won = 1 << 6

    def __str__(self):
        return self.name


class UserFlag(Enum):
    staff = 1 << 0
    bug_hunter = 1 << 1
    bot_reviewer = 1 << 2
    premium = 1 << 3

    def __str__(self):
        return self.name
