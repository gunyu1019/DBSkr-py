<p align="center">
    <img src="https://user-images.githubusercontent.com/16767890/122014718-6716d600-cdfa-11eb-8723-a64ca2df7fe0.png" width="50%"/>
</p>
<h1 align="center">DBSkr</h1>
<p align="center">
    <a href="https://www.codefactor.io/repository/github/gunyu1019/dbskr-py"><img src="https://www.codefactor.io/repository/github/gunyu1019/dbskr-py/badge" alt="CodeFactor" /></a>
    <a href="https://www.codacy.com/gh/gunyu1019/DBSkr-py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=gunyu1019/DBSkr-py&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/8b2a0f3270994feba873554ecc922531"/></a>
    <a href="https://pypistats.org/packages/DBSkr"><img src="https://img.shields.io/pypi/dm/DBSkr" alt="PyPi Downloading" /></a>
    <a href="https://pypi.org/project/DBSkr"><img src="https://img.shields.io/pypi/v/DBSkr" alt="PyPi Version" /></a>
    <a href="https://pypi.org/project/DBSkr"><img src="https://img.shields.io/pypi/pyversions/DBSkr" alt="PyPi Version" /></a>
</p>

한국 디스코드봇을 모아두는 사이트(들)을 위하여 제작된 비공식 파이썬 레퍼(Python3 Wapper) 입니다.

**<지원하는 웹사이트 목록>**<br/>
아래의 사이트를 해당 모듈을 통하여 한 번에 관리&사용 하실 수 있습니다.
* [한국 디스코드봇 리스트(Koreanbots)](https://koreanbots.dev)
* [Discord Bot List(topgg)](https://top.gg)
* [UniqueBots](https://uniquebots.kr/)
디스코드봇 홍보 사이트를 추가지원을 하기 위해선 gunyu1019@yhs.kr로 문의해주시기 바랍니다.

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
python -3 -m pip install git+https://github.com/gunyu1019/DBSkr

# Windows
py -3 -m pip install git+https://github.com/gunyu1019/DBSkr
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