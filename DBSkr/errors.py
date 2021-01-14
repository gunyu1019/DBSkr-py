class DBSException(Exception):
    """DBSkr의 기본 예외 클래스입니다."""
    pass

class HTTPException(DBSException):
    """.HTTPClient의 기본 예외 클래스입니다."""
    def __init__(self, response, message):
        self.response = response
        if isinstance(message, dict):
            self.text = message.get('message','')
            self.code = message.get('code', 0)
        else:
            self.text = message

        if self.text != '':
            super().__init__(f"{response.reason} (상태코드: {response.status}): {self.text}")
        else:
            super().__init__(f"{response.reason} (상태코드: {response.status})")

class Unauthorized(HTTPException):
    """잘못된 토큰을 사용했을 떄 발생합니다."""
    pass

class Forbidden(HTTPException):
    """접근 권한이 없을 때 발생합니다."""
    pass

class NotFound(HTTPException):
    """해당 항목을 찾을 수 없을 때 발생합니다."""
    pass
