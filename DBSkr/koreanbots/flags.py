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
