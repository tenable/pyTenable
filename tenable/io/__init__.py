'''
.. autoclass:: TenableIO

.. automodule:: tenable.io.access_groups
.. automodule:: tenable.io.access_groups_v2
.. automodule:: tenable.io.agent_config
.. automodule:: tenable.io.agent_exclusions
.. automodule:: tenable.io.agent_groups
.. automodule:: tenable.io.agents
.. automodule:: tenable.io.assets
.. automodule:: tenable.io.audit_log
.. automodule:: tenable.io.credentials
.. automodule:: tenable.io.editor
.. automodule:: tenable.io.exclusions
.. automodule:: tenable.io.exports
.. automodule:: tenable.io.files
.. automodule:: tenable.io.filters
.. automodule:: tenable.io.folders
.. automodule:: tenable.io.groups
.. automodule:: tenable.io.networks
.. automodule:: tenable.io.permissions
.. automodule:: tenable.io.plugins
.. automodule:: tenable.io.policies
.. automodule:: tenable.io.scanner_groups
.. automodule:: tenable.io.scanners
.. automodule:: tenable.io.scans
.. automodule:: tenable.io.server
.. automodule:: tenable.io.session
.. automodule:: tenable.io.tags
.. automodule:: tenable.io.target_groups
.. automodule:: tenable.io.users
.. automodule:: tenable.io.workbenches

Raw HTTP Calls
==============

Even though the ``TenableIO`` object pythonizes the Tenable.io API for you,
there may still bee the occasional need to make raw HTTP calls to the IO API.
The methods listed below aren't run through any naturalization by the library
aside from the response code checking.  These methods effectively route
directly into the requests session.  The responses will be Response objects from
the ``requests`` library.  In all cases, the path is appended to the base
``url`` parameter that the ``TenableIO`` object was instantiated with.

Example:

.. code-block:: python

   resp = tio.get('scans')

.. py:module:: tenable.io
.. rst-class:: hide-signature
.. py:class:: TenableIO

    .. automethod:: get
    .. automethod:: post
    .. automethod:: put
    .. automethod:: delete
'''
import logging, os
from tenable.errors import UnexpectedValueError
from tenable.base.v1 import APISession
from .access_groups import AccessGroupsAPI
from .access_groups_v2 import AccessGroupsV2API
from .agent_config import AgentConfigAPI
from .agent_exclusions import AgentExclusionsAPI
from .agent_groups import AgentGroupsAPI
from .agents import AgentsAPI
from .assets import AssetsAPI
from .audit_log import AuditLogAPI
from .credentials import CredentialsAPI
from .editor import EditorAPI
from .exclusions import ExclusionsAPI
from .exports import ExportsAPI
from .files import FileAPI
from .filters import FiltersAPI
from .folders import FoldersAPI
from .groups import GroupsAPI
from .networks import NetworksAPI
from .permissions import PermissionsAPI
from .plugins import PluginsAPI
from .policies import PoliciesAPI
from .scanner_groups import ScannerGroupsAPI
from .scanners import ScannersAPI
from .scans import ScansAPI
from .server import ServerAPI
from .session import SessionAPI
from .tags import TagsAPI
from .target_groups import TargetGroupsAPI
from .users import UsersAPI
from .workbenches import WorkbenchesAPI


