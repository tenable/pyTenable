'''

.. note::
    Please refer to the common themes section for TenableSC for details on how
    these methods are written from an overall concept.  Not all attributes are
    explicitly documented, only the ones that pyTenable is augmenting,
    validating, or modifying.  For a complete listing of the attributes that can
    be passed to most APIs, refer to the official API documentation that each
    method calls, which is conveniently linked in each method's docs.

.. autoclass:: TenableSC

    .. automethod:: login
    .. automethod:: logout

.. automodule:: tenable.sc.alerts
.. automodule:: tenable.sc.accept_risks
.. automodule:: tenable.sc.analysis
.. automodule:: tenable.sc.asset_lists
.. automodule:: tenable.sc.audit_files
.. automodule:: tenable.sc.credentials
.. automodule:: tenable.sc.current
.. automodule:: tenable.sc.feeds
.. automodule:: tenable.sc.files
.. automodule:: tenable.sc.groups
.. automodule:: tenable.sc.organizations
.. automodule:: tenable.sc.plugins
.. automodule:: tenable.sc.policies
.. automodule:: tenable.sc.queries
.. automodule:: tenable.sc.repositories
.. automodule:: tenable.sc.roles
.. automodule:: tenable.sc.scan_zones
.. automodule:: tenable.sc.scans
.. automodule:: tenable.sc.scan_instances
.. automodule:: tenable.sc.scanners
.. automodule:: tenable.sc.status
.. automodule:: tenable.sc.system
.. automodule:: tenable.sc.users
.. automodule:: tenable.sc.base


Raw HTTP Calls
==============

Even though the ``TenableSC`` object pythonizes the Tenable.sc API for
you, there may still bee the occasional need to make raw HTTP calls to the
Tenable.sc API.  The methods listed below aren't run through any
naturalization by the library aside from the response code checking.  These
methods effectively route directly into the requests session.  The responses
will be Response objects from the ``requests`` library.  In all cases, the path
is appended to the base ``url`` parameter that the ``TenableSC`` object was
instantiated with.

Example:

.. code-block:: python

   resp = sc.get('feed')

.. py:module:: tenable.sc
.. rst-class:: hide-signature
.. py:class:: TenableSC

    .. automethod:: get
    .. automethod:: post
    .. automethod:: put
    .. automethod:: delete
'''
from tenable.base.v1 import APISession
from tenable.errors import *
from .accept_risks import AcceptRiskAPI
from .alerts import AlertAPI
from .analysis import AnalysisAPI
from .asset_lists import AssetListAPI
from .audit_files import AuditFileAPI
from .credentials import CredentialAPI
from .current import CurrentSessionAPI
from .files import FileAPI
from .feeds import FeedAPI
from .groups import GroupAPI
from .organizations import OrganizationAPI
from .plugins import PluginAPI
from .policies import ScanPolicyAPI
from .queries import QueryAPI
from .recast_risks import RecastRiskAPI
from .repositories import RepositoryAPI
from .roles import RoleAPI
from .scanners import ScannerAPI
from .scans import ScanAPI
from .scan_instances import ScanResultAPI
from .scan_zones import ScanZoneAPI
from .status import StatusAPI
from .system import SystemAPI
from .users import UserAPI
import warnings, logging, semver


