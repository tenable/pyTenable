"""
.. autoexception:: RestflyException
.. autoexception:: UnexpectedValueError
.. autoexception:: RequiredParameterError
.. autoexception:: APIError
.. autoexception:: BadRequestError
.. autoexception:: UnauthorizedError
.. autoexception:: ForbiddenError
.. autoexception:: NotFoundError
.. autoexception:: InvalidMethodError
.. autoexception:: NotAcceptableError
.. autoexception:: ProxyAuthenticationError
.. autoexception:: RequestTimeoutError
.. autoexception:: RequestConflictError
.. autoexception:: NoLongerExistsError
.. autoexception:: LengthRequiredError
.. autoexception:: PreconditionFailedError
.. autoexception:: PayloadTooLargeError
.. autoexception:: URITooLongError
.. autoexception:: UnsupportedMediaTypeError
.. autoexception:: RangeNotSatisfiableError
.. autoexception:: ExpectationFailedError
.. autoexception:: TeapotResponseError
.. autoexception:: MisdirectRequestError
.. autoexception:: InvalidContentError
.. autoexception:: TooEarlyError
.. autoexception:: UpgradeRequiredError
.. autoexception:: PreconditionRequiredError
.. autoexception:: TooManyRequestsError
.. autoexception:: RequestHeaderFieldsTooLargeError
.. autoexception:: UnavailableForLegalReasonsError
.. autoexception:: ServerError
.. autoexception:: MethodNotImplementedError
.. autoexception:: BadGatewayError
.. autoexception:: ServiceUnavailableError
.. autoexception:: GatewayTimeoutError
.. autoexception:: NotExtendedError
.. autoexception:: NetworkAuthenticationRequiredError
.. autoclass:: AuthenticationWarning
.. autoclass:: FileDownloadError
.. autoclass:: ImpersonationError
.. autoclass:: PasswordComplexityError
.. autoclass:: TioExportsError
.. autoclass:: TioExportsTimeout
"""

import logging
from typing import Optional

from httpx import Response
from restfly import APIError as RestflyAPIError


class TenableCloudAPIError(RestflyAPIError):
    request_uuid: str
    """
    Request UUID for the API Request. Used by Tenable to track the request through the
    various services it may traverse.
    """

    def __init__(self, response: Response, template: str):
        self.request_uuid = response.headers.get('Request-UUID')
        super().__init__(response=response, template=template)


def api_error_func(resp, **kwargs):  # noqa: PLW0613
    """
    Default message function for APIErrors

    Args:
        resp (request.Response):
            The HTTP response that caused the error to be thrown.
        **kwargs (dict):
            The keyword argument dictionary from the APIError

    Returns:
        :obj:`str`:
            The string message for the error.
    """
    return (
        f'[{str(resp.status_code)}: {str(resp.request.method)}] '
        f'{str(resp.request.url)} body={str(resp.content)}'
    )


def base_msg_func(msg, **kwargs):  # noqa: PLW0613
    """
    Default function used for RestflyException

    Args:
        msg (str):
            The message string to be returned
        **kwargs (dict):
            The keyword argument dictionary from the RestflyException

    Returns:
        :obj:`str`:
            The string message
    """
    return str(msg)


class RestflyException(Exception):
    """
    Base exception class that sets up logging and handles some basic
    scaffolding for all other exception classes.  This exception should never
    be directly seen.
    """

    def __init__(self, msg, **kwargs):
        self._log = logging.getLogger(f'{self.__module__}.{self.__class__.__name__}')
        self.msg = kwargs.get('func', base_msg_func)(msg, **kwargs)
        self._log.error(self.__str__())
        super().__init__()

    def __str__(self):
        return str(self.msg)

    def __repr__(self):
        return repr(self.__str__())


class UnexpectedValueError(RestflyException):
    """
    An unexpected value error is thrown whenever the value specified for a
    parameter is outside the bounds of what is expected.  For example, if the
    parameter **a** is expected to have a value of 1, 2, or 3, and it is
    instead passed a value of 0, then it is an unexpected value, and this
    Exception should be thrown by the package.
    """


class RequiredParameterError(RestflyException):
    """
    A Required Parameter error is thrown whenever the value specified for a
    parameter is required to have a value other than `None`.
    """


class ConnectionError(RestflyException):  # noqa: PLW0622
    """
    A connection-error is thrown only for products like Tenable.sc or Nessus,
    where the application may be installed anywhere.  This error is thrown if
    we are unable to complete the initial connection or gather the basic
    information about the application that is necessary.
    """


class AuthenticationWarning(Warning):  # noqa: PLW0622
    """
    An authentication warning is thrown when an unauthenticated API session is
    initiated.
    """


class PackageMissingError(RestflyException):
    """
    In situations where an optional library is needed, this exception will be
    thrown if the optional library is needed, however is unavailable.
    """