class TenableIO(APISession):
    '''
    The Tenable.io object is the primary interaction point for users to
    interface with Tenable.io via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        access_key (str, optional):
            The user's API access key for Tenable.io  If an access key isn't
            specified, then the library will attempt to read the environment
            variable ``TIO_ACCESS_KEY`` to acquire the key.
        secret_key (str, optional):
            The user's API secret key for Tenable.io  If a secret key isn't
            specified, then the library will attempt to read the environment
            variable ``TIO_SECRET_KEY`` to acquire the key.
        url (str, optional):
            The base URL that the paths will be appended onto.  The default
            is ``https://cloud.tenable.com``
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``5``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``1`` second.
        vendor (str, optional):
            The vendor name for the User-Agent string.
        product (str, optional):
            The product name for the User-Agent string.
        build (str, optional):
            The version or build identifier for the User-Agent string.
        timeout (int, optional):
            The connection timeout parameter informing the library how long to
            wait in seconds for a stalled response before terminating the
            connection.  If unspecified, the default is 120 seconds.

    Examples:
        Basic Example:

        >>> from tenable.io import TenableIO
        >>> tio = TenableIO('ACCESS_KEY', 'SECRET_KEY')

        Example with proper identification:

        >>> tio = TenableIO('ACCESS_KEY', 'SECRET_KEY',
        >>>     vendor='Company Name',
        >>>     product='My Awesome Widget',
        >>>     build='1.0.0')

        Example with proper identification leveraging environment variables for
        access and secret keys:

        >>> tio = TenableIO(
        >>>     vendor='Company Name', product='Widget', build='1.0.0')
    '''

    _tzcache = None
    _url = 'https://cloud.tenable.com'
    _timeout = 120

    @property
    def access_groups(self):
        return AccessGroupsAPI(self)

    @property
    def access_groups_v2(self):
        return AccessGroupsV2API(self)

    @property
    def agent_config(self):
        return AgentConfigAPI(self)

    @property
    def agent_groups(self):
        return AgentGroupsAPI(self)

    @property
    def agent_exclusions(self):
        return AgentExclusionsAPI(self)

    @property
    def agents(self):
        return AgentsAPI(self)

    @property
    def assets(self):
        return AssetsAPI(self)

    @property
    def audit_log(self):
        return AuditLogAPI(self)

    @property
    def credentials(self):
        return CredentialsAPI(self)

    @property
    def editor(self):
        return EditorAPI(self)

    @property
    def exclusions(self):
        return ExclusionsAPI(self)

    @property
    def exports(self):
        return ExportsAPI(self)

    @property
    def files(self):
        return FileAPI(self)

    @property
    def filters(self):
        return FiltersAPI(self)

    @property
    def folders(self):
        return FoldersAPI(self)

    @property
    def groups(self):
        return GroupsAPI(self)

    @property
    def networks(self):
        return NetworksAPI(self)

    @property
    def permissions(self):
        return PermissionsAPI(self)

    @property
    def plugins(self):
        return PluginsAPI(self)

    @property
    def policies(self):
        return PoliciesAPI(self)

    @property
    def scanner_groups(self):
        return ScannerGroupsAPI(self)

    @property
    def scanners(self):
        return ScannersAPI(self)

    @property
    def scans(self):
        return ScansAPI(self)

    @property
    def server(self):
        return ServerAPI(self)

    @property
    def session(self):
        return SessionAPI(self)

    @property
    def tags(self):
        return TagsAPI(self)

    @property
    def target_groups(self):
        return TargetGroupsAPI(self)

    @property
    def users(self):
        return UsersAPI(self)

    @property
    def workbenches(self):
        return WorkbenchesAPI(self)

    @property
    def _tz(self):
        '''
        As we will be using the timezone listing in a lot of parameter checking,
        we should probably cache the response as a private attribute to speed
        up checking times.
        '''
        if not self._tzcache:
            self._tzcache = self.scans.timezones()
        return self._tzcache

    def __init__(self, access_key=None, secret_key=None, url=None, retries=None,
                 backoff=None, ua_identity=None, session=None, proxies=None,
                 vendor=None, product=None, build=None, timeout=None, ssl_verify=None):
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

        super(TenableIO, self).__init__(url,
            retries=retries,
            backoff=backoff,
            ua_identity=ua_identity,
            session=session,
            proxies=proxies,
            vendor=vendor,
            product=product,
            build=build,
            timeout=timeout,
            ssl_verify=ssl_verify
        )

    def _retry_request(self, response, retries, kwargs):
        '''
        If the call is retried, we will need to set some additional headers
        '''
        if 'headers' not in kwargs:
            kwargs['headers'] = dict()

        if 'X-Request-Uuid' in response.headers:
            # if the request uuid exists in the response, then we will sent the
            # uuid back so that there is solid requesty chain in any subsiquent
            # logs.
            kwargs['headers']['X-Tio-Last-Request-Uuid'] = response.headers['X-Request-Uuid']

        # We also need to return the number of times that we have attempted to
        # retry this call.
        kwargs['headers']['X-Tio-Retry-Count'] = str(retries)
        return kwargs


    def _build_session(self, session=None):
        '''
        Build the session and add the API Keys into the session
        '''
        super(TenableIO, self)._build_session(session)
        self._session.headers.update({
            'X-APIKeys': 'accessKey={}; secretKey={};'.format(
                self._access_key, self._secret_key)
        })
