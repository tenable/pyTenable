'''
.. autoclass:: AuthenticationWarning
.. autoclass:: FileDownloadError
.. autoclass:: ImpersonationError
.. autoclass:: PasswordComplexityError
.. autoclass:: TioExportsError
.. autoclass:: TioExportsTimeout
'''
from typing import Optional
from restfly.errors import *


class AuthenticationWarning(Warning):  # noqa: PLW0622
    '''
    An authentication warning is thrown when an unauthenticated API session is
    initiated.
    '''


class FileDownloadError(RestflyException):
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

    def __init__(self, resource: str, resource_id: str, filename: str):
        self.resource = str(resource)
        self.resource_id = str(resource_id)
        self.filename = str(filename)
        self.msg = (f'resource {resource}:{resource_id} '
                    f'requested file {filename} and has failed.'
                    )


class TioExportsError(RestflyException):
    '''
    When the exports APIs throw an error when processing an export, pyTenable
    will throw this error in turn to relay that context to the user.
    '''

    def __init__(self, export: str, uuid: str, msg: Optional[str] = None):
        self.export = export
        self.uuid = uuid
        if not msg:
            msg = f'{export} export {uuid} has errored.'
        self.msg = msg
        super().__init__(msg)


class TioExportsTimeout(TioExportsError):
    '''
    When an export has been cancelled due to timeout, this error is thrown.
    '''

    def __init__(self, export: str, uuid: str, msg: Optional[str] = None):
        msg = f'{export} export {uuid} has timed out.'
        super().__init__(export, uuid, msg)


class ImpersonationError(APIError):
    '''
    An ImpersonationError exists when there is an issue with user
    impersonation.

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
