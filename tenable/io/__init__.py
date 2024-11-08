'''
Tenable Vulnerability Management
================================

.. autoclass:: TenableIO
   :members:


.. toctree::
    :hidden:
    :glob:

    cs/index
    access_control
    agent_config
    agent_exclusions
    agent_groups
    agents
    assets
    audit_log
    credentials
    editor
    exclusions
    exports
    files
    filters
    folders
    groups
    networks
    permissions
    plugins
    policies
    remediation_scans
    scanner_groups
    scanners
    scans
    server
    session
    tags
    target_groups
    users
    was
    workbenches
'''
import warnings
from typing import Dict, Optional
from requests import Response


from tenable.base.platform import APIPlatform
from .access_control import AccessControlAPI
from .access_groups import AccessGroupsAPI
from .access_groups_v2 import AccessGroupsV2API
from .agent_config import AgentConfigAPI
from .agent_exclusions import AgentExclusionsAPI
from .agent_groups import AgentGroupsAPI
from .agents import AgentsAPI
from .assets import AssetsAPI
from .audit_log import AuditLogAPI
from .credentials import CredentialsAPI
from .cs.api import ContainerSecurity
from .editor import EditorAPI
from .exclusions import ExclusionsAPI
from .exports.api import ExportsAPI
from .files import FileAPI
from .filters import FiltersAPI
from .folders import FoldersAPI
from .groups import GroupsAPI
from .networks import NetworksAPI
from .permissions import PermissionsAPI
from .plugins import PluginsAPI
from .policies import PoliciesAPI
from .remediation_scans import RemediationScansAPI
from .scanner_groups import ScannerGroupsAPI
from .scanners import ScannersAPI
from .scans import ScansAPI
from .server import ServerAPI
from .session import SessionAPI
from .tags import TagsAPI
from .target_groups import TargetGroupsAPI
from .users import UsersAPI
from .v3 import Version3API
from .was.api import WasAPI
from .workbenches import WorkbenchesAPI


