from tenable.tenable_io.agent_config import AgentConfigAPI
from tenable.tenable_io.agent_exclusions import AgentExclusionsAPI
from tenable.tenable_io.agent_groups import AgentGroupsAPI
from tenable.tenable_io.agents import AgentsAPI
from tenable.tenable_io.assets import AssetsAPI
from tenable.tenable_io.audit_log import AuditLogAPI
from tenable.tenable_io.editor import EditorAPI
from tenable.tenable_io.exclusions import ExclusionsAPI
from tenable.tenable_io.file import FileAPI
from tenable.tenable_io.filters import FiltersAPI
from tenable.tenable_io.folders import FoldersAPI
from tenable.tenable_io.groups import GroupsAPI
from tenable.tenable_io.permissions import PermissionsAPI
from tenable.tenable_io.plugins import PluginsAPI
from tenable.tenable_io.scans import ScansAPI
from tenable.base import APISession


class TenableIO(APISession):
    '''
    The Tenable.io object is the primary interaction point for users to
    interface with Tenable.io via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        access_key (str):
            The user's API access key for Tenable.io
        secret_key (str):
            The user's API secret key for Tenable.io
        url (str, optional):
            The base URL that the paths will be appended onto.  The default
            is ``https://cloud.tenable.com`` 
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``3``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``0.1`` seconds.
    '''
    
    _TZ = None
    URL = 'https://cloud.tenable.com'

    @property
    def agent_config(self):
        '''
        An object for interfacing to the agent configurations API.  See the
        :doc:`agent_config documentation <tenable_io.agent_config>` 
        for full details.
        '''
        return AgentConfigAPI(self)

    @property
    def agent_groups(self):
        '''
        An object for interfacing to the agent groups API.  See the
        :doc:`agent_groups documentation <tenable_io.agent_groups>` 
        for full details.
        '''
        return AgentGroupsAPI(self)

    @property
    def agent_exclusions(self):
        '''
        An object for interfacing to the agent exclusions API.  See the
        :doc:`agent_exclusions documentation <tenable_io.agent_exclusions>` 
        for full details.
        '''
        return AgentExclusionsAPI(self)

    @property
    def agents(self):
        '''
        An object for interfacing to the agents API.  See the
        :doc:`agents documentation <tenable_io.agents>` 
        for full details.
        '''
        return AgentsAPI(self)

    @property
    def assets(self):
        '''
        An object for interfacing to the assets API.  See the
        :doc:`assets documentation <tenable_io.assets>` 
        for full details.
        '''
        return AssetsAPI(self)

    @property
    def audit_log(self):
        '''
        An object for interfacing to the audit log API.  See the
        :doc:`audit_log documentation <tenable_io.audit_log>` 
        for full details.
        '''
        return AuditLogAPI(self)

    @property
    def editor(self):
        '''
        An object for interfacing to the editor API.  See the
        :doc:`editor documentation <tenable_io.editor>` 
        for full details.
        '''
        return EditorAPI(self)

    @property
    def exclusions(self):
        '''
        An object for interfacing to the exclusions API.  See the
        :doc:`exclusions documentation <tenable_io.exclusions>` 
        for full details.
        '''
        return ExclusionsAPI(self)

    @property
    def file(self):
        '''
        An object for interfacing to the file API.  See the
        :doc:`file documentation <tenable_io.file>` 
        for full details.
        '''
        return FileAPI(self)

    @property
    def filters(self):
        '''
        An object for interfacing to the filters API.  See the
        :doc:`filters documentation <tenable_io.filters>` 
        for full details.
        '''
        return FiltersAPI(self)

    @property
    def folders(self):
        '''
        An object for interfacing to the folders API.  See the
        :doc:`folders documentation <tenable_io.folders>` 
        for full details.
        '''
        return FoldersAPI(self)

    @property
    def groups(self):
        '''
        An object for interfacing to the groups API.  See the
        :doc:`groups documentation <tenable_io.groups>` 
        for full details.
        '''
        return GroupsAPI(self)

    @property
    def permissions(self):
        '''
        An object for interfacing to the permissions API.  See the
        :doc:`permissions documentation <tenable_io.permissions>` 
        for full details.
        '''
        return PermissionsAPI(self)

    @property
    def plugins(self):
        '''
        An object for interfacing to the plugins API.  See the
        :doc:`plugins documentation <tenable_io.plugins>` 
        for full details.
        '''
        return PluginsAPI(self)

    @property
    def policies(self):
        '''
        An object for interfacing to the policies API.  See the
        :doc:`policies documentation <tenable_io.policies>` 
        for full details.
        '''
        return None

    @property
    def scanner_groups(self):
        '''
        An object for interfacing to the scanner groups API.  See the
        :doc:`scanner_groups documentation <tenable_io.scanner_groups>` 
        for full details.
        '''
        return None

    @property
    def scanners(self):
        '''
        An object for interfacing to the scanners API.  See the
        :doc:`scanners documentation <tenable_io.scanners>` 
        for full details.
        '''
        return None

    @property
    def scans(self):
        '''
        An object for interfacing to the scans API.  See the
        :doc:`scans documentation <tenable_io.scans>` 
        for full details.
        '''
        return ScansAPI(self)

    @property
    def server(self):
        '''
        An object for interfacing to the server API.  See the
        :doc:`server documentation <tenable_io.server>` 
        for full details.
        '''
        return None

    @property
    def session(self):
        '''
        An object for interfacing to the session API.  See the
        :doc:`session documentation <tenable_io.session>` 
        for full details.
        '''
        return None

    @property
    def target_groups(self):
        '''
        An object for interfacing to the target groups API.  See the
        :doc:`target_groups documentation <tenable_io.target_groups>` 
        for full details.
        '''
        return None

    @property
    def users(self):
        '''
        An object for interfacing to the users API.  See the
        :doc:`users documentation <tenable_io.users>` 
        for full details.
        '''
        return None

    @property
    def workbenches(self):
        '''
        An object for interfacing to the workbenches API.  See the
        :doc:`workbenches documentation <tenable_io.workbenches>` 
        for full details.
        '''
        return None

    @property
    def _tz(self):
        '''
        As we will be using the timezone listing in a lot of parameter checking,
        we should probably cache the response as a private attribute to speed 
        up checking times.
        '''
        if not self._TZ:
            self._TZ = self.scans.timezones()
        return self._TZ

    def __init__(self, access_key, secret_key, url=None, retries=None, backoff=None):
        self._access_key = access_key
        self._secret_key = secret_key
        APISession.__init__(self, url, retries, backoff)

    def _build_session(self):
        '''
        Build the session and add the API Keys into the session
        '''
        APISession._build_session(self)
        self._session.headers.update({
            'X-APIKeys': 'accessKey={}; secretKey={};'.format(
                self._access_key, self._secret_key)
        })