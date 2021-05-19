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
    def __init__(self, data: int):
        self.value = data


class BotFlagModel(BaseFlag):
    def __init__(self, data):
        super().__init__(data)

        self.flags: list = [i for i in BotFlag if i.value & data != 0]

    def empty(self):
        return len(self.flags) == 0

    def official(self):
        return BotFlag.official in self.flags

    def verification_bot(self):
        return BotFlag.verification_bot in self.flags

    def partner(self):
        return BotFlag.partner in self.flags

    def discord_verification_bot(self):
        return BotFlag.discord_verification_bot in self.flags

    def premium(self):
        return BotFlag.premium in self.flags

    def first_hackathon_won(self):
        return BotFlag.first_hackathon_won in self.flags

    def all(self):
        return self.flags


class UserFlagModel(BaseFlag):
    def __init__(self, data):
        super().__init__(data)

        self.flags: list = [i for i in UserFlag if i.value & data != 0]

    def empty(self):
        return len(self.flags) == 0

    def staff(self):
        return UserFlag.staff in self.flags

    def bug_hunter(self):
        return UserFlag.bug_hunter in self.flags

    def bot_reviewer(self):
        return UserFlag.bot_reviewer in self.flags

    def premium(self):
        return UserFlag.premium in self.flags
