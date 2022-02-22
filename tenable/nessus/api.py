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
    migration
    permissions
    plugin_rules
    plugins
    policies
    proxy
    scanners
    scans
    server
    settings
    software_update
    tokens
    users
'''
from tenable.base.platform import APIPlatform
from .agent_groups import AgentGroupsAPI
from .agents import AgentsAPI
from .files import FilesAPI
from .folders import FoldersAPI
from .groups import GroupsAPI
from .mail import MailAPI
from .permissions import PermissionsAPI
from .plugin_rules import PluginRulesAPI
from .proxy import ProxyAPI
from .plugins import PluginsAPI
from .scanners import ScannersAPI
from .server import ServerAPI


class Nessus(APIPlatform):
    '''
    The Nessus object is the primary interaction point for users to
    interface with Nessus via the pyTenable library.  All of the API
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
        :doc:`Nessus Agent Groups APIs <agent_groups>`.
        '''
        return AgentGroupsAPI(self)

    @property
    def agents(self):
        '''
        The interface object for the :doc:`Nessus Agents APIs <agents>`.
        '''
        return AgentsAPI(self)
    
    @property
    def files(self):
        '''
        The interface object for the :doc:`Nessus File APIs <files>`.
        '''
        return FilesAPI(self)
    
    @property
    def folders(self):
        '''
        The interface object for the :doc:`Nessus Folders APIs <folders>`.
        '''
        return FoldersAPI(self)
    
    @property
    def groups(self):
        '''
        The interface object for the :doc:`Nessus Groups APIs <groups>`.
        '''
        return GroupsAPI(self)
    
    @property
    def mail(self):
        '''
        The interface object for the :doc:`Nessus Mail APIs <mail>`.
        '''
        return MailAPI(self)
    
    @property
    def permissions(self):
        '''
        The interface object for the 
        :doc:`Nessus Permissions APIs <permissions>`.
        '''
        return PermissionsAPI(self)
    
    @property
    def plugin_rules(self):
        '''
        The interface object for the 
        :doc:`Nessus Plugin Rules APIs <plugin_rules>`.
        '''
        return PluginRulesAPI(self)

    @property
    def plugins(self):
        '''
        The interface object for the :doc:`Nessus Plugins APIs <plugins>`.
        '''
        return PluginsAPI(self)
    
    @property
    def proxy(self):
        '''
        The interface object for the :doc:`Nessus Proxy APIs <proxy>`.
        '''
        return ProxyAPI(self)
    
    @property
    def scanners(self):
        '''
        The interface object for the :doc:`Nessus Scanners APIs <scanners>`.
        '''
        return ScannersAPI(self)
    
    @property
    def server(self):
        '''
        The interface object for the :doc:`Nessus Server APIs <server>`.
        '''
        return ServerAPI(self)
