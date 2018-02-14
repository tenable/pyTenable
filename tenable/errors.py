class UnexpectedValueError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class APIError(Exception):
    def __init__(self, r):
        self.code = r.status_code
        self.body = r.content
        self.uuid = r.headers['X-Request-Uuid'] if 'X-Request-Uuid' in r.headers else ''

    def __str__(self):
        return repr('{}:{} {}'.format(self.uuid, self.code, self.body))


class PermissionError(APIError):
    pass


class NotFoundError(APIError):
    pass


class ServerError(APIError):
    pass


class UnknownError(APIError):
    pass