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

import aiohttp

from .api import Api, GraphQL
from .models import Bot, Stats, Vote, User


class HttpClient:
    def __init__(self, token: str = None, session: aiohttp.ClientSession = None):
        self.token = token
        self.requests = Api(token=token, session=session)
        self.session = session

    async def bot(self, bot_id: int) -> Bot:
        data = GraphQL(query="""{
            bot (id: $bot_id) {
                id, name, avatarURL, trusted, discordVerified, guilds, status, brief, description, invite, website,
                support, prefix, library { name }, categories { name, id }
            }
        }""")

        data.variables = """{
            "bot_id": "{}" 
        }""".format(bot_id)

        result = await self.requests.requests(data)
        result = result.get("data").get("bot")
        return Bot(result)

    async def stats(self, bot_id: int, guild_count: int) -> Stats:
        data = GraphQL(query="""{
            bot (id: $bot_id) {
                guilds(patch: $guild_count)
            }
        }""")

        data.variables = """{
            "bot_id": "{}",
            "guild_count": {} 
        }""".format(bot_id, guild_count)

        result = await self.requests.requests(data)
        result = result.get("data").get("bot")
        return Stats(result)

    async def vote(self, bot_id: int, user_id: int) -> Vote:
        data = GraphQL(query="""{
                    bot (id: $bot_id) {
                        heartClicked(user: user_id)
                    }
                }""")

        data.variables = """{
                    "bot_id": "{}",
                    "user_id": {} 
                }""".format(bot_id, user_id)

        result = await self.requests.requests(data)
        result = result.get("data").get("bot")
        return Vote(result)

    async def votes(self, bot_id: int) -> list:
        data = GraphQL(query="""{
                    bot (id: $bot_id) {
                        hearts {
                            from {
                                id, tag, avatarURL, admin, description, bots {
                                    id, name, avatarURL, trusted, discordVerified, guilds, status, brief,
                                    description, invite, website, support, prefix, library { name },
                                    categories { name, id }, slug, premium, owner { id } }
                            }
                        }
                    }
                }""")

        data.variables = """{
                    "bot_id": "{}"
                }""".format(bot_id)

        result = await self.requests.requests(data)
        result = result.get("data").get("bot")
        return result

    async def users(self, user_id: int) -> User:
        data = GraphQL(query="""{
                    profile (id: $user_id) {
                        id, tag, avatarURL, admin, description, bots {
                            id, name, avatarURL, trusted, discordVerified, guilds, status, brief, description, invite,
                            website, support, prefix, library { name }, categories { name, id }, slug, premium
                        }
                    }
                }""")

        data.variables = """{
                    "user_id": "{}"
                }""".format(user_id)

        result = await self.requests.requests(data)
        result = result.get("data").get("profile")
        return User(result)
