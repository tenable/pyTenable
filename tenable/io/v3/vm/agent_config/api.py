'''
Agent Config
============

The following methods allow for interaction into the Tenable.io
:devportal:`agent config <agent-config>` API endpoints.

Methods available on ``tio.v3.vm.agent_config``:

.. rst-class:: hide-signature
.. autoclass:: AgentConfigAPI
    :members:
'''
from typing import Dict

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class AgentConfigAPI(ExploreBaseEndpoint):
    '''
    This will contain all methods related to agent config
    '''
    _path: str = 'api/v3/agents'
    _conv_json: bool = True

    def edit(self, agent_id: int, auto_unlink: int,
             software_update: bool) -> Dict:
        '''
        Edits the agent configuration.

        :devportal:`agent-config: edit <agent-config-details>`

        Args:
            agent_id (int): The Agent ID.
            software_update (bool, optional):
                If True, software updates are enabled for agents
                (exclusions may override this).  If false, software
                updates for all agents are disabled.
            auto_unlink (int, optional):
                If true, agent auto-unlinking is enabled, allowing agents to
                automatically unlink themselves after a given period of time.
                If the value is 0 or false, auto-unlinking is disabled.  True
                values are between 1 and 365.

        Returns:
            :obj:`Dict`:
                Dictionary of the applied settings is returned if successfully
                applied.

        Examples:
            Enabling auto-unlinking for agents after 30 days:

            >>> tio.v3.vm.agent_config.edit(auto_unlink=30)

            Disabling auto-unlinking for agents:

            >>> tio.v3.vm.agent_config.edit(auto_unlink=False)

            Enabling software updates for agents:

            >>> tio.v3.vm.agent_config.edit(software_update=True)
        '''
        # Lets build the dictionary that we will present to the API...
        payload = {'auto_unlink': {}}
        if software_update in [True, False]:
            payload['software_update'] = software_update
        if auto_unlink and 0 < auto_unlink < 366:
            payload['auto_unlink']['enabled'] = True
            payload['auto_unlink']['expiration'] = auto_unlink
        elif auto_unlink in [False, 0]:
            payload['auto_unlink']['enabled'] = False
        return self._put(f'{agent_id}/config', json=payload)

    def details(self, agent_id: int) -> Dict:
        '''
        Returns the current agent configuration.

        :devportal:`agent-config: details <agent-config-edit>`

        Args:
            agent_id (int): The Agent ID.

        Returns:
            :obj:`Dict`:
                Dictionary of the current settings.

        Examples:
            >>> details = tio.v3.vm.agent_config.details()
            >>> pprint(details)
        '''
        return self._get(f'{agent_id}/config')