class TenableSC(APISession):
    '''TenableSC API Wrapper
    The Tenable.sc object is the primary interaction point for users to
    interface with Tenable.sc via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        host (str):
            The address of the Tenable.sc instance to connect to.
        access_key (str, optional):
            The API access key to use for sessionless authentication.
        adapter (requests.Adaptor, optional):
            If a requests session adaptor is needed to ensure connectivity
            to the Tenable.sc host, one can be provided here.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``1`` second.
        cert (tuple, optional):
            The client-side SSL certificate to use for authentication.  This
            format could be either a tuple or a string pointing to the
            certificate.  For more details, please refer to the
            `Requests Client-Side Certificates`_ documentation.
        password (str, optional):
            The password to use for session authentication.
        port (int, optional):
            The port number to connect to on the specified host.  The
            default is port ``443``.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``5``.
        scheme (str, optional):
            What HTTP scheme should be used for URI path construction.  The
            default is ``https``.
        secret_key (str, optional):
            The API secret key to use for sessionless authentication.
        session (requests.Session, optional):
            If a requests Session is provided, the provided session will be used
            instead of constructing one during initialization.
        ssl_verify (bool, optional):
            Should the SSL certificate on the Tenable.sc instance be verified?
            Default is False.
        username (str, optional):
            The username to use for session authentication.
        timeout (int, optional):
            The connection timeout parameter informing the library how long to
            wait in seconds for a stalled response before terminating the
            connection.  If unspecified, the default is 300 seconds.


    Examples:
        A direct connection to Tenable.sc:

        >>> from tenable.sc import TenableSC
        >>> sc = TenableSC('sc.company.tld')

        A connection to Tenable.sc using SSL certificates:

        >>> sc = TenableSC('sc.company.tld',
        ...     cert=('/path/client.cert', '/path/client.key'))

        Using an adaptor to use a passworded certificate (via the immensely
        useful `requests_pkcs12`_ adaptor):

        >>> from requests_pkcs12 import Pkcs12Adapter
        >>> adapter = Pkcs12Adapter(
        ...     pkcs12_filename='certificate.p12',
        ...     pkcs12_password='omgwtfbbq!')
        >>> sc = TenableSC('sc.company.tld', adapter=adapter)

        Using API Keys to communicate to Tenable.sc:

        >>> sc = TenableSC('sc.compant.tld', access_key='key', secret_key='key')

        Using context management to handle

    For more information, please See Tenable's `SC API documentation`_ and
    the `SC API Best Practices Guide`_.

    .. _SC API documentation:
        https://docs.tenable.com/sccv/api/index.html
    .. _SC API Best Practices Guide:
        https://docs.tenable.com/sccv/api_best_practices/Content/ScApiBestPractices/AboutScApiBestPrac.htm
    .. _Requests Client-Side Certificates:
        http://docs.python-requests.org/en/master/user/advanced/#client-side-certificates
    .. _requests_pkcs12:
        https://github.com/m-click/requests_pkcs12
    '''
    _apikeys = False
    _restricted_paths = ['token']
    _timeout = 300
    _error_codes = {
        400: InvalidInputError,
        403: APIError,
        404: NotFoundError,
        500: ServerError,
    }

    def __init__(self, host, access_key=None, secret_key=None, username=None,
                 password=None, port=443, ssl_verify=False, cert=None,
                 adapter=None, scheme='https', retries=None, backoff=None,
                 ua_identity=None, session=None, proxies=None, timeout=None,
                 vendor=None, product=None, build=None, base_path='rest',):
        # As we will always be passing a URL to the APISession class, we will
        # want to construct a URL that APISession (and further requests)
        # understands.
        base = '{}://{}:{}'.format(scheme, host, port)
        url = '{}/{}'.format(base, base_path)

        # Setting the SSL Verification flag on the object itself so that it's
        # reusable if the user logs out and logs back in.
        self._ssl_verify = ssl_verify

        # Now lets pass the relevant parts off to the APISession's constructor
        # to make sure we have everything lined up as we expect.
        super(TenableSC, self).__init__(url,
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

        # If a client-side certificate is specified, then we will want to add
        # it into the session object as well.  The cert parameter is expecting
        # a path pointing to the client certificate file.
        if cert:
            self._session.cert = cert

        # If an adapter for requests was provided, we should pull that in as
        # well.
        if adapter:
            self._session.mount(base, adapter)

        # We will attempt to make the first call to the Tenable.sc instance
        # and get the system information.  If this call fails, then we likely
        # aren't pointing to a SecurityCenter at all and should throw an error
        # stating this.
        try:
            self.info = self.system.details()
        except:
            raise ConnectionError('No Tenable.sc Instance at {}:{}'.format(host, port))

        # Now we will try to interpret the Tenable.sc information into
        # something usable.
        try:
            self.version = self.info['version']
            self.build_id = self.info['buildID']
            self.license = self.info['licenseStatus']
            self.uuid = self.info['uuid']
            if 'token' in self.info:
                # if a token was passed in the system info page, then we should
                # update the X-SecurityCenter header with the token info.
                self._session.headers.update({
                    'X-SecurityCenter': str(self.info['token'])
                })
        except:
            raise ConnectionError('Invalid Tenable.sc Instance')

        # Now we will attempt to authenticate to the API using any auth settings
        # passed into the constructor.
        self.login(
            username=username,
            password=password,
            access_key=access_key,
            secret_key=secret_key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.logout()

    def _resp_error_check(self, response, **kwargs):
        if not kwargs.get('stream', False):
            try:
                d = response.json()
                if d['error_code']:
                    raise APIError(response)
            except ValueError:
                pass
        return response

    def login(self, username=None, password=None,
              access_key=None, secret_key=None):
        '''
        Logs the user into Tenable.sc

        Args:
            username (str, optional): Username
            password (str, optional): Password
            access_key (str, optional): API Access Key
            secret_key (str, optional): API Secret Key

        Returns:
            None

        Examples:

            Using a username && password:

            >>> sc = TenableSC('127.0.0.1', port=8443)
            >>> sc.login('username', 'password')

            Using API Keys:

            >>> sc = TenableSC('127.0.0.1', port=8443)
            >>> sc.login(access_key='ACCESSKEY', secret_key='SECRETKEY')
        '''

        if username != None and password != None:
            resp = self.post('token', json={
                'username': username,
                'password': password
            })
            self._session.headers.update({
                'X-SecurityCenter': str(resp.json()['response']['token'])
            })

        elif access_key != None and secret_key != None:
            if semver.VersionInfo.parse(self.version).match('<5.13.0'):
                raise ConnectionError(
                    'API Keys not supported on this version of Tenable.sc')
            self._session.headers.update({
                'X-APIKey': 'accessKey={}; secretKey={}'.format(
                    access_key, secret_key)
            })
            self._apikeys = True

    def logout(self):
        '''
        Logs out of Tenable.sc and resets the session.

        Returns:
            None

        Examples:
            >>> sc.logout()
        '''
        if not self._apikeys:
            resp = self.delete('token')
        self._build_session()
        self._apikeys = False

    @property
    def accept_risks(self):
        return AcceptRiskAPI(self)

    @property
    def alerts(self):
        return AlertAPI(self)

    @property
    def analysis(self):
        return AnalysisAPI(self)

    @property
    def asset_lists(self):
        return AssetListAPI(self)

    @property
    def audit_files(self):
        return AuditFileAPI(self)

    @property
    def credentials(self):
        return CredentialAPI(self)

    @property
    def current(self):
        return CurrentSessionAPI(self)

    @property
    def feeds(self):
        return FeedAPI(self)

    @property
    def files(self):
        return FileAPI(self)

    @property
    def groups(self):
        return GroupAPI(self)

    @property
    def organizations(self):
        return OrganizationAPI(self)

    @property
    def plugins(self):
        return PluginAPI(self)

    @property
    def policies(self):
        return ScanPolicyAPI(self)

    @property
    def queries(self):
        return QueryAPI(self)

    @property
    def recast_risks(self):
        return RecastRiskAPI(self)

    @property
    def repositories(self):
        return RepositoryAPI(self)

    @property
    def roles(self):
        return RoleAPI(self)

    @property
    def scanners(self):
        return ScannerAPI(self)

    @property
    def scans(self):
        return ScanAPI(self)

    @property
    def scan_instances(self):
        return ScanResultAPI(self)

    @property
    def scan_zones(self):
        return ScanZoneAPI(self)

    @property
    def status(self):
        return StatusAPI(self)

    @property
    def system(self):
        return SystemAPI(self)

    @property
    def users(self):
        return UserAPI(self)
