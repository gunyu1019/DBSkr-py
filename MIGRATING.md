# Migrating to v2.0 (한국어)
<img src="https://user-images.githubusercontent.com/16767890/122014718-6716d600-cdfa-11eb-8723-a64ca2df7fe0.png" width="50%"/><br/>
DBSkr-py의 메이저 업데이트로 인해 변경된 사항을 나열하였습니다.
DBSkr v2.0은 v1.0에서 다양한 사항을 변경하였습니다.
아래의 내용을 참고하여 코드를 개선해주시길 부탁드립니다.

## UniqueBots API Additional Support
[UniqueBots](https://uniquebots.kr/) 의 SDK를 새롭게 지원합니다.
UniqueBots의 추가 요청이 가끔 들어왔으며, v2.0부터 공식적으로 지원하게 되었습니다.

## Koreanbots API version up
Koreanbots의 v2 배포에 따른 API 구조가 다소 변경되었습니다. 따라서, 새롭게 SDK를 구성하여 알맞게 대응하게 되었습니다.
**BASE URL 자체가 변경되었기 때문에 v1.0에서 DBSkr.koreanbots SDK를 정상적으로 이용하실 수 없습니다**

### Change how Koreanbots search for bots
KoreanBots 에서 봇을 검색하는 방법이 다소 변경되었습니다.
아래의 두가재 함수가 추가되었으며 용도는 다음과 같습니다.

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Description</th>
  </tr>
</thead>
    <tbody>
        <tr>
            <td>koreanbots.HttpClient.new</td>
            <td>Koreanbots에 새롭게 등재된 봇 목록을 불러옵니다.</td>
        </tr>
        <tr>
            <td>koreanbots.HttpClient.votes</td>
            <td>하트를 누른 랭킹 순으로 봇의 목록을 불러옵니다. <br/><b>Koreanbots SDK 내에서는 원래 하트를 누른 사용자 목록을 제공하지 않습니다.</b></td>
        </tr>
    </tbody>
</table>

또한 각 함수(`search`, `new`, `votes`)에는 page라는 매개변수가 추가되었으며,
total과 current를 Data Model에 추가하였기 때문에 총 페이지수와 현재 페이지 확인하실 수 있습니다.

## Independent SDK Configuration
DBSkr v2.0부터는 다른 API 구조를 모두 대응하기 위하여, 각 모듈을 독립적으로 구성하게 되었습니다.
만약에 일부 모듈만 사용하실 꺼면, 직접 SDK에 들어있는 `Client class`를 사용하셔도 됩니다.

아래와 같이 SDK를 직접꺼내서 사용하실 수 있습니다.
```python
from DBSkr import koreanbots
from DBSkr import topgg
from DBSkr import uniquebots
```

## Major Class Changes
DBSkr v2.0에서부터 구조개선을 위해 클래스 내에 있는 함수를 모두 변경하였습니다.
따라서 DBSkr v1.0과 비교하면 아래와 같습니다.

<table>
<thead>
  <tr>
    <th>Before</th>
    <th>After</th>
  </tr>
</thead>
    <tbody>
        <tr>
            <td>Client.getBot</td>
            <td>Client.bot</td>
        </tr>
        <tr>
            <td>Client.post_guild_count</td>
            <td>Client.stats</td>
        </tr>
        <tr>
            <td>Client.getVote</td>
            <td>Client.vote</td>
        </tr>
        <tr>
            <td>Client.getVotes</td>
            <td>Client.votes</td>
        </tr>
        <tr>
            <td>Client.getSearchBot</td>
            <td>(Removed)</td>
        </tr>
        <tr>
            <td>httpClient.getBot</td>
            <td>HttpClient.bot</td>
        </tr>
        <tr>
            <td>httpClient.post_guild_count</td>
            <td>HttpClient.stats</td>
        </tr>
        <tr>
            <td>httpClient.getVote</td>
            <td>HttpClient.vote</td>
        </tr>
        <tr>
            <td>httpClient.getVotes</td>
            <td>HttpClient.votes</td>
        </tr>
        <tr>
            <td>httpClient.getSearchBot</td>
            <td>(Removed)</td>
        </tr>
    </tbody>
</table>

봇을 검색하는 함수는 각 SDK간 호환성 문제로 v2.0부터 제거되었습니다.
해당 기능은 직접 SDK 내에 있는 `HttpClient`를 꺼내시면 사용이 가능합니다.
(UniqueBots는 검색기능을 원래 지원하지 않음.)

## Major Data Class Changes
기존 Data Class에는 `getAttr()`를 사용하여, `Class.content` 를 불러올 수 있었습니다.
해당 방법은 사전에 통보 없이 SDK 사용방법이 바뀌면, 업데이트 없이 개선할 수 있지만 무슨 업데이트인지 알아야할 필요가 있었으며
Data Class의 통일성 강화를 위하여 모두 직접 선언해주는 방법으로 교체하였습니다. 

사용방법이 다소 복잡하기 때문에 각 Model의 `docstring`를 확인해주세요

## Widget Support
Koreanbots와 topgg에는 위젯을 지원합니다. 위젯에 대해 대응되는 업데이트를 진행하였습니다.
`Client.widget()` 또는 `HttpClient.widget()`를 통하여 사용하실 수 있으며, `Asset` 모델에 저장됩니다.

## Add Assets Class
Discord Avatar, SDK Widget를 저장하기 위한 `Assets Class`를 추가하였습니다.
`save()`, `read()`를 통하여, 이미지 파일을 알맞게 사용하시기 바랍니다.