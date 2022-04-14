'''
Agent Config
============

The following methods allow for interaction into the Tenable.io
:devportal:`agent config <agent-config>` API endpoints.

Methods available on ``tio.v3.vm.agent_config``:

.. rst-class:: hide-signature
.. autoclass:: AgentsConfigAPI
    :members:
'''
from typing import Dict, Optional

from restfly.utils import dict_clean

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.vm.agent_config.schema import AgentsConfigSchema


class AgentsConfigAPI(ExploreBaseEndpoint):
    '''
    This will contain all methods related to agent config
    '''
    _path: str = 'api/v3/agents/config'
    _conv_json: bool = True
    _schema = AgentsConfigSchema()

    def details(self) -> Dict:
        '''
        Returns the current agent configuration.

        :devportal:`agent-config: details <agent-config-details>`

        Returns:
            :obj:`dict`:
                Dictionary of the current settings.

        Examples:
            >>> details = tio.v3.vm.agent_config.details()
            >>> pprint(details)
        '''
        return self._get()

    def edit(self,
             auto_unlink: Optional[int] = None,
             software_update: Optional[bool] = None) -> Dict:
        '''
        Edits the agent configuration.

        :devportal:`agent-config: edit <agent-config-edit>`

        Args:
            auto_unlink (int, optional):
                If true, agent auto-unlinking is enabled, allowing agents to
                automatically unlink themselves after a given period of time.
                If the value is 0 or false, auto-unlinking is disabled.  True
                values are between 1 and 365.
            software_update (bool, optional):
                If True, software updates are enabled for agents
                (exclusions may override this).  If false, software
                updates for all agents are disabled.

        Returns:
            :obj:`dict`:
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
        payload = {
            'software_update': software_update,
            'auto_unlink': {
                'expiration': auto_unlink
            }
        }

        # Let's remove None value from payload
        payload = dict_clean(payload)

        # Let's validate schema
        payload = self._schema.dump(self._schema.load(payload))

        return self._put(json=payload)
