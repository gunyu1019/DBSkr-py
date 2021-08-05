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

from .enums import BotFlag, UserFlag


class BaseFlag:
    """ KoreanBots의 모든 Flag 값의 베이스 모델입니다."""
    def __init__(self, data: int):
        self.value = data


class BotFlagModel(BaseFlag):
    """ KoreanBots에 등록된 디스코드 봇의 Flag 값입니다."""
    def __init__(self, data):
        super().__init__(data)

        self.flags: list = [i for i in BotFlag if i.value & data != 0]

    def empty(self):
        """ Flag 값이 없을 경우 `True`를 리턴합니다."""
        return len(self.flags) == 0

    def official(self):
        """ 디스코드 봇이 공식 봇인 경우 `True`를 리턴합니다."""
        return BotFlag.official in self.flags

    def verification_bot(self):
        """ 디스코드 봇이 KoreanBots로 부터 인증 받은 봇인 경우 `True`를 리턴합니다."""
        return BotFlag.verification_bot in self.flags

    def partner(self):
        """ 디스코드 봇이 KoreanBots의 파트너 봇인 경우 `True`를 리턴합니다."""
        return BotFlag.partner in self.flags

    def discord_verification_bot(self):
        """ 디스코드 봇이 디스코드로 부터 인증 받은 봇인 경우 `True`를 리턴합니다."""
        return BotFlag.discord_verification_bot in self.flags

    def premium(self):
        """ 디스코드 봇이 프리미엄 헤택을 받은 봇인 경우 `True`를 리턴합니다."""
        return BotFlag.premium in self.flags

    def first_hackathon_won(self):
        """ 디스코드 봇이 제1회 KoreanBots 해커톤에 우승한 경우 `True`를 리턴합니다."""
        return BotFlag.first_hackathon_won in self.flags

    def all(self):
        """ 디스코드 봇이 가지고 있는 모든 Flag 값을 리턴합니다."""
        return self.flags


class UserFlagModel(BaseFlag):
    """ KoreanBots에 있는 사용자의 Flag 값입니다."""
    def __init__(self, data):
        super().__init__(data)

        self.flags: list = [i for i in UserFlag if i.value & data != 0]

    def empty(self):
        """ Flag 값이 없을 경우 `True`를 리턴합니다."""
        return len(self.flags) == 0

    def staff(self):
        """ 사용자가 KoreanBots 관리자인 경우 `True`를 리턴합니다."""
        return UserFlag.staff in self.flags

    def bug_hunter(self):
        """ 사용자가 KoreanBots 버그 헌터인 경우 `True`를 리턴합니다."""
        return UserFlag.bug_hunter in self.flags

    def bot_reviewer(self):
        """ 사용자가 KoreanBots 봇 리뷰어인 경우 `True`를 리턴합니다."""
        return UserFlag.bot_reviewer in self.flags

    def premium(self):
        """ 사용자가 KoreanBots로 부터 프리미엄 헤택를 받는 경우 `True`를 리턴합니다."""
        return UserFlag.premium in self.flags
