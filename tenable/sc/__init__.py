'''
.. autoclass:: TenableSC

    .. automethod:: login
    .. automethod:: logout

.. automodule:: tenable.sc.alerts
.. automodule:: tenable.sc.accept_risks
.. automodule:: tenable.sc.analysis
.. automodule:: tenable.sc.audit_files
.. automodule:: tenable.sc.credentials
.. automodule:: tenable.sc.feeds
.. automodule:: tenable.sc.files
.. automodule:: tenable.sc.groups
.. automodule:: tenable.sc.plugins
.. automodule:: tenable.sc.policies
.. automodule:: tenable.sc.repositories
.. automodule:: tenable.sc.roles
.. automodule:: tenable.sc.scan_zones
.. automodule:: tenable.sc.scans
.. automodule:: tenable.sc.scan_instances
.. automodule:: tenable.sc.scanners
.. automodule:: tenable.sc.status
.. automodule:: tenable.sc.system
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
from tenable.base import APISession
from tenable.errors import *
from .accept_risks import AcceptRiskAPI
from .alerts import AlertAPI
from .analysis import AnalysisAPI
from .audit_files import AuditFileAPI
from .credentials import CredentialAPI
from .files import FileAPI
from .feeds import FeedAPI
from .groups import GroupAPI
from .plugins import PluginAPI
from .policies import ScanPolicyAPI
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
import warnings, logging


class TenableSC(APISession):
    '''TenableSC API Wrapper
    The Tenable.sc object is the primary interaction point for users to
    interface with Tenable.sc via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        host (str):
            The address of the Tenable.sc instance to connect to.
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
        port (int, optional):
            The port number to connect to on the specified host.  The
            default is port ``443``.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``3``.
        scheme (str, optional):
            What HTTP scheme should be used for URI path construction.  The
            default is ``https``.
        session (requests.Session, optional):
            If a requests Session is provided, the provided session will be used
            instead of constructing one during initialization.
        ssl_verify (bool, optional):
            Should the SSL certificate on the Tenable.sc instance be verified?
            Default is False.
        ua_identity (str, optional):
            An application identifier to be added into the User-Agent string
            for the purposes of application identification.


    Examples:
        A direct connection to TenableSC:

        >>> from tenable.sc import TenableSC
        >>> sc = TenableSC('securitycenter.company.tld')

        A connection to TenableSC using SSL certificates:

        >>> sc = TenableSC('securitycenter.company.tld',
        ...     cert=('/path/client.cert', '/path/client.key'))

        Using an adaptor to use a passworded certificate (via the immensely
        useful `requests_pkcs12`_ adaptor):

        >>> from requests_pkcs12 import Pkcs12Adapter
        >>> adapter = Pkcs12Adapter(
        ...     pkcs12_filename='certificate.p12',
        ...     pkcs12_password='omgwtfbbq!')
        >>> sc = TenableSC('securitycenter.company.tld', adapter=adapter)

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
    _restricted_paths = ['token']
    _error_codes = {
        400: InvalidInputError,
        403: APIError,
        404: NotFoundError,
        500: ServerError,
    }

    def __init__(self, host, port=443, ssl_verify=False, cert=None, adapter=None,
                 scheme='https', retries=None, backoff=None, ua_identity=None,
                 session=None, proxies=None):
        # As we will always be passing a URL to the APISession class, we will
        # want to construct a URL that APISession (and further requests)
        # understands.
        base = '{}://{}:{}'.format(scheme, host, port)
        url = '{}/rest'.format(base)

        # Now lets pass the relevent parts off to the APISession's constructor
        # to make sure we have everything lined up as we expect.
        APISession.__init__(self, url,
            retries=retries,
            backoff=backoff,
            ua_identity=ua_identity,
            session=session,
            proxies=proxies)

        # Also, as Tenable.sc is generally installed without a certificate
        # chain that we can validate, we will want to turn off verification
        # and the associated warnings unless told to otherwise:
        self._session.verify = ssl_verify
        if not ssl_verify:
            warnings.filterwarnings('ignore', 'Unverified HTTPS request')

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
                    'X-SecurityCenter': str(d['response']['token'])
                })
        except:
            raise ConnectionError('Invalid Tenable.sc Instance')

    def _resp_error_check(self, response):
        try:
            d = response.json()
            if d['error_code']:
                raise APIError(d['error_code'], d['error_msg'])
        except ValueError:
            pass
        return response

    def login(self, user, passwd):
        '''
        Logs the user into Tenable.sc

        Args:
            user (str): Username
            passwd (str): Password

        Returns:
            None

        Examples:
            >>> sc = TenableSC('127.0.0.1', port=8443)
            >>> sc.login('username', 'password')
        '''
        resp = self.post('token', json={'username': user, 'password': passwd})
        self._session.headers.update({
            'X-SecurityCenter': str(resp.json()['response']['token'])
        })

    def logout(self):
        '''
        Logs out of Tenable.sc and resets the session.

        Returns:
            None

        Examples:
            >>> sc.logout()
        '''
        resp = self.delete('token')
        self._build_session()

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
    def audit_files(self):
        return AuditFileAPI(self)

    @property
    def credentials(self):
        return CredentialAPI(self)

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
    def plugins(self):
        return PluginAPI(self)

    @property
    def policies(self):
        return ScanPolicyAPI(self)

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


class SecurityCenter(TenableSC):
    '''
    The historical name for TenableSC prior to the rename in Nov 2018.  Usage is
    identical to using TenableSC, however we will throw a deprecation warning
    when using the SecurityCenter class.  Please use ``TenableSC``.
    '''
    def __init__(self, host, port=443, ssl_verify=False, cert=None,
                 scheme='https', retries=None, backoff=None):
        warnings.warn(
            ' '.join([
                'The SecurityCenter class has been replaced by the TenableSC',
                'class.  The existing SecurityCenter class will be removed in',
                'the first stable version (1.0).']),
            Warning)
        TenableSC.__init__(self, host, port, ssl_verify,
            cert, scheme, retries, backoff)
