class ClientException(Exception):
    pass


class HTTPException(Exception):
    def __init__(self, response, message):
        self.status = response.status
        if isinstance(message, dict):
            self.status = message.get('code', self.status)
            self.error = message.get('message', 'Exception')
        else:
            self.error = message
        super().__init__(f"{self.status} {self.error}")


class BadRequests(HTTPException):
    pass


class Unauthorized(HTTPException):
    pass


class Forbidden(HTTPException):
    pass


class NotFound(HTTPException):
    pass


class MethodNotAllowed(HTTPException):
    pass


class TooManyRequests(HTTPException):
    pass