class TenableIO(APIPlatform):  # noqa: PLR0904
    '''
    The Tenable Vulnerability Management object is the primary interaction point for users to
    interface with Tenable Vulnerability Management via the pyTenable library.  All the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        access_key (str, optional):
            The user's API access key for Tenable Vulnerability Management.  If an access key isn't
            specified, then the library will attempt to read the environment
            variable ``TIO_ACCESS_KEY`` to acquire the key.
        secret_key (str, optional):
            The user's API secret key for Tenable Vulnerability Management.  If a secret key isn't
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
    _env_base = 'TIO'
    _tzcache = None
    _url = 'https://cloud.tenable.com'
    _timeout = 120

    def __init__(self,
                 access_key: Optional[str] = None,
                 secret_key: Optional[str] = None,
                 **kwargs
                 ):
        if access_key:
            kwargs['access_key'] = access_key
        if secret_key:
            kwargs['secret_key'] = secret_key
        super().__init__(**kwargs)

    def _retry_request(self,
                       response: Response,
                       retries: int,
                       **kwargs) -> Dict:
        '''
        If the call is retried, we will need to set some additional headers
        '''
        kwargs['headers'] = kwargs.get('headers', {})
        # if the request uuid exists in the response, then we will send the
        # uuid back so that there is solid request chain in the Tenable Vulnerability Management
        # platform logs.
        request_uuid = response.headers.get('X-Tio-Last-Request-Uuid')
        if request_uuid:
            kwargs['headers']['X-Tio-Last-Request-Uuid'] = request_uuid

        # We also need to return the number of times that we have attempted to
        # retry this call.
        kwargs['headers']['X-Tio-Retry-Count'] = str(retries)

        # Return the keyword arguments back to the caller.
        return kwargs

    @property
    def _tz(self):
        '''
        As we will be using the timezone listing in a lot of parameter
        checking, we should probably cache the response as a private attribute
        to speed up checking times.
        '''
        if not self._tzcache and self._auth_mech:
            self._tzcache = self.scans.timezones()
        return self._tzcache

    @property
    def cs(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Container Security APIs <cs/index>`.
        '''
        return ContainerSecurity(self)

    @property
    def access_control(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Access Control APIs <access_control>`.
        '''
        return AccessControlAPI(self)

    @property
    def access_groups(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Access Groups APIs <access_groups>`.
        '''
        warnings.warn('Access Groups have been deprecated from the TVM'
                      'platform.  This method will be removed in a future'
                      'version of the SDK.',
                      DeprecationWarning,
                      stacklevel=2
                      )
        return AccessGroupsAPI(self)

    @property
    def access_groups_v2(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Access Groups v2 APIs <access_groups_v2>`.
        '''
        warnings.warn('Access Groups have been deprecated from the TVM'
                      'platform.  This method will be removed in a future'
                      'version of the SDK.',
                      DeprecationWarning,
                      stacklevel=2
                      )
        return AccessGroupsV2API(self)

    @property
    def agent_config(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Agent Config APIs <agent_config>`.
        '''
        return AgentConfigAPI(self)

    @property
    def agent_groups(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Agent Groups APIs <agent_groups>`.
        '''
        return AgentGroupsAPI(self)

    @property
    def agent_exclusions(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Agent Exclusions APIs <agent_exclusions>`.
        '''
        return AgentExclusionsAPI(self)

    @property
    def agents(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Agents APIs <agents>`.
        '''
        return AgentsAPI(self)

    @property
    def assets(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management assets APIs <assets>`.
        '''
        return AssetsAPI(self)

    @property
    def audit_log(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Audit Log APIs <audit_log>`.
        '''
        return AuditLogAPI(self)

    @property
    def credentials(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Credentials APIs <credentials>`.
        '''
        return CredentialsAPI(self)

    @property
    def editor(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Editor APIs <editor>`.
        '''
        return EditorAPI(self)

    @property
    def exclusions(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Exclusions APIs <exclusions>`.
        '''
        return ExclusionsAPI(self)

    @property
    def exports(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Exports APIs <exports>`.
        '''
        return ExportsAPI(self)

    @property
    def files(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Files APIs <files>`.
        '''
        return FileAPI(self)

    @property
    def filters(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Filters APIs <filters>`.
        '''
        return FiltersAPI(self)

    @property
    def folders(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Folders APIs <folders>`.
        '''
        return FoldersAPI(self)

    @property
    def groups(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Groups APIs <groups>`.
        '''
        return GroupsAPI(self)

    @property
    def networks(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Networks APIs <networks>`.
        '''
        return NetworksAPI(self)

    @property
    def permissions(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Permissions APIs <permissions>`.
        '''
        return PermissionsAPI(self)

    @property
    def plugins(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Plugins APIs <plugins>`.
        '''
        return PluginsAPI(self)

    @property
    def policies(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Policies APIs <policies>`.
        '''
        return PoliciesAPI(self)

    @property
    def scanner_groups(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Scanner Groups APIs <scanner_groups>`.
        '''
        return ScannerGroupsAPI(self)

    @property
    def scanners(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Scanners APIs <scanners>`.
        '''
        return ScannersAPI(self)

    @property
    def scans(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Scans APIs <scans>`.
        '''
        return ScansAPI(self)

    @property
    def remediationscans(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Remediation Scans APIs <remediation_scans>`.
        '''
        return RemediationScansAPI(self)

    @property
    def server(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Server APIs <server>`.
        '''
        return ServerAPI(self)

    @property
    def session(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Session APIs <session>`.
        '''
        return SessionAPI(self)

    @property
    def tags(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Tags APIs <tags>`.
        '''
        return TagsAPI(self)

    @property
    def target_groups(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Target Groups APIs <target_groups>`.
        '''
        warnings.warn('Target Groups have been deprecated from the TVM'
                      'platform.  This method will be removed in a future'
                      'version of the SDK.',
                      DeprecationWarning,
                      stacklevel=2
                      )
        return TargetGroupsAPI(self)

    @property
    def users(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Users APIs <users>`.
        '''
        return UsersAPI(self)

    @property
    def workbenches(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management Workbenches APIs <workbenches>`.
        '''
        warnings.warn('The workbench module been deprecated from the TVM'
                      'package.  This method will be removed in a future'
                      'version of the SDK.  Please use the exports sub-pkg'
                      'instead.',
                      DeprecationWarning,
                      stacklevel=2
                      )
        return WorkbenchesAPI(self)

    @property
    def v3(self):
        '''
        The interface object for the
        :doc:`Tenable Vulnerability Management v3 APIs <v3/index>`.
        '''
        warnings.warn('The V3 sub-pkg have been deprecated from the TVM'
                      'package.  This method will be removed in a future'
                      'version of the SDK.  Please use the relocated modules'
                      'within the package',
                      DeprecationWarning,
                      stacklevel=2
                      )
        return Version3API(self)

    @property
    def was(self):
        """
        The interface object for the
        :doc:`Tenable Vulnerability Management WAS APIs <was>`.
        """
        return WasAPI(self)

