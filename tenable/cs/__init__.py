'''
.. autoclass:: ContainerSecurity
.. automodule:: tenable.cs.images
.. automodule:: tenable.cs.reports
.. automodule:: tenable.cs.repositories
.. automodule:: tenable.cs.uploads
.. automodule:: tenable.cs.usage

Raw HTTP Calls
==============

Even though the ``ContainerSecurity`` object pythonizes the Container
Security API for you, there may still bee the occasional need to make raw HTTP
calls to the Container Security API.  The methods listed below aren't run
through any naturalization by the library aside from the response code checking.
These methods effectively route directly into the requests session.  The
responses will be Response objects from the ``requests`` library.  In all cases,
the path is appended to the base ``url`` paramater that the
``ContainerSecurity`` object was instantiated with.

Example:

.. code-block:: python

   resp = cs.get('repositories')

.. py:module:: tenable.cs
.. rst-class:: hide-signature
.. autoclass:: ContainerSecurity

    .. automethod:: get
    .. automethod:: post
    .. automethod:: put
    .. automethod:: delete
'''
from tenable.base import APISession
from tenable.errors import UnexpectedValueError
from .images import ImageAPI
from .reports import ReportAPI
from .repositories import RepositoryAPI
from .uploads import UploadAPI
from .usage import UsageAPI

class ContainerSecurity(APISession):
    '''
    The Container Security object is the primary interaction point for users to
    interface with Container Security via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        access_key (str):
            The user's API access key for Tenable.io.
        secret_key (str):
            The user's API secret key for Tenable.io.
        url (str, optional):
            The base URL that the paths will be appended onto.  The default
            is ``https://cloud.tenable.com``.
        registry (str, optional):
            The registry path to use for docker pushes.  The default is
            ``registry.cloud.tenable.com``.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``3``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``0.1`` seconds.
    '''
    _url = 'https://cloud.tenable.com/container-security/api/v2'
    _registry = 'registry.cloud.tenable.com'

    @property
    def images(self):
        return ImageAPI(self)

    @property
    def repositories(self):
        return RepositoryAPI(self)

    @property
    def reports(self):
        return ReportAPI(self)

    @property
    def uploads(self):
        return UploadAPI(self)

    @property
    def usage(self):
        return UsageAPI(self)

    def __init__(self, access_key=None, secret_key=None, registry=None,
                 url=None, retries=None, backoff=None, ua_identity=None,
                 session=None, proxies=None, vendor=None, product=None,
                 build=None):
        if access_key:
            self._access_key = access_key
        else:
            self._access_key = os.getenv('TIO_ACCESS_KEY')

        if secret_key:
            self._secret_key = secret_key
        else:
            self._secret_key = os.getenv('TIO_SECRET_KEY')

        if not self._access_key or not self._secret_key:
            raise UnexpectedValueError('No valid API Keypair Defined')

        if registry:
            self._registry = registry

        super(ContainerSecurity, self).__init__(url,
            retries=retries,
            backoff=backoff,
            ua_identity=ua_identity,
            session=session,
            proxies=proxies,
            vendor=vendor,
            product=product,
            build=build)

    def _build_session(self, session=None):
        '''
        Build the session and add the API Keys into the session
        '''
        super(ContainerSecurity, self)._build_session(session)
        self._session.headers.update({
            'X-APIKeys': 'accessKey={}; secretKey={};'.format(
                self._access_key, self._secret_key)
        })
