'''
Nessus
======

This package covers the Nessus interface.

.. autoclass:: Nessus
    :members:


.. toctree::
    :hidden:
    :glob:

    agent_groups
    agents
    editor
    files
    folders
    groups
    mail
    permissions
    plugins
    policies
    proxy
    scanners
    scans
    server
    session
    settings
    software_update
    tokens
    users
'''
from tenable.base.platform import APIPlatform
from .agent_groups import AgentGroupsAPI
from .agents import AgentsAPI
from .editor import EditorAPI
from .files import FilesAPI
from .folders import FoldersAPI
from .groups import GroupsAPI
from .mail import MailAPI
from .permissions import PermissionsAPI
from .plugin_rules import PluginRulesAPI
from .policies import PoliciesAPI
from .proxy import ProxyAPI
from .plugins import PluginsAPI
from .scanners import ScannersAPI
from .scans import ScansAPI
from .server import ServerAPI
from .session import SessionAPI
from .settings import SettingsAPI
from .software_update import SoftwareUpdateAPI
from .tokens import TokensAPI
from .users import UsersAPI


class Nessus(APIPlatform):
    '''
    The Nessus object is the primary interaction point for users to
    interface with Tenable Nessus via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.
    '''
    _env_base = 'NESSUS'
    _ssl_verify = False
    _conv_json = True

    def _session_auth(self, username, password):  # noqa: PLW0221,PLW0613
        token = self.post('session', json={
            'username': username,
            'password': password
        }).get('token')
        self._session.headers.update({
            'X-Cookie': f'token={token}'
        })
        self._auth_mech = 'user'

    @property
    def agent_groups(self):
        '''
        The interface object for the
        :doc:`Tenable Nessus Agent Groups APIs <agent_groups>`.
        '''
        return AgentGroupsAPI(self)

    @property
    def agents(self):
        '''
        The interface object for the :doc:`Tenable Nessus Agents APIs <agents>`.
        '''
        return AgentsAPI(self)

    @property
    def editor(self):
        '''
        The interface object for the :doc:`Tenable Nessus Editor APIs <editor>`.
        '''
        return EditorAPI(self)

    @property
    def files(self):
        '''
        The interface object for the :doc:`Tenable Nessus File APIs <files>`.
        '''
        return FilesAPI(self)

    @property
    def folders(self):
        '''
        The interface object for the :doc:`Tenable Nessus Folders APIs <folders>`.
        '''
        return FoldersAPI(self)

    @property
    def groups(self):
        '''
        The interface object for the :doc:`Tenable Nessus Groups APIs <groups>`.
        '''
        return GroupsAPI(self)

    @property
    def mail(self):
        '''
        The interface object for the :doc:`Tenable Nessus Mail APIs <mail>`.
        '''
        return MailAPI(self)

    @property
    def permissions(self):
        '''
        The interface object for the
        :doc:`Tenable Nessus Permissions APIs <permissions>`.
        '''
        return PermissionsAPI(self)

    @property
    def plugin_rules(self):
        '''
        The interface object for the
        :doc:`Tenable Nessus Plugin Rules APIs <plugin_rules>`.
        '''
        return PluginRulesAPI(self)

    @property
    def plugins(self):
        '''
        The interface object for the :doc:`Tenable Nessus Plugins APIs <plugins>`.
        '''
        return PluginsAPI(self)

    @property
    def policies(self):
        '''
        The interface object for the :doc:`Tenable Nessus Policies APIs <policies>`.
        '''
        return PoliciesAPI(self)

    @property
    def proxy(self):
        '''
        The interface object for the :doc:`Tenable Nessus Proxy APIs <proxy>`.
        '''
        return ProxyAPI(self)

    @property
    def scanners(self):
        '''
        The interface object for the :doc:`Tenable Nessus Scanners APIs <scanners>`.
        '''
        return ScannersAPI(self)

    @property
    def scans(self):
        '''
        The interface object for the :doc:`Tenable Nessus Scans APIs <scans>`.
        '''
        return ScansAPI(self)

    @property
    def server(self):
        '''
        The interface object for the :doc:`Tenable Nessus Server APIs <server>`.
        '''
        return ServerAPI(self)

    @property
    def session(self):
        '''
        The interface object for the :doc:`Tenable Nessus Session APIs <session>`.
        '''
        return SessionAPI(self)

    @property
    def settings(self):
        '''
        The interface object for the :doc:`Tenable Nessus Settings APIs <settings>`.
        '''
        return SettingsAPI(self)

    @property
    def software_update(self):
        '''
        The interface object for the
        :doc:`Tenable Nessus Software Update APIs <software_update>`.
        '''
        return SoftwareUpdateAPI(self)

    @property
    def tokens(self):
        '''
        The interface object for the :doc:`Tenable Nessus Tokens APIs <tokens>`.
        '''
        return TokensAPI(self)

    @property
    def users(self):
        '''
        The interface object for the :doc:`Tenable Nessus Users APIs <users>`.
        '''
        return UsersAPI(self)
