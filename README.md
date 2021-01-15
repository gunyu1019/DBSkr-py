# DBSkr
koreanbots와 top.gg를 위한 비공식 파이썬 API 레퍼입니다.
* [KoreanBots 공식 SDK](https://github.com/koreanbots/py-sdk)
* [topgg 공식 SDK](https://github.com/top-gg/python-sdk)

## 설치 (Installation)
파이썬 3.6 혹은 그 이상의 버전이 필요합니다.
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
python -3 -m pip install git+https://github.com/top-gg/DBL-Python-Library

# Windows
py -3 -m pip install git+https://github.com/top-gg/DBL-Python-Library
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
Bot = DBSkr.client(client, koreanbots='Korean Bots 봇 토큰', topgg='top.gg 봇 토큰',autopost=True)

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
import DBSkr
from discord.ext import commands

client = commands.Bot()
Bot = DBSkr.client(client, koreanbots='Korean Bots 봇 토큰', topgg='top.gg 봇 토큰',autopost=True)

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
Bot = DBSkr.client(client, koreanbots='Korean Bots 봇 토큰', topgg='top.gg 봇 토큰')

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
        await Bot.postGuildCount()

client.run('Discord 토큰')
```

### 유저 투표 유무 불러오기
특정 사용자가 12시간내에 투표 혹은 하트를 했는지 안했는지에 대한 값이 나옵니다.
```python
import discord
import DBSkr

client = discord.Client()
Bot = DBSkr.client(client, koreanbots='Korean Bots 봇 토큰', topgg='top.gg 봇 토큰')

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
    vote_data = Bot.getVote(author.id)
    print(f"{author}투표 유무: \nKoreanBots: {vote_data.koreanbots}\nTop.gg: {vote_data.topgg}")
    # Bool 형태이므로, 두 값에는 True 혹은 False가 리턴됨. 그러나 토큰값이 없을 경우 None이 이런됨.

client.run('Discord 토큰')
```

### 봇의 아이디로 봇 정보 불러오기
```python
import discord
import DBSkr

client = discord.Client()
Bot = DBSkr.client(client, koreanbots='Korean Bots 봇 토큰', topgg='top.gg 봇 토큰')

@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')
    
    Data = Bot.getBot(680694763036737536)
    # Koreanbots에서 불러올 경우 토큰값이 필요없지만, top.gg에서 불러올 경우 토큰 값이 필요함.
    print(f"{Data.koreanbots}\n{Data.topgg})
    
client.run('Discord 토큰')
```
