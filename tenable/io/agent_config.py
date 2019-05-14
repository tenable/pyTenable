'''
agent_config
============

The following methods allow for interaction into the Tenable.io
:devportal:`agent config <agent-config>` API endpoints.

Methods available on ``tio.agent_config``:

.. rst-class:: hide-signature
.. autoclass:: AgentConfigAPI

    .. automethod:: edit
    .. automethod:: details
'''
from .base import TIOEndpoint

class AgentConfigAPI(TIOEndpoint):
    def edit(self, scanner_id=1, software_update=None, auto_unlink=None):
        '''
        Edits the agent configuration.

        :devportal:`agent-config: edit <agent-config-details>`

        Args:
            scanner_id (int, optional): The scanner ID.
            software_update (bool, optional):
                If True, software updates are enabled for agents (exclusions may
                override this).  If false, software updates for all agents are
                disabled.
            auto_unlink (int, optional):
                If true, agent auto-unlinking is enabled, allowing agents to
                automatically unlink themselves after a given period of time.
                If the value is 0 or false, auto-unlinking is disabled.  True
                values are between 1 and 365.

        Returns:
            :obj:`dict`:
                Dictionary of the applied settings is returned if successfully
                applied.

        Examples:
            Enabling auto-unlinking for agents after 30 days:

            >>> tio.agent_config.edit(auto_unlink=30)

            Disabling auto-unlinking for agents:

            >>> tio.agent_config.edit(auto_unlink=False)

            Enabling software updates for agents:

            >>> tio.agent_config.edit(software_update=True)
        '''
        # Lets build the dictionary that we will present to the API...
        payload = {'auto_unlink': {}}
        if not scanner_id:
            scanner_id = 1
        if self._check('software_update', software_update, bool):
            payload['software_update'] = software_update
        if auto_unlink:
            payload['auto_unlink']['enabled'] = True
            payload['auto_unlink']['expiration'] = self._check(
                'auto_unlink', auto_unlink, int, [False] + list(range(1, 366)))
        elif auto_unlink in [False, 0]:
            payload['auto_unlink']['enabled'] = False

        # Now to run the API call and get the response
        return self._api.put(
            'scanners/{}/agents/config'.format(
                self._check('scanner_id', scanner_id, int)
            )).json()

    def details(self, scanner_id=1):
        '''
        Returns the current agent configuration.

        :devportal:`agent-config: details <agent-config-edit>`

        Args:
            scanner_id (int, optional): The scanner ID.

        Returns:
            :obj:`dict`:
                Dictionary of the current settings.

        Examples:
            >>> details = tio.agent_config.details()
            >>> pprint(details)
        '''
        if not scanner_id:
            scanner_id = 1
        return self._api.get(
            'scanners/{}/agents/config'.format(
                self._check('scanner_id', scanner_id, int)
            )).json()
