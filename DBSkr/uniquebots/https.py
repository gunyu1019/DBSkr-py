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

import asyncio
import aiohttp

from .api import Api, GraphQL
from .models import Bot, Stats, Vote, User

from typing import List


class HttpClient:
    """ UniqueBots의 Http 클라이언트를 선언합니다.
     이 클래스를 통하여 UniqueBots API에 연결됩니다.

    Parameters
    ----------
    token: Optional[str]
        UniqueBots 에서 발급받은 봇의 토큰 키값 입니다. 일부 데이터를 반영하거나 불러올 때 토큰 값이 사용될 수 있습니다.
    session: Optional[aiohttp.ClientSession]
        HttpClient 를 위한 aiohttp 의 ClientSession 클래스 입니다.
        기본값은 None이며, 자동으로 ClientSession을 생성하게 됩니다.
    loop: Optional[asyncio.AbstractEventLoop]
        비동기를 사용하기 위한 asyncio.AbstractEventLoop 입니다.
        기본값은 None 입니다.
        기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.
    """
    def __init__(self,
                 token: str = None,
                 session: aiohttp.ClientSession = None,
                 loop: asyncio.AbstractEventLoop = None):
        self.token = token
        self.requests = Api(token=token, session=session, loop=loop)
        self.session = session

    async def bot(self, bot_id: int) -> Bot:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        봇 정보를 불러옵니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.

        Returns
        -------
        Bot:
            UniqueBots로 부터 들어온 봇 정보가 포함되어 있습니다.
        """
        data = GraphQL(query="""{
            bot (id: $bot_id) {
                id, name, avatarURL, trusted, discordVerified, guilds, status, brief, description, invite, website,
                support, prefix, library { name }, categories { name, id }, owners { 
                    id, tag, avatarURL, admin, description, bots {
                        id, name, avatarURL, trusted, discordVerified, guilds, status, brief, description, invite,
                        website, support, prefix, library { name }, categories { name, id }, slug, premium, 
                        owners { id }
                    }
                }
            }
        }""")

        data.set_variables({
            'bot_id': str(bot_id)
        })

        result = await self.requests.requests(data)
        result = result.get("data", {}).get("bot")
        return Bot(result)

    async def stats(self, bot_id: int, guild_count: int) -> Stats:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        봇 정보를 수신하거나 발신합니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.
        guild_count: int
            서버 갯수가 포함되어 있습니다.
        Returns
        -------
        Stats:
            UniqueBots로 부터 들어온 봇 상태 정보가 포함되어 있습니다.
        """
        data = GraphQL(query="""{
            bot (id: $bot_id) {
                guilds(patch: $guild_count)
            }
        }""")

        data.set_variables({
            'bot_id': str(bot_id),
            'guild_count': guild_count
        })

        result = await self.requests.requests(data)
        result = result.get("data", {}).get("bot")
        return Stats(result)

    async def vote(self, bot_id: int, user_id: int) -> Vote:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        `user_id`에 들어있는 사용자가 봇에 하트를 누른 여부에 대하여 불러옵니다.

        Parameters
        ----------
        bot_id: int
            봇 ID 값이 포함됩니다.
        user_id: int
            유저 ID 값이 포함되어 있습니다.

        Returns
        -------
        Vote:
            UniqueBots로 부터 들어온 사용자 투표 정보에 대한 정보가 포함되어 있습니다.
        """
        data = GraphQL(query="""{
                    bot (id: $bot_id) {
                        heartClicked(user: $user_id)
                    }
                }""")

        data.set_variables({
            'bot_id': str(bot_id),
            'user_id': str(user_id)
        })

        result = await self.requests.requests(data)
        result = result.get("data", {}).get("bot")
        return Vote(result)

    async def votes(self, bot_id: int) -> List[User]:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        투표를 누른 사용자 목록을 모두 불러옵니다.

        Returns
        -------
        List[User]:
            UniqueBots로 부터 투표 누른 사용자 목록에 대한 정보가 포함되어 있습니다.
        """
        data = GraphQL(query="""{
                    bot (id: $bot_id) {
                        hearts {
                            from {
                                id, tag, avatarURL, admin, description, bots {
                                    id, name, avatarURL, trusted, discordVerified, guilds, status, brief,
                                    description, invite, website, support, prefix, library { name },
                                    categories { name, id }, slug, premium, owners { 
                                        id, tag, avatarURL, admin, description, bots {
                                            id, name, avatarURL, trusted, discordVerified, guilds, status, brief,
                                            description, invite, website, support, prefix, library { name }, categories
                                            { name, id }, slug, premium, owners { id }
                                        }
                                    } 
                                }
                            }
                        }
                    }
                }""")

        data.set_variables({
            'bot_id': str(bot_id)
        })

        result = await self.requests.requests(data)
        result = result.get("data", {}).get("bot", {}).get("hearts", [])
        return [User(user.get("from", {})) for user in result]

    async def users(self, user_id: int) -> User:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        사용자 정보를 불러옵니다.

        Parameters
        ----------
        user_id: int
            사용자 ID 값이 포함됩니다.

        Returns
        -------
        User
            UniqueBots로 부터 들어온 사용자 정보가 포함되어 있습니다.
        """
        data = GraphQL(query="""{
                    profile (id: $user_id) {
                        id, tag, avatarURL, admin, description, bots {
                            id, name, avatarURL, trusted, discordVerified, guilds, status, brief, description, invite,
                            website, support, prefix, library { name }, categories { name, id }, slug, premium, 
                            owners { 
                                id, tag, avatarURL, admin, description, bots { id }
                            }
                        }
                    }
                }""")

        data.set_variables({
            'user_id': str(user_id)
        })

        result = await self.requests.requests(data)
        result = result.get("data", {}).get("profile")
        return User(result)
