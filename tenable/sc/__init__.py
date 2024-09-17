'''
Tenable Security Center
=======================

.. note::
    Please refer to the common themes section for TenableSC for details on how
    these methods are written from an overall concept.  Not all attributes are
    explicitly documented, only the ones that pyTenable is augmenting,
    validating, or modifying.  For a complete listing of the attributes that can
    be passed to most APIs, refer to the official API documentation that each
    method calls, which is conveniently linked in each method's docs.

.. autoclass:: TenableSC
   :members:


.. toctree::
    :hidden:
    :glob:

    base
    accept_risks
    alerts
    analysis
    asset_lists
    audit_files
    credentials
    current
    feeds
    files
    groups
    organizations
    plugins
    policies
    queries
    recast_risks
    repositories
    roles
    scan_instances
    scan_zones
    scanners
    scans
    status
    system
    users

'''
import warnings
from typing import Optional
from semver import VersionInfo
import tempfile
import cryptography.hazmat.primitives.serialization.pkcs12
from cryptography.hazmat.primitives import serialization
from tenable.errors import APIError, ConnectionError
from tenable.base.platform import APIPlatform
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


class TenableSC(APIPlatform):  # noqa PLR0904
    '''TenableSC API Wrapper
    The Tenable Security Center object is the primary interaction point for users to
    interface with Tenable Security Center via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        host (str):
            The address of the Tenable Security Center instance to connect to.
            (NOTE: The `host` parameter will be deprecated in favor of the `url`
            parameter in future releases).
        access_key (str, optional):
            The API access key to use for sessionless authentication.
        adapter (requests.Adaptor, optional):
            If a requests session adaptor is needed to ensure connectivity
            to the Tenable Security Center host, one can be provided here.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``1`` second.
        cert (tuple, optional):
            The client-side SSL certificate to use for authentication.  This
            format could be either a tuple or a string pointing to the
            certificate.  For more details, please refer to the
            `Requests Client-Side Certificates`_ documentation.
        p12_cert (str, optional):
            The client-side PKCS12 certificate to use for certificate-based
            authentication.  A password must be provided to descrypt the password
            along with the certificate file (see password).
        password (str, optional):
            The password to use for session authentication.
        port (int, optional):
            The port number to connect to on the specified host.  The
            default is port ``443``.  (NOTE: The `port` parameter will be
            deprecated in favor of the unified `url` parameter in future
            releases).
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``5``.
        scheme (str, optional):
            What HTTP scheme should be used for URI path construction.  The
            default is ``https``.  (NOTE: The `scheme` parameter will be
            deprecated in favor of the unified `url` parameter in future
            releases).
        secret_key (str, optional):
            The API secret key to use for sessionless authentication.
        session (requests.Session, optional):
            If a requests Session is provided, the provided session will be
            used instead of constructing one during initialization.
        ssl_verify (bool, optional):
            Should the SSL certificate on the Tenable Security Center instance be
            verified? Default is False.
        username (str, optional):
            The username to use for session authentication.
        timeout (int, optional):
            The connection timeout parameter informing the library how long to
            wait in seconds for a stalled response before terminating the
            connection.  If unspecified, the default is 300 seconds.


    Examples:
        A direct connection to Tenable Security Center:

        >>> from tenable.sc import TenableSC
        >>> sc = TenableSC(url='https://sc.company.tld')

        A connection to Tenable Security Center using SSL certificates:

        >>> sc = TenableSC(url='https://sc.company.tld',
        ...                cert=('/path/client.cert', '/path/client.key')
                           )

        Using a PKCS12 Certificate:

        >>> sc = TenableSC(url='https://sc.company.tld',
        ...                p12_cert='/path/client.p12',
        ...                password='s3kr3tsqu1rr3l',
        ...                )

        Using API Keys to communicate to Tenable Security Center:

        >>> sc = TenableSC(url='https://sc.company.tld',
        ...                access_key='abcdef1234567890',
        ...                secret_key='abcdef1234567890'
        ...                )



    For more information, please See Tenable's `SC API documentation`_ and
    the `SC API Best Practices Guide`_.

    .. _SC API documentation:
        https://docs.tenable.com/security-center/api/index.htm
    .. _SC API Best Practices Guide:
        https://docs.tenable.com/security-center/api_best_practices/Content/AboutScApiBestPrac.htm
    .. _Requests Client-Side Certificates:
        http://docs.python-requests.org/en/master/user/advanced/#client-side-certificates
    .. _requests_pkcs12:
        https://github.com/m-click/requests_pkcs12
    '''
    _env_base = 'TSC'
    _base_path: str = 'rest'
    _error_map = {403: APIError}
    _restricted_paths = ['token', 'credential']
    _timeout = 300
    _ssl_verify = False
    _version = None
    _client_cert: tempfile.NamedTemporaryFile
    _client_key: tempfile.NamedTemporaryFile
    _allowed_auth_mech_priority = ['key', 'cert', 'session']
    _allowed_auth_mech_params = {
        'session': ['username', 'password'],
        'key': ['access_key', 'secret_key'],
        'cert': ['_cert'],
    }

    def __init__(self,  # noqa: PLR0913
                 host: Optional[str] = None,
                 access_key: Optional[str] = None,
                 secret_key: Optional[str] = None,
                 **kwargs
                 ):
        # As we will always be passing a URL to the APISession class, we will
        # want to construct a URL that APISession (and further requests)
        # understands.
        if host:
            warnings.warn('The "host", "port", and "scheme" parameters are '
                          'deprecated and will be removed from the TenableSC '
                          'class in version 2.0.',
                          DeprecationWarning,
                          stacklevel=2
                          )
            kwargs['url'] = (f'{kwargs.get("scheme", "https")}://'
                             f'{host}:{kwargs.get("port", 443)}'
                             )

        kwargs['access_key'] = access_key
        kwargs['secret_key'] = secret_key

        # Check to see if there is a p12_cert and password specified, if so, then
        # convert the cert into an unencrypted PEM format and construct the cert
        # tuple from the _p12_auth response.
        if 'p12_cert' in kwargs and 'password' in kwargs:
            cert = self._p12_auth(kwargs['p12_cert'], kwargs['password'])
            kwargs['cert'] = cert

        # If the cert argument exists, then set _cert to True in order to pass the
        # cert auth checks.
        if 'cert' in kwargs:
            kwargs['_cert'] = True
        # Now lets pass the relevant parts off to the APISession's constructor
        # to make sure we have everything lined up as we expect.
        super().__init__(**kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.logout()

    def _resp_error_check(self, response, **kwargs):
        if not kwargs.get('stream', False):
            try:
                data = response.json()
                if data['error_code']:
                    raise APIError(response)
            except ValueError:
                pass
        return response

    def _key_auth(self, access_key, secret_key):
        """
        API Key Authentication
        """
        # if we can pull a version, check to see that the version is at least
        # 5.13, which is the minimum version of SC that supports API Keys.  If
        # we cant pull a version, then we will assume it's ok.
        if (not self.version
            or VersionInfo.parse(self.version).match('>=5.13.0')
        ):
            self._session.headers.update({
                'X-APIKey': f'accessKey={access_key}; secretKey={secret_key}'
            })
            self._auth_mech = 'keys'
        else:
            raise ConnectionError(
                   f'API Keys not supported on Tenable Security Center {self.version}'
                )

    def _session_auth(self, username, password):
        """
        Basic Session Authentication
        """
        warnings.warn('Session based authentication to Security Center will be removed'
                      'in later iterations of the library as it\'s no longer an'
                      'oficially recommended method of authentication to SC.',
                      DeprecationWarning,
                      stacklevel=2
                      )
        resp = self.post('token', json={
            'username': username,
            'password': password
        })
        self._auth_mech = 'user'
        self._session.headers.update({
            'X-SecurityCenter': str(resp.json()['response']['token']),
            'TNS_SESSIONID': str(resp.headers['Set-Cookie'])[14:46]
        })

    def _p12_auth(self, p12_cert, password):
        """
        PKCS12 Certificate Authentication
        """
        with open(p12_cert, 'rb') as fobj:
            key, cert, _ = serialization.pkcs12.load_key_and_certificates(
                fobj.read(), password.encode()
            )
        self._client_key = tempfile.NamedTemporaryFile()  # noqa: PLR1732
        self._client_key.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ))
        self._client_key.flush()

        self._client_cert = tempfile.NamedTemporaryFile()   # noqa: PLR1732
        self._client_cert.write(cert.public_bytes(serialization.Encoding.PEM))
        self._client_cert.flush()
        return self._client_cert.name, self._client_key.name

    def _cert_auth(self, _cert):
        """
        PEM Cert Authentication
        """
        resp = self.get('system', box=False)
        self._session.headers.update({
            'X-SecurityCenter': str(resp.json()['response']['token']),
            'TNS_SESSIONID': str(resp.headers['Set-Cookie'])[14:46]
        })
        self._auth_meth = 'cert'


    def _deauthenticate(self):  # noqa PLW0221
        super()._deauthenticate(path='token')

    def login(self, username=None, password=None,
              access_key=None, secret_key=None):
        '''
        Logs the user into Tenable Security Center

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
        warnings.warn('Use of the login method is deprecated and will be removed in'
                      'later versions of the library',
                      DeprecationWarning,
                      stacklevel=2
                      )
        self._authenticate(**{
            'username': username,
            'password': password,
            'access_key': access_key,
            'secret_key': secret_key
        })

    def logout(self):
        '''
        Logs out of Tenable Security Center and resets the session.

        Examples:
            >>> sc.logout()
        '''
        self._deauthenticate()

    @property
    def version(self):
        """
        The version of the SecurityCenter instance
        """
        if not self._version:
            # We will attempt to pull the version number from the system
            # details method.  If we get an APRError response, then we will
            # simply pass through.
            try:
                version = self.system.details().get('version')
            except APIError:
                pass
            else:
                self._version = version
        return self._version

    @property
    def accept_risks(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Accept Risks APIs <accept_risks>`.
        '''
        return AcceptRiskAPI(self)

    @property
    def alerts(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Alerts APIs <alerts>`.
        '''
        return AlertAPI(self)

    @property
    def analysis(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Analysis APIs <analysis>`.
        '''
        return AnalysisAPI(self)

    @property
    def asset_lists(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Asset Lists APIs <asset_lists>`.
        '''
        return AssetListAPI(self)

    @property
    def audit_files(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Audit Files APIs <audit_files>`.
        '''
        return AuditFileAPI(self)

    @property
    def credentials(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Credentials APIs <credentials>`.
        '''
        return CredentialAPI(self)

    @property
    def current(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Current Session APIs <current>`.
        '''
        return CurrentSessionAPI(self)

    @property
    def feeds(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Feeds APIs <feeds>`.
        '''
        return FeedAPI(self)

    @property
    def files(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Files APIs <files>`.
        '''
        return FileAPI(self)

    @property
    def groups(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Groups APIs <groups>`.
        '''
        return GroupAPI(self)

    @property
    def organizations(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Organization APIs <organizations>`.
        '''
        return OrganizationAPI(self)

    @property
    def plugins(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Plugins APIs <plugins>`.
        '''
        return PluginAPI(self)

    @property
    def policies(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Policies APIs <policies>`.
        '''
        return ScanPolicyAPI(self)

    @property
    def queries(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Queries APIs <queries>`.
        '''
        return QueryAPI(self)

    @property
    def recast_risks(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Recast Risks APIs <recast_risks>`.
        '''
        return RecastRiskAPI(self)

    @property
    def repositories(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Repositories APIs <repositories>`.
        '''
        return RepositoryAPI(self)

    @property
    def roles(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Roles APIs <roles>`.
        '''
        return RoleAPI(self)

    @property
    def scanners(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Scanners APIs <scanners>`.
        '''
        return ScannerAPI(self)

    @property
    def scans(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Scans APIs <scans>`.
        '''
        return ScanAPI(self)

    @property
    def scan_instances(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Scan Instances APIs <scan_instances>`.
        '''
        return ScanResultAPI(self)

    @property
    def scan_zones(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Scan Zones APIs <scan_zones>`.
        '''
        return ScanZoneAPI(self)

    @property
    def status(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Status APIs <status>`.
        '''
        return StatusAPI(self)

    @property
    def system(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center System APIs <system>`.
        '''
        return SystemAPI(self)

    @property
    def users(self):
        '''
        The interface object for the
        :doc:`Tenable Security Center Users APIs <users>`.
        '''
        return UserAPI(self)
