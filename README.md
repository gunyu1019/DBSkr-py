<p align="center">
    <img src="https://user-images.githubusercontent.com/16767890/122014718-6716d600-cdfa-11eb-8723-a64ca2df7fe0.png" width="50%" alt="DBSkr"/>
</p>
<h1 align="center">DBSkr</h1>
<p align="center">
    <a href="https://www.codefactor.io/repository/github/gunyu1019/dbskr-py"><img src="https://www.codefactor.io/repository/github/gunyu1019/dbskr-py/badge" alt="CodeFactor" /></a>
    <a href="https://www.codacy.com/gh/gunyu1019/DBSkr-py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=gunyu1019/DBSkr-py&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/8b2a0f3270994feba873554ecc922531" alt="DBSkr"/></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fgunyu1019%2FDBSkr-py?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fgunyu1019%2FDBSkr-py.svg?type=shield"/></a>
    <a href="https://pypistats.org/packages/DBSkr"><img src="https://img.shields.io/pypi/dm/DBSkr" alt="PyPi Downloading" /></a>
    <a href="https://pypi.org/project/DBSkr"><img src="https://img.shields.io/pypi/v/DBSkr" alt="PyPi Version" /></a>
    <a href="https://pypi.org/project/DBSkr"><img src="https://img.shields.io/pypi/pyversions/DBSkr" alt="PyPi Version" /></a>
</p>

한국 디스코드봇을 모아두는 사이트(들)을 위하여 제작된 비공식 파이썬 레퍼(Python3 Wapper) 입니다.

> **더 이상 DBSkr-py의 지원은 없을 예정입니다.**<br/>
> 가능한 공식 SDK를 이용해주시길 부탁드립니다.<br/>

**<지원하는 웹사이트 목록>**<br/>
아래의 사이트를 해당 모듈을 통하여 한 번에 관리&사용 하실 수 있습니다.
* [한국 디스코드봇 리스트(Koreanbots)](https://koreanbots.dev)
* [Discord Bot List(topgg)](https://top.gg)
* [UniqueBots](https://uniquebots.kr/)

> 일부 SDK는 지원을 중단했습니다. 따라서 정상작동하지 않을 수 있습니다!

디스코드 봇 홍보 사이트의 지원을 요청하고자 한다면, [이슈](https://github.com/gunyu1019/DBSkr-py/issues)로 올려주세요.

## 설치 (Installation)
파이썬 3.7 혹은 그 이상의 버전이 필요합니다.
**Install via pip (recommended)**
```
# Linux/macOS
python -3 -m pip install DBSkr

# Windows
py -3 -m pip install DBSkr
```

**Install from source**
```
# Linux/macOS
python -3 -m pip install git+https://github.com/gunyu1019/DBSkr-py

# Windows
py -3 -m pip install git+https://github.com/gunyu1019/DBSkr-py
```

## 로깅 (Logging)
DBSkr은 파이썬의 `logging` 모듈을 사용하여, 오류 및 디버그 정보를 기록합니다.
로깅 모듈이 설정되지 않은 경우 오류 또는 경고가 출력되지 않으므로 로깅 모듈을 구성하는 것이 좋습니다.

로깅 모듈의 레벨은 `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`가 있으며 `INFO`로 설정하는 것을 추천합니다.
```python
import logging

logger = logging.getLogger('DBSkr')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(filename)s] [%(name)s:%(module)s] [%(levelname)s]: %(message)s'))
logger.addHandler(handler)
```


## 예시(Example)

### 자동으로 서버 수 업데이트하기
주기적으로 봇의 수를 업데이트합니다. (discord.Client 기준)
```python
import discord
import DBSkr

client = discord.Client()
Bot = DBSkr.Client(
    bot=client,
    koreanbots_token='Korean Bots 봇 토큰',
    topgg_token='top.gg 봇 토큰',
    uniquebots_token='Unique Bots 봇 토큰',
    autopost=True
)

@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')

client.run('Discord 토큰')
```

주기적으로 봇의 수를 업데이트합니다. (discord.ext.command 기준)
```python
import discord
import DBSkr
from discord.ext import commands

client = commands.Bot(command_prefix="!!")
Bot = DBSkr.Client(
    bot=client,
    koreanbots_token='Korean Bots 봇 토큰',
    topgg_token='top.gg 봇 토큰',
    uniquebots_token='Unique Bots 봇 토큰',
    autopost=True
)

@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')

client.run('Discord 토큰')
```

### 직접 서버 수 업데이트하기
사용자가 직접 서버 수를 업데이트 할 수 있습니다.
```python
import discord
import DBSkr

client = discord.Client()
Bot = DBSkr.Client(
    bot=client,
    koreanbots_token='Korean Bots 봇 토큰',
    topgg_token='top.gg 봇 토큰',
    uniquebots_token='Unique Bots 봇 토큰'
)

@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')

@client.event
async def on_message(message):
    if message.content == "서버수업데이트":
        await Bot.stats()

client.run('Discord 토큰')
```

### 유저 투표 유무 불러오기
특정 사용자가 12시간내에 투표 혹은 하트를 했는지 안했는지에 대한 값이 나옵니다.
```python
import discord
import DBSkr

client = discord.Client()
Bot = DBSkr.Client(
    bot=client,
    koreanbots_token='Korean Bots 봇 토큰',
    topgg_token='top.gg 봇 토큰',
    uniquebots_token='Unique Bots 봇 토큰'
)

@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')

@client.event
async def on_message(message):
    author = message.author
    vote_data = await Bot.vote(author.id)
    print(f"{author}투표 유무: \nKoreanBots: {vote_data.koreanbots}\nTop.gg: {vote_data.topgg}\nUniqueBots: {vote_data.uniquebots}")
    # Bool 형태이므로, 두 값에는 True 혹은 False가 리턴됨. 그러나 토큰값이 없을 경우 None이 이런됨.

client.run('Discord 토큰')
```

### 봇의 아이디로 봇 정보 불러오기
```python
import discord
import DBSkr

client = discord.Client()
Bot = DBSkr.Client(
    bot=client,
    koreanbots_token='Korean Bots 봇 토큰',
    topgg_token='top.gg 봇 토큰',
    uniquebots_token='Unique Bots 봇 토큰'
)

@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')
    
    data = await Bot.bot(680694763036737536)
    print(f"{data.koreanbots}\n{data.topgg}\n{data.uniquebots}")
    
client.run('Discord 토큰')
```

## 라이센스(License)
DBSkr의 라이센스는 [MIT License](LICENSE)를 부여합니다.


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fgunyu1019%2FDBSkr-py.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fgunyu1019%2FDBSkr-py?ref=badge_large)
