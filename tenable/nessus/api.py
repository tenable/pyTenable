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

'''
from tenable.base.platform import APIPlatform
from .agent_groups import AgentGroupsAPI
from .agents import AgentsAPI


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
        The interface object for the
        :doc:`Nessus Agents APIs <agents>`.
        '''
        return AgentsAPI(self)
