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

from typing import Union
from enum import Enum

from ..enums import get_value
from .models import Category


class Status(Enum):
    online = "online"
    idle = "idle"
    dnd = "dnd"
    offline = "offline"


class Categories(Enum):
    moderation = Category(category_id="moderation", name="관리")
    music = Category(category_id="music", name="음악")
    translation = Category(category_id="translation", name="번역")
    chat = Category(category_id="chat", name="대화")
    search = Category(category_id="search", name="검색")
    game = Category(category_id="game", name="게임")
    utilities = Category(category_id="util", name="유틸")
    economy = Category(category_id="economy", name="경제")
    gambling = Category(category_id="gambling", name="도박")
    stats = Category(category_id="total", name="전적")
    meme = Category(category_id="meme", name="밈")
    leveling = Category(category_id="leveling", name="레벨링")
    dashboard = Category(category_id="webdash", name="웹 대시보드")

    def __eq__(self, other: Union[Enum, Category, str]):
        return self.value if not isinstance(other, str) else self.value.id == other if isinstance(other, str) else other.value

    def __ne__(self, other):
        return not self.__eq__(other)