class NotImplementedError(RestflyException):  # noqa: PLW0622
    """
    In situations where something is stubbed out or otherwise not yet
    implemented, this error can be thrown back to inform the user that the
    requesting method, class, etc. is not yet developed.
    """


# The following Exception codes have been written using the following link as
# a baseline:  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


class APIError(RestflyException):
    """
    The APIError Exception is a generic Exception for handling responses from
    the API that aren't whats expected.  The APIError Exception itself attempts
    to provide the developer with enough information around the response to
    ascertain what went wrong.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """

    retryable = False
    retries = None

    def __init__(self, resp, **kwargs):
        kwargs['func'] = kwargs.get('func', api_error_func)
        self.response = resp
        self.code = resp.status_code
        self.retries = kwargs.get('retries')
        super().__init__(resp, **kwargs)

    @classmethod
    def set_retryable(cls, value: bool) -> None:
        """
        Sets the retry flag for the given response code.
        """
        cls.retryable = value


class BadRequestError(APIError):  # 400 Response
    """
    The server cannot or will not process the request due to an apparent client
    error (e.g., malformed request syntax, size too large, invalid request
    message framing, or deceptive request routing).

    Typically associated with a ``400`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class UnauthorizedError(APIError):  # 401 Response
    """
    Similar to 403 Forbidden, but specifically for use when authentication is
    required and has failed or has not yet been provided. The response must
    include a WWW-Authenticate header field containing a challenge applicable
    to the requested resource. See Basic access authentication and Digest
    access authentication. 401 semantically means "unauthenticated", i.e. the
    user does not have the necessary credentials.

    Typically associated with a ``401`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class ForbiddenError(APIError):  # 403 Response
    """
    The request was valid, but the server is refusing action. The user might
    not have the necessary permissions for a resource, or may need an account
    of some sort.

    Typically associated with a ``403`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class NotFoundError(APIError):  # 404 Response
    """
    The requested resource could not be found but may be available in the
    future. Subsequent requests by the client are permissible.

    Typically associated with a ``404`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class InvalidMethodError(APIError):  # 405 Response
    """
    A request method is not supported for the requested resource; for example,
    a GET request on a form that requires data to be presented via POST, or a
    PUT request on a read-only resource.

    Typically associated with a ``405`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class NotAcceptableError(APIError):  # 406 Response
    """
    The requested resource is only capable of generating content not
    acceptable according to the Accept headers sent in the request.

    Typically associated with a ``406`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class ProxyAuthenticationError(APIError):  # 407 Response
    """
    The client must first authenticate itself with the proxy.

    Typically associated with a ``407`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class RequestTimeoutError(APIError):  # 408 Response
    """
    The client did not produce a request within the time that the server was
    prepared to wait. The client MAY repeat the request without modifications
    at any later time.

    Typically associated with a ``408`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class RequestConflictError(APIError):  # 409 Response
    """
    Indicates that the request could not be processed because of conflict in
    the current state of the resource, such as an edit conflict between
    multiple simultaneous updates.

    Typically associated with a ``409`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class NoLongerExistsError(APIError):  # 410 Response
    """
    Indicates that the resource requested is no longer available and will not
    be available again. This should be used when a resource has been
    intentionally removed and the resource should be purged. Upon receiving a
    410 status code, the client should not request the resource in the future.
    Clients such as search engines should remove the resource from their
    indices. Most use cases do not require clients and search engines to purge
    the resource, and a "404 Not Found" may be used instead.

    Typically associated with a ``410`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class LengthRequiredError(APIError):  # 411 Response
    """
    The request did not specify the length of its content, which is required by
    the requested resource.

    Typically associated with a ``411`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class PreconditionFailedError(APIError):  # 412 Response
    """
    The server does not meet one of the preconditions that the requester put
    on the request.

    Typically associated with a ``412`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class PayloadTooLargeError(APIError):  # 413 Response
    """
    The request is larger than the server is willing or able to process.

    Typically associated with a ``413`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class URITooLongError(APIError):  # 414 Response
    """
    The URI provided was too long for the server to process. Often the result
    of too much data being encoded as a query-string of a GET request, in which
    case it should be converted to a POST request.

    Typically associated with a ``414`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class UnsupportedMediaTypeError(APIError):  # 415 Response
    """
    The request entity has a media type which the server or resource does not
    support. For example, the client uploads an image as image/svg+xml, but the
    server requires that images use a different format.

    Typically associated with a ``415`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class RangeNotSatisfiableError(APIError):  # 416 Response
    """
    The client has asked for a portion of the file (byte serving), but the
    server cannot supply that portion. For example, if the client asked for a
    part of the file that lies beyond the end of the file.

    Typically associated with a ``416`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class ExpectationFailedError(APIError):  # 417 Response
    """
    The server cannot meet the requirements of the Expect request-header field.

    Typically associated with a ``417`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class TeapotResponseError(APIError):  # 418 Response
    """
    This code was defined in 1998 as one of the traditional IETF April Fools'
    jokes, in RFC 2324, Hyper Text Coffee Pot Control Protocol, and is not
    expected to be implemented by actual HTTP servers. The RFC specifies this
    code should be returned by teapots requested to brew coffee.

    Typically associated with a ``418`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class MisdirectRequestError(APIError):  # 421 Response
    """
    The request was directed at a server that is not able to produce a response

    Typically associated with a ``421`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class InvalidContentError(APIError):
    """
    The request contained content that did not match the expected schema or was
    otherwise invalid in some way.

    Typically associated with a ``422`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (requests.Response):
            This is the Response object that had caused the Exception to fire.
    """


class TooEarlyError(APIError):  # 425 Response
    """
    Indicates that the server is unwilling to risk processing a request that
    might be replayed.

    Typically associated with a ``425`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class UpgradeRequiredError(APIError):  # 426 Response
    """
    The client should switch to a different protocol such as TLS/1.0, given in
    the Upgrade header field.

    Typically associated with a ``426`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class PreconditionRequiredError(APIError):  # 428 Response
    """
    The origin server requires the request to be conditional. Intended to
    prevent the 'lost update' problem, where a client GETs a resource's state,
    modifies it, and PUTs it back to the server, when meanwhile a third party
    has modified the state on the server, leading to a conflict.

    Typically associated with a ``428`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class TooManyRequestsError(APIError):  # 420 & 429 Response
    """
    The user has sent too many requests in a given amount of time. Intended for
    use with rate-limiting schemes.

    Typically associated with a ``429`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """

    retryable = True


class RequestHeaderFieldsTooLargeError(APIError):  # 431 Response
    """
    The server is unwilling to process the request because either an individual
    header field, or all the header fields collectively, are too large.

    Typically associated with a ``431`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class UnavailableForLegalReasonsError(APIError):  # 451 Response
    """
    A server operator has received a legal demand to deny access to a resource
    or to a set of resources that includes the requested resource.

    Typically associated with a ``451`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class ServerError(APIError):  # 500 Response
    """
    A generic error message, given when an unexpected condition was encountered
    and no more specific message is suitable.

    Typically associated with a ``500`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class MethodNotImplementedError(APIError):  # 501 Response
    """
    The server either does not recognize the request method, or it lacks the
    ability to fulfill the request. Usually this implies future availability.

    Typically associated with a ``501`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """

    retryable = True


class BadGatewayError(APIError):  # 502 Response
    """
    The server was acting as a gateway or proxy and received an invalid
    response from the upstream server.

    Typically associated with a ``502`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """

    retryable = True


class ServiceUnavailableError(APIError):  # 503 Response
    """
    The server cannot handle the request (because it is overloaded or down for
    maintenance). Generally, this is a temporary state.

    Typically associated with a ``503`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """

    retryable = True


class GatewayTimeoutError(APIError):  # 504 Response
    """
    The server was acting as a gateway or proxy and did not receive a timely
    response from the upstream server.

    Typically associated with a ``504`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """

    retryable = True


class NotExtendedError(APIError):  # 510 Response
    """
    Further extensions to the request are required for the server to fulfill it.

    Typically associated with a ``510`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class NetworkAuthenticationRequiredError(APIError):  # 511 Response
    """
    The client needs to authenticate to gain network access. Intended for use
    by intercepting proxies used to control access to the network

    Typically associated with a ``511`` Status code.

    Attributes:
        code (int):
            The HTTP response code from the offending response.
        response (request.Response):
            This is the Response object that had caused the Exception to fire.
    """


class FileDownloadError(RestflyException):
    """
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
    """

    def __init__(self, resource: str, resource_id: str, filename: str):
        self.resource = str(resource)
        self.resource_id = str(resource_id)
        self.filename = str(filename)
        self.msg = (
            f'resource {resource}:{resource_id} '
            f'requested file {filename} and has failed.'
        )


class TioExportsError(RestflyException):
    """
    When the exports APIs throw an error when processing an export, pyTenable
    will throw this error in turn to relay that context to the user.
    """

    def __init__(self, export: str, uuid: str, msg: Optional[str] = None):
        self.export = export
        self.uuid = uuid
        if not msg:
            msg = f'{export} export {uuid} has errored.'
        self.msg = msg
        super().__init__(msg)


class TioExportsTimeout(TioExportsError):
    """
    When an export has been cancelled due to timeout, this error is thrown.
    """

    def __init__(self, export: str, uuid: str, msg: Optional[str] = None):
        msg = f'{export} export {uuid} has timed out.'
        super().__init__(export, uuid, msg)


class ImpersonationError(APIError):
    """
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
    """


class PasswordComplexityError(APIError):
    """
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
    """
