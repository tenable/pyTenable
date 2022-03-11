'''
Vulnerability Management
========================

The following API's are available for interaction under
Vulnerability Management platform.

Methods available on ``tio.v3.vm``:


.. rst-class:: hide-signature
.. autoclass:: VulnerabilityManagement
    :members:

.. toctree::
    :hidden:
    :glob:

    agent_config
    agent_groups
    agents
    credentials
    exclusions
    agent_exclusions
    files
    folders
    networks
    permissions
    plugins
    remediation_scans
    scans
    scanners
    scanner_groups
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.vm.agent_exclusions.api import AgentExclusionsAPI
from tenable.io.v3.vm.agent_config.api import AgentsConfigAPI
from tenable.io.v3.vm.agent_groups.api import AgentGroupsAPI
from tenable.io.v3.vm.agents.api import AgentsAPI
from tenable.io.v3.vm.audit_log.api import AuditLogAPI
from tenable.io.v3.vm.credentials.api import CredentialsAPI
from tenable.io.v3.vm.exclusions.api import ExclusionsAPI
from tenable.io.v3.vm.files.api import FileAPI
from tenable.io.v3.vm.folders.api import FoldersAPI
from tenable.io.v3.vm.networks.api import NetworksAPI
from tenable.io.v3.vm.permissions.api import PermissionsAPI
from tenable.io.v3.vm.plugins.api import PluginsAPI
from tenable.io.v3.vm.remediation_scans.api import RemediationScansAPI
from tenable.io.v3.vm.scanner_groups.api import ScannerGroupsAPI
from tenable.io.v3.vm.scanners.api import ScannersAPI
from tenable.io.v3.vm.scans.api import ScansAPI
from tenable.io.v3.vm.server.api import ServerAPI


class VulnerabilityManagement(ExploreBaseEndpoint):
    '''
    This class will contain property for all resources
    under Vulnerability Management
    i.e assets, agents, scanners etc.
    '''

    @property
    def agent_config(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Agent Config APIs <agent_config>`.
        '''
        return AgentsConfigAPI(self._api)

    @property
    def agent_exclusions(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Agent Exclusions APIs <agent_exclusions>`.
        '''
        return AgentExclusionsAPI(self._api)

    @property
    def agent_groups(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Agent Groups APIs <agent_groups>`.
        '''
        return AgentGroupsAPI(self._api)

    @property
    def agents(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Agents APIs <agents>`.
        '''
        return AgentsAPI(self._api)

    @property
    def audit_log(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Audit Log APIs <audit_log>`.
        '''
        return AuditLogAPI(self._api)

    @property
    def credentials(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Credentials APIs <credentials>`.
        '''
        return CredentialsAPI(self._api)

    @property
    def exclusions(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Exclusions APIs <exclusions>`.
        '''
        return ExclusionsAPI(self._api)

    @property
    def files(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Files APIs <files>`
        '''
        return FileAPI(self._api)

    @property
    def folders(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Folders APIs <folders>`
        '''
        return FoldersAPI(self._api)

    @property
    def networks(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Networks APIs <networks>`
        '''
        return NetworksAPI(self._api)

    @property
    def permissions(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Permissions APIs <permissions>`
        '''
        return PermissionsAPI(self._api)

    @property
    def plugins(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Plugins APIs <plugins>`
        '''
        return PluginsAPI(self._api)

    @property
    def remediation_scans(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Remediation Scans APIs <remediation_scans>`
        '''
        return RemediationScansAPI(self._api)
    
    @property
    def scans(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Scans APIs <scans>`
        '''
        return ScansAPI(self._api)

    @property
    def scanners(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Scanners APIs <scanners>`
        '''
        return ScannersAPI(self._api)

    @property
    def scanner_groups(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Scanner Groups APIs <scanner_groups>`
        '''
        return ScannerGroupsAPI(self._api)

    @property
    def server(self):
        '''
        The interface object for the
        :doc:`Tenable.io v3 Server APIs <server>`
        '''
        return ServerAPI(self._api)