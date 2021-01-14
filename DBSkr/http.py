import asyncio
import aiohttp
import logging

import json
import datetime
log = logging.getLogger(__name__)

from .model import *
from .errors import *

BASE = {
    "topgg":"https://top.gg/api",
    "koreanbots":"https://api.koreanbots.dev"
}

async def content_type(response):
    if response.headers['Content-Type'] == 'application/json; charset=utf-8':
        return await response.json()
    return await response.text()

class httpClient:
    """DBSkr의 Http 클라이언트를 반환합니다.
        이 클래스를 통하여 KoreanBots API와 top.gg에게 연결됩니다.

        일부 옵션이 Client에 전달될 수 있습니다.

        Parameters
        ==========

        ** bot: Optional
            discord.py의 client() 혹은 bot() 형태의 변수가 들어갑니다.
        **loop: Optional[asyncio.AbstractEventLoop]
            비동기를 사용하기 위한 asyncio.AbstractEventLoop입니다.
            기본값은 None이거나 bot 오브젝트가 들어왔을 때에는 bot.loop입니다.
            기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.
        **token: Optional[dict]
            koreanbots 토큰과 top.gg 토큰이 dict형태로 들어갑니다.
    """
    def __init__(self, token:dict, bot=None, loop:asyncio.AbstractEventLoop=None):
        self.token = token
        self.loop = loop
        self.bot = bot
        if token['koreanbots'] == None: self.koreanbots = False
        else: self.koreanbots = True

        if token['topgg'] == None: self.topgg = False
        else: self.topgg = True

    async def request(self, method, endpoint, base, count:int=0, auth:bool=True, **kwargs):
        """주어진 값에 따른 base를 기반으로 한 API로 보냅니다.

            Parameters
            ==========
            method: str
                HTTP 리퀘스트 메소드
            url: str
                topgg API 또는 KoreanBots API의 엔드포인트
            base: str
                API를 보낼 베이스URL를 선정합니다.
                koreanbots와 topgg 중에서 한가지를 선택해주세요.
            auth: Optional[bool]
                API 리퀘스트에 토큰과 함께 전송할지 입니다.
                기본값은 True입니다.
            count: Optional[int]
                만약 API의 요청 횟수가 초과될 경우 최대 5회까지 재실행합니다.
                기본값으로는 0이 들어가있으며, count값이 5가 될 경우 오류와 함께 중단합니다.

            Raises
            ==========
            .errors.AuthorizeError
                토큰이 필요한 엔드포인트지만, 클라이언트에 토큰이 주어지지 않았습니다.
            .errors.Unauthrized
                인증되지 않았습니다, KoreanBots 토큰이 잘못되었을 수 있습니다.
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        url = f"{BASE[base]}{endpoint}"
        headers = {
            'Content-Type': 'application/json'
        }
        if base == 'koreanbots' and auth:
            headers['token'] = self.token['koreanbots']
        elif base == 'topgg' and auth:
            headers['Authorization'] = self.token['topgg']

        kwargs['headers'] = headers
        log.debug(f"{url}를 향한 요청이 들어왔습니다.")
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as resp:
                data = await content_type(resp)
                if resp.status == 200:
                    return data
                elif resp.status == 400 and base == 'koreanbots' and endpoint == '/bots/servers':
                    log.debug("업데이트하려는 서버 수와 기존의 서버 수가 동일하여, 업데이트할 수 없습니다.")
                    return
                elif resp.status == 429:
                    if base == "koreanbots":
                        retry_after = json.loads(resp.headers.get('Retry-After'))
                    elif base == "topgg":
                        resetLimitTimestamp = int(resp.headers.get('x-ratelimit-reset'))
                        resetLimit = datetime.fromtimestamp(resetLimitTimestamp)
                        retryAfter = resetLimit - datetime.now()
                        retry_after = retryAfter.total_seconds()
                    mins = retry_after / 60
                    log.warning(f"지정된 시간에 너무 많은 요청을 보냈습니다. {mins}분({retry_after}초) 후 다시 시도하겠습니다.")
                    if count >= 5:
                        log.error("많은 시도에도 실패하였습니다.")
                        return
                    await asyncio.sleep(retry_after)
                    return await self.request(method=method, endpoint=endpoint, base=base, count=count+1, **kwargs)

                if resp.status == 400:
                    raise HTTPException(resp, data)
                elif resp.status == 401:
                    raise Unauthorized(resp, data)
                elif resp.status == 403:
                    raise Forbidden(resp, data)
                elif resp.status == 404:
                    raise NotFound(resp, data)
                else:
                    raise HTTPException(resp, data)

    async def postCount(self, guild_count, shard_count: int = None, shard_no: int = None):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            임의적으로 정해진 수치값을 통하여 각 API들에게 보냅니다.
            해당 기능은 koreanbots 혹은 topgg의 토큰이 필요합니다.(token값을 기재하거나, client를 이용해주세요.)
            만약에 두 API 키가 없을 경우, 작동하지 않습니다. 한 곳이상 등록해 주세요.

            Parameters
            ==========
            guild_count: [int]
                서버가 들어가있는 갯수의 값을 지정할 수 있습니다.
            ** shard_count: Optional[int]
                샤드 갯수가 들어갑니다. 샤드는 top.gg에만 업로드 됩니다.
            ** shard_no: Optional[int]
                현재의 샤드 번호가 들어갑니다. 샤드는 top.gg에만 업로드 됩니다.

            Raises
            ==========
            .errors.Unauthrized
                인증되지 않았습니다, 두 토큰 중 어느 하나라도 토큰이 잘못되었을 수 있습니다.
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        if self.koreanbots:
            await self.request('POST', '/bots/servers','koreanbots', json={'servers': guild_count})

        if self.topgg:
            if shard_count is not None:
                json_data = {
                    'server_count': guild_count,
                    'shard_id': shard_no,
                    'shard_count': shard_count
                }
            else:
                json_data = {
                    'server_count': guild_count
                }
            await self.request('POST', f'/bots/{self.bot.user.id}/stats', 'topgg', json=json_data)

    async def getVote(self, user:int):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            주어진 유저ID의 하트, 투표 유무 정보를 가져옵니다.
            해당 기능은 koreanbots 혹은 topgg의 토큰이 필요합니다.(token값을 기재하거나, client를 이용해주세요.)

            Parameters
            ==========
            user: int
                정보를 가져올 유저의 ID값이 들어갑니다.

            Returns
            =======
            ** koreanbots: Optional[bool]
                해당 유저가 koreanbots에서 하트를 유모 정보를 가져옵니다.
            ** topgg: Optional[bool]
                해당 유저가 topgg에서 최근 12시간내에 투표를 유무 정보를 가져옵니다.

            Raises
            ==========
            .errors.Unauthrized
                인증되지 않았습니다, 두 토큰 중 어느 하나라도 토큰이 잘못되었을 수 있습니다.
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        final_data = {}
        if self.koreanbots:
            data = await self.request('GET', f'/bots/voted/{user}','koreanbots')
            final_data['koreanbots'] = data['voted']

        if self.topgg:
            data = await self.request('GET', f'/bots/{self.bot.user.id}/check', 'topgg', params={'userId':user})
            final_data['topgg'] = data['voted']
        return final_data

    async def getVotes(self):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            본 기능은 top.gg 토큰을 등록했을 경우에만 사용이 가능합니다.
            top.gg에서 투표했던 100명의 목록을 불러옵니다.
            본 함수는 topgg의 토큰이 필요합니다.(token값을 기재하거나, client를 이용해주세요.)

            Returns
            =======
            Users: [List]
                유저의 목록이 dict 형태로 돌아갑니다.

            Raises
            ==========

            .errors.Unauthrized
                인증되지 않았습니다, 두 토큰 중 어느 하나라도 토큰이 잘못되었을 수 있습니다.
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        if self.topgg:
            return await self.request('GET', f'/bots/{self.bot.user.id}/votes', 'topgg')

    async def getBot(self, bot:int):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            주어진 봇 ID의 정보를 가져옵니다.
            본 함수는 topgg의 정보를 구하기 위해선, topgg의 토큰이 필요합니다.(token값을 기재하거나, client를 이용해주세요.)

            Parameters
            ==========
            id: Optional[int]
                정보를 가져올 디스코드 봇의 ID값이 들어갑니다.
                기본값은 본인 봇 ID입니다.

            Returns
            =======
            ** koreanbots: Optional[Object]
                해당 koreanbots에서 불러온 디스코드봇 정보가 들어갑니다.
            ** topgg: Optional[Object]
                해당 topgg에서 불러온 디스코드봇 정보가 들어갑니다.

            Raises
            ==========

            .errors.Unauthrized
                인증되지 않았습니다, 두 토큰 중 어느 하나라도 토큰이 잘못되었을 수 있습니다.
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        final_data = {}
        if self.topgg:
            data = await self.request('GET', f'/bots/{bot}', 'topgg')
            transform_data = data['results']
            final_data['topgg'] = Bot(transform_data)
        final_data['koreanbots'] = Bot(await self.request('GET', f'/bots/get/{bot}', 'koreanbots',auth=False))
        return final_data

    async def getBots(self, page:int =1):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            디스코드 봇 목록을 koreanbots와 topgg에서 가져옵니다.
            본 함수는 topgg의 정보를 구하기 위해선, topgg의 토큰이 필요합니다.(token값을 기재하거나, client를 이용해주세요.)

            Parameters
            ==========
            page: Optional[int]
                페이지 번호가 들어갑니다. 기본적으로 10개씩 불러오며, 기본값은 1입니다.

            Returns
            =======
            ** koreanbots: Optional[Object]
                해당 koreanbots에서 불러온 디스코드봇들 정보가 들어갑니다.
            ** topgg: Optional[Object]
                해당 topgg에서 불러온 디스코드봇들 정보가 들어갑니다.

            Raises
            ==========

            .errors.Unauthrized
                인증되지 않았습니다, 두 토큰 중 어느 하나라도 토큰이 잘못되었을 수 있습니다.
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        final_data = {}
        if self.topgg:
            first = (page-1)*10
            data = await self.request('GET', '/bots/', 'topgg',params={'offset':first, 'limit':10})
            transform_data = data['results']
            final_data['topgg'] = [Bots(_) for _ in transform_data]
        data = await self.request('GET', f'/bots/get/', 'koreanbots',auth=False, params={'page': page})
        final_data['koreanbots'] = [Bots(_) for _ in data['data']]
        return final_data

    async def getSearchBot(self, query:str):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            디스코드 봇 검색 결과를 koreanbots와 topgg에서 가져옵니다.
            본 함수는 topgg의 정보를 구하기 위해선, topgg의 토큰이 필요합니다.(token값을 기재하거나, client를 이용해주세요.)

            Parameters
            ==========
            query: Optional[str]
                검색하는 값이 들어갑니다.

            Returns
            =======
            ** koreanbots: Optional[Object]
                해당 koreanbots에서 불러온 디스코드봇들 정보가 들어갑니다.
            ** topgg: Optional[Object]
                해당 topgg에서 불러온 디스코드봇들 정보가 들어갑니다.

            Raises
            ==========
            .errors.Unauthrized
                인증되지 않았습니다, 두 토큰 중 어느 하나라도 토큰이 잘못되었을 수 있습니다.
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        final_data = {}
        if self.topgg:
            data = await self.request('GET', f'/bots/', 'topgg',params={'search':query})
            transform_data = data['results']
            final_data['topgg'] = [Bots(_) for _ in transform_data]
        data = await self.request('GET', f'/bots/get', 'koreanbots',auth=False, params={'q':query})
        final_data['koreanbots'] = [Bots(_) for _ in data['data']]
        return final_data