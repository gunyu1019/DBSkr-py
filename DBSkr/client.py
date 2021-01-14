import asyncio
import logging

log = logging.getLogger(__name__)
from .http import httpClient
from .model import *

class client:
    """discord.py Client를 기반으로 한 KoreanBots 클라이언트와 top.gg 클라이언트를 반환합니다.
        이 클래스를 통하여 KoreanBots API와 top.gg에게 연결됩니다.

        일부 옵션이 Client에 전달될 수 있습니다.

        Parameters
        ==========
        bot:
            discord.py의 client() 혹은 bot() 형태의 변수가 들어갑니다.
        **loop: Optional[asyncio.AbstractEventLoop]
            비동기를 사용하기 위한 asyncio.AbstractEventLoop입니다.
            기본값은 None이거나 bot 오브젝트가 들어왔을 때에는 bot.loop입니다.
            기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.
        **koreanbots: Optional[str]
            koreanbots에서 발급받은 토큰 값이 입력합니다. 만약에 없을 경우 공백으로 둡니다.
        **top.gg: Optional[str]
            topgg에서 발급받은 토큰 값을 입력합니다. 만약에 없을 경우 공백으로 둡니다.
        **autopost: Optional[bool]
            자동으로 1800초(30분)마다 길드 정보를 등록된 토큰값을 통하여 전송할지 설정합니다. 기본값은 False입니다.
    """

    def __init__(self, bot=None, koreanbots:str=None, topgg:str=None, loop:asyncio.AbstractEventLoop=None, autopost:bool=False):
        self.bot = bot
        self.token = {
            "koreanbots":koreanbots,
            "topgg":topgg
        }
        self.loop = loop
        self.http = httpClient(bot=self.bot, token=self.token, loop=loop)
        if self.loop == None and bot is not loop:
            self.loop = bot.loop
        elif self.loop == None and bot is None:
            self.loop = None

        if self.token['koreanbots'] == None: self.koreanbots = False
        else: self.koreanbots = True

        if self.token['topgg'] == None: self.topgg = False
        else: self.topgg = True

        if autopost:
            self.loop.create_task(self.autopost(time=1800))

    async def autopost(self, time:int=30):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
        discord.Client의 .guilds의 수를 등록된 토큰을 `postGuildCount()` 통하여 각 API로 자동으로 보냅니다.
        만약에 두 API 키가 없을 경우, 작동하지 않습니다. 최소 한 곳이상 등록해 주세요.

        Parameters
        ==========
        ** time: Optional[int]
            시간을 분 단위로 설정합니다. 기본값은 30분입니다.

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
        time = time * 60
        self.time = time

        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            log.info('Korean Bots와 top.gg에 서버 갯수를 자동으로 포스트하고 있습니다.')
            await self.postGuildCount()
            await asyncio.sleep(time)

    def GuildCount(self):
        return len(self.bot.guilds)

    async def postGuildCount(self, guild_count: int = None,shard_count: int = None,shard_no: int = None):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            discord.Client의 .guilds의 수와 .shards의 수를 등록된 토큰을 통하여 각 API로 보냅니다.
            만약에 두 API 키가 없을 경우, 작동하지 않습니다. 한 곳이상 등록해 주세요.

            Parameters
            ==========
            ** guild_count: Optional[int]
                서버가 들어가있는 갯수의 값을 임의적으로 지정할 수 있습니다.
                기본값은 모듈에서 자동적으로 `GuildCount()`를 통해 불러옵니다.
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
        log.info("서버 포스트 요청이 들어왔습니다.")
        koreanbots = self.koreanbots
        topgg = self.topgg
        if not koreanbots and not topgg:
            log.error("최소 Koreanbots 혹은 topgg의 토큰을 넣어주시기 바랍니다.")
            return

        if guild_count == None:
            guild_count = self.GuildCount()
        await self.http.postCount(guild_count, shard_count, shard_no)

    async def getVote(self, user:int):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            주어진 유저ID의 하트, 투표 유무 정보를 가져옵니다.

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
        log.info(f"(ID: {user})가 top.gg 혹은 koreanbots에 투표를 했는지 확인 요청이 들어왔습니다.")
        Data = await self.http.getVote(user)
        return typeSite(Data)

    async def getVotes(self):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            본 기능은 top.gg 토큰을 등록했을 경우에만 사용이 가능합니다.
            top.gg에서 투표했던 100명의 목록을 불러옵니다.

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
        log.info(f"최근 12시간 내에 투표한 유저들 목록표에 대해 요청이 들어왔습니다.")
        Data = await self.http.getVotes()
        return [Votes(_) for _ in Data]

    async def getBot(self,id:int =None):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            주어진 봇 ID의 정보를 가져옵니다.

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
        log.info(f"(ID: {id})에 대한 디스코드봇 검색결과 요청이 들어왔습니다.")
        if id == None:
            id = self.bot.user.id
        Data = await self.http.getBot(id)
        return typeSite(Data)

    async def getBots(self, page: int=1):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            디스코드 봇 목록을 koreanbots와 topgg에서 가져옵니다.

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
        log.info("디스코드봇 목록 검색결과 요청이 들어왔습니다.")
        Data = await self.http.getBots(page)
        return typeSite(Data)

    async def getSearchBots(self, query: str):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            디스코드 봇 검색 결과를 koreanbots와 topgg에서 가져옵니다.

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
        log.info(f"(쿼리값: {query})에 대한 디스코드봇 검색결과 요청이 들어왔습니다.")
        Data = await self.http.getSearchBot(query)
        return typeSite(Data)
