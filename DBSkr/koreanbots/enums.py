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

from enum import Enum
from ..enums import get_value


class WidgetType(Enum):
    """ KoreanBots의 위젯 유형"""
    Vote = "votes"
    Server = "servers"
    Status = "status"


class WidgetStyle(Enum):
    """ KoreanBots의 위젯 스타일"""
    classic = "classic"
    flat = "flat"


class Category(Enum):
    """ KoreanBots 카테고리"""
    moderation = "관리"
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
    """ 디스코드 봇의 상태"""
    online = "online"
    idle = "idle"
    dnd = "dnd"
    streaming = "streaming"
    offline = "offline"


class State(Enum):
    """ KoreanBots에 등록된 디스코드 봇의 상태"""
    ok = "ok"
    reported = "reported"
    blocked = "blocked"
    private = "private"
    archived = "archived"


class BotFlag(Enum):
    """ 디스코드 봇의 Flag 값"""
    official = 1 << 0
    verification_bot = 1 << 2
    partner = 1 << 3
    discord_verification_bot = 1 << 4
    premium = 1 << 5
    first_hackathon_won = 1 << 6

    def __str__(self):
        return self.name


class UserFlag(Enum):
    """ 유저의 Flag 값"""
    staff = 1 << 0
    bug_hunter = 1 << 1
    bot_reviewer = 1 << 2
    premium = 1 << 3

    def __str__(self):
        return self.name
