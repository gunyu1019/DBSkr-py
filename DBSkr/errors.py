class ClientException(Exception):
    pass


class InvalidArgument(ClientException):
    pass


class HTTPException(Exception):
    pass


class BadRequests(HTTPException):
    pass


class Unauthorized(HTTPException):
    pass


class Forbidden(HTTPException):
    pass


class NotFound(HTTPException):
    pass


class MethodNotAllowed(HTTPException, Me):
    pass


class TooManyRequests(HTTPException):
    pass