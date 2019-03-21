'''
.. autoclass:: APIError
.. autoclass:: ConnectionError
.. autoclass:: ImpersonationError
.. autoclass:: NotFoundError
.. autoclass:: PackageMissingError
.. autoclass:: PasswordComplexityError
.. autoclass:: RetryError
.. autoclass:: ServerError
.. autoclass:: TenableException
.. autoclass:: TioExportsError
.. autoclass:: UnexpectedValueError
.. autoclass:: UnknownError
.. autoclass:: UnsupportedError
'''
import logging

class TenableException(Exception):
    '''
    Base exception class that sets up logging and handles some basic scaffolding
    for all other exception classes.  This exception should never be directly
    seen.
    '''
    def __init__(self, msg):
        self._log = logging.getLogger('{}.{}'.format(
            self.__module__, self.__class__.__name__))
        self.msg = str(msg)
        self._log.error(self.msg)

    def __str__(self):
        return self.msg

    def __repr__(self):
        return repr(self.__str__())


class FileDownloadError(TenableException):
    '''
    FileDownloadError is thrown when a file fails to download.

    Attributes:
        msg (str):
            The error message
        filename (str):
            The Filename or file id that was requested.
        resource (str):
            The resource that the file was requested from (e.g. "scans")
        resource_id (str):
            The identifier for the resource that was requested.
    '''
    def __init__(self, resource, resource_id, filename):
        self.resource = str(resource)
        self.resource_id = str(resource_id)
        self.filename = str(filename)
        self.msg = 'resource {}:{} requested file {} and has failed.'.format(
            self.resource, self.resource_id, self.filename)


class UnexpectedValueError(TenableException):
    '''
    An unexpected value error is thrown whenever the value specified for a
    parameter is outside the bounds of what is expected.  For example, if the
    parameter **a** is expected to have a value of 1, 2, or 3, and it is instead
    passed a value of 0, then it is an unexpected value, and this Exception
    should be thrown by the package.
    '''
    pass


class ConnectionError(TenableException):
    '''
    A connection-error is thrown only for products like Tenable.sc or Nessus,
    where the application may be installed anywhere.  This error is thrown if
    we are unable to complete the initial connection or gather the basic
    information about the application that is necessary.
    '''
    pass


class PackageMissingError(TenableException):
    '''
    In situations where an optional library is needed, this exception will be
    thrown if the optional library is needed, however is unavailable.
    '''
    pass


class TioExportsError(TenableException):
    '''
    When the exports APIs throw an error when processing an export, pyTenable
    will throw this error in turn to relay that context to the user.
    '''
    def __init__(self, export, uuid):
        self.export = export
        self.uuid = uuid
        TenableException.__init__(self, '{} export {} has errored.'.format(
            export, uuid))


class APIError(TenableException):
    '''
    The APIError Exception is a generic Exception for handling responses from
    the API that aren't whats expected.  The APIError Exception itself attempts
    to provide the developer with enough information around the response to
    ascertain what went wrong.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
        uuid (str):
            The Request UUID of the request.  This can be used for the purpose
            of tracking the request and the response through the Tenable.io
            infrastructure.  In the case of Non-Tenable.io products, is simply
            an empty string.
    '''
    uuid = None
    
    def __init__(self, r):
        self.response = r
        self.code = r.status_code

        if 'X-Request-Uuid' in r.headers:
            self.uuid = r.headers['X-Request-Uuid']

        TenableException.__init__(self, '{} {} >> {}'.format(
            self.response.request.method,
            self.response.request.url,
            self.__str__()))

    def __str__(self):
        return '{}:{} {}'.format(
            str(self.uuid),
            str(self.code),
            str(self.response.text))


class RetryError(APIError):
    '''
    A RetryError is thrown when too many retry attempts have been made.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
        uuid (str):
            The Request UUID of the request.  This can be used for the purpose
            of tracking the request and the response through the Tenable.io
            infrastructure.  In the case of Non-Tenable.io products, is simply
            an empty string.
        attempts (int):
            The number of attempts that were made before bailing.    
    '''
    attempts = 0
    
    def __init__(self, r, attempts):
        self.attempts = attempts
        APIError.__init__(self, r)

    def __str__(self):
        return '{} attempts made, last returned {}:{} {}'.format(
            str(self.attempts),
            str(self.uuid),
            str(self.code),
            str(self.response.text))


class InvalidInputError(APIError):
    '''
    A InvalidInputError is thrown if there is either incomplete or invalid
    information passed to the API.  The HTTP response code generally associated
    to this Exception is 400.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
        uuid (str):
            The Request UUID of the request.  This can be used for the purpose
            of tracking the request and the response through the Tenable.io
            infrastructure.  In the case of Non-Tenable.io products, is simply
            an empty string.
    '''
    pass


class PermissionError(APIError):
    '''
    A PermissionError Exception is thrown when the request cannot be completed
    because the user performing the request doesn't have sufficient permissions
    to complete the task.  The HTTP response code generally associated to this
    Exception is 403.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
        uuid (str):
            The Request UUID of the request.  This can be used for the purpose
            of tracking the request and the response through the Tenable.io
            infrastructure.  In the case of Non-Tenable.io products, is simply
            an empty string.
    '''
    pass


class NotFoundError(APIError):
    '''
    A NotFoundError Exception is thrown when the requested object either
    doesn't exist, or cannot be retrieved.  The HTTP response code generally
    associated to this Exception is 404.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
        uuid (str):
            The Request UUID of the request.  This can be used for the purpose
            of tracking the request and the response through the Tenable.io
            infrastructure.  In the case of Non-Tenable.io products, is simply
            an empty string.
    '''
    pass


class ServerError(APIError):
    '''
    A ServerError is thrown when the HTTP request cannot be completed due to a
    server-side issue.  The HTTP response code generally associated to this
    Exception is 500.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
        uuid (str):
            The Request UUID of the request.  This can be used for the purpose
            of tracking the request and the response through the Tenable.io
            infrastructure.  In the case of Non-Tenable.io products, is simply
            an empty string.
    '''
    pass


class ImpersonationError(APIError):
    '''
    An ImpersonationError exists when there is an issue with user impersonation.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
        uuid (str):
            The Request UUID of the request.  This can be used for the purpose
            of tracking the request and the response through the Tenable.io
            infrastructure.  In the case of Non-Tenable.io products, is simply
            an empty string.
    '''
    pass


class PasswordComplexityError(APIError):
    '''
    PasswordComplexityError is thrown when attempting to change a password and
    the password complexity is insufficient.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
        uuid (str):
            The Request UUID of the request.  This can be used for the purpose
            of tracking the request and the response through the Tenable.io
            infrastructure.  In the case of Non-Tenable.io products, is simply
            an empty string.
    '''
    pass


class UnsupportedError(APIError):
    '''
    UnsupportedError is thrown when an unsupported call is thrown.  The HTTP
    response code generally associated to this Exception is 409.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
        uuid (str):
            The Request UUID of the request.  This can be used for the purpose
            of tracking the request and the response through the Tenable.io
            infrastructure.  In the case of Non-Tenable.io products, is simply
            an empty string.
    '''
    pass


class UnknownError(APIError):
    '''
    If the package is unable to determine what categorization the Exception
    should fall under, it will fall back to this Exception type.  We should
    generally not see UnknownError be thrown.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
        uuid (str):
            The Request UUID of the request.  This can be used for the purpose
            of tracking the request and the response through the Tenable.io
            infrastructure.  In the case of Non-Tenable.io products, is simply
            an empty string.
    '''
    pass