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
    def __init__(self, koreanbots=None, topgg=None, uniquebots=None):
        super().__init__(koreanbots=koreanbots, topgg=topgg, uniquebots=uniquebots)


class WebsiteStats(WebsiteBase):
    def __init__(self, koreanbots=None, topgg=None, uniquebots=None):
        super().__init__(koreanbots=koreanbots, topgg=topgg, uniquebots=uniquebots)


class WebsiteVote(WebsiteBase):
    def __init__(self, koreanbots=None, topgg=None, uniquebots=None):
        super().__init__(koreanbots=koreanbots, topgg=topgg, uniquebots=uniquebots)


class WebsiteVotes(WebsiteBase):
    def __init__(self, topgg=None, uniquebots=None):
        super().__init__(topgg=topgg, uniquebots=uniquebots)


class WebsiteUser(WebsiteBase):
    def __init__(self, koreanbots=None, topgg=None, uniquebots=None):
        super().__init__(koreanbots=koreanbots, topgg=topgg, uniquebots=uniquebots)