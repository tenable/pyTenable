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
            The base URL that the paths will be appended onto.  

            For example, if you want to override the default URL base with 
            _http://a.b.c/api_, you could then make a GET requests with 
            self.get('item').  This would then inform APISession to 
            construct a GET request to _http://ab.c./api/item_ and use
            whatever parameters you wanted to pass to the Requests Session
            object.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is 3.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.
    '''
    URL = 'https://cloud.tenable.com'
    def __init__(self, access_key, secret_key, url=None, retries=None, backoff=None):
        self._access_key = access_key
        self._secret_key = secret_key
        APISession.__init__(self, url, retries, backoff)

        # Graft on the API Components
        self.agent_config = AgentConfigAPI(self)
        self.agent_groups = AgentGroupsAPI(self)
        self.agent_exclusions = AgentExclusionsAPI(self)
        self.agents = AgentsAPI(self)
        self.assets = AssetsAPI(self)
        self.audit_log = AuditLogAPI(self)
        self.editor = EditorAPI(self)
        self.exclusions = ExclusionsAPI(self)
        self.file = FileAPI(self)
        self.filters = FiltersAPI(self)
        self.folders = FoldersAPI(self)
        self.groups = GroupsAPI(self)
        self.permissions = PermissionsAPI(self)
        self.plugins = PluginsAPI(self)
        self.scans = ScansAPI(self)

        # As we will be using the timezone listing in a lot of parameter
        # checking, we should probably cache the response as a private
        # attribute to speed up checking times.
        self._tz = self.scans.timezones()

    def _build_session(self):
        '''
        Build the session and add the API Keys into the session
        '''
        APISession._build_session(self)
        self._session.headers.update({
            'X-APIKeys': 'accessKey={}; secretKey={};'.format(
                self._access_key, self._secret_key)
        })