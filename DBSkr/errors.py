class DBSkrException(Exception):
    """DBSkr의 기본 예외 클래스 입니다."""
    pass


class ClientException(DBSkrException):
    """Client 값에서 값이 잘못 설정되었을 때 발생하는 예외 클래스 입니다."""
    pass


class InvalidArgument(ClientException):
    """Argument 값이 잘못 설정되었을 때 발생하는 예외 클래스 입니다."""
    pass


class HTTPException(DBSkrException):
    """
    HttpClient의 대표 예외 클래스 입니다.
    DBSkr에 속한 모든 HttpClient가 핸들러 됩니다.
    """
    pass


class BadRequests(HTTPException):
    """Bad Requests (400):
     잘못된 피라미터가 입력되었을 경우에 발생하는 예외클래스 입니다.
    """
    pass


class Unauthorized(HTTPException):
    """Unauthorized (401):
     Token 값이 누락되거나, 알맞지 않을 때 발생하는 예외 클래스 입니다.
    """
    pass


class Forbidden(HTTPException):
    """Forbidden (403):
     권한이 없을 때 발생되는 예외 클래스입니다.
    """
    pass


class NotFound(HTTPException):
    """Not Found(404):
     값을 찾을 수 없을 때 발생하는 예외 클래스입니다.
    """
    pass


class MethodNotAllowed(HTTPException):
    """Method Not Allowed(405):
     Method가 허용되지 않았을 때 발생하는 예외 클래스 입니다.
    """
    pass


class TooManyRequests(HTTPException):
    """Too Many Requests(429):
     서버에서 너무 많은 요청을 했을 때 발생하는 예외 클래스 입니다.
    """
    pass
