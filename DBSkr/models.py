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


class WebsiteBase:
    def __init__(self, koreanbots=None, topgg=None, uniquebots=None):
        self.koreanbots = koreanbots
        self.topgg = topgg
        self.uniquebots = uniquebots


class WebsiteBot(WebsiteBase):
    """ 웹사이트로 부터 들어온 봇 정보의 모델을 나타냅니다.

    Attributes
    ------------
    koreanbots: Optional
        koreanbots로 부터 들어온 값이 포함됩니다.
    topgg: Optional
        top.gg로 부터 들어온 값이 포함됩니다.
    uniquebots: Optional
        UniqueBots로 부터 들어온 값이 포함됩니다.
    """
    def __init__(self, koreanbots=None, topgg=None, uniquebots=None):
        super().__init__(koreanbots=koreanbots, topgg=topgg, uniquebots=uniquebots)


class WebsiteStats(WebsiteBase):
    """ 웹사이트로 부터 들어온 봇 상태 정보의 모델을 나타냅니다.

    Attributes
    ------------
    koreanbots: Optional
        koreanbots로 부터 들어온 값이 포함됩니다.
    topgg: Optional
        top.gg로 부터 들어온 값이 포함됩니다.
    uniquebots: Optional
        UniqueBots로 부터 들어온 값이 포함됩니다.
    """
    def __init__(self, koreanbots=None, topgg=None, uniquebots=None):
        super().__init__(koreanbots=koreanbots, topgg=topgg, uniquebots=uniquebots)


class WebsiteVote(WebsiteBase):
    """ 웹사이트로 부터 들어온 사용자 투표 정보에 대한 모델을 나타냅니다.

    Attributes
    ------------
    koreanbots: Optional
        koreanbots로 부터 들어온 값이 포함됩니다.
    topgg: Optional
        top.gg로 부터 들어온 값이 포함됩니다.
    uniquebots: Optional
        UniqueBots로 부터 들어온 값이 포함됩니다.
    """
    def __init__(self, koreanbots=None, topgg=None, uniquebots=None):
        super().__init__(koreanbots=koreanbots, topgg=topgg, uniquebots=uniquebots)


class WebsiteVotes(WebsiteBase):
    """ 웹사이트로 부터 들어온 봇 하트 정보에 대한 모델을 나타냅니다.

    Attributes
    ------------
    topgg: Optional
        top.gg로 부터 들어온 값이 포함됩니다.
    uniquebots: Optional
        UniqueBots로 부터 들어온 값이 포함됩니다.
    """
    def __init__(self, topgg=None, uniquebots=None):
        super().__init__(topgg=topgg, uniquebots=uniquebots)


class WebsiteUser(WebsiteBase):
    """ 웹사이트로 부터 들어온 사용자 정보에 대한 모델을 나타냅니다.

    Attributes
    ------------
    koreanbots: Optional
        koreanbots로 부터 들어온 값이 포함됩니다.
    topgg: Optional
        top.gg로 부터 들어온 값이 포함됩니다.
    uniquebots: Optional
        UniqueBots로 부터 들어온 값이 포함됩니다.
    """
    def __init__(self, koreanbots=None, topgg=None, uniquebots=None):
        super().__init__(koreanbots=koreanbots, topgg=topgg, uniquebots=uniquebots)
