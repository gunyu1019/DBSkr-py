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
from .. import errors


class ClientException(Exception):
    """ Client 값에서 값이 잘못 설정되었을 때 발생하는 예외 클래스 입니다."""
    pass


class HTTPException(errors.HTTPException):
    """
    koreanbots.HttpClient의 대표 예외 클래스 입니다.
    KoreanBots에 속한 모든 HttpClient가 핸들러 됩니다.
    """
    def __init__(self, response, message):
        self.status = response.status
        if isinstance(message, dict):
            self.status = message.get('code', self.status)
            self.error = message.get('message', 'Exception')
        else:
            self.error = message
        super().__init__(f"{self.status} {self.error}")


class BadRequests(HTTPException, errors.BadRequests):
    """ Bad Requests (400):
     잘못된 피라미터가 입력되었을 경우에 발생하는 예외클래스 입니다.
    """
    pass


class Unauthorized(HTTPException, errors.Unauthorized):
    """ Unauthorized (401):
     Token 값이 누락되거나, 알맞지 않을 때 발생하는 예외 클래스 입니다.
    """
    pass


class Forbidden(HTTPException, errors.Forbidden):
    """ Forbidden (403):
     권한이 없을 때 발생되는 예외 클래스입니다.
    """
    pass


class NotFound(HTTPException, errors.NotFound):
    """ Not Found(404):
     값을 찾을 수 없을 때 발생하는 예외 클래스입니다.
    """
    pass


class MethodNotAllowed(HTTPException, errors.MethodNotAllowed):
    """ Method Not Allowed(405):
     Method가 허용되지 않았을 때 발생하는 예외 클래스 입니다.
    """
    pass


class TooManyRequests(HTTPException, errors.TooManyRequests):
    """ Too Many Requests(429):
     서버에서 너무 많은 요청을 했을 때 발생하는 예외 클래스 입니다.
    """
    pass
