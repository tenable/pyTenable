from tenable.tenable_io.base import TIOEndpoint

class AgentConfigAPI(TIOEndpoint):
    def edit(self, scanner_id=1, software_update=None, auto_unlink=None):
        '''
        `agent-config: edit <https://cloud.tenable.com/api#/resources/agent-config/edit>`_

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
            dict: Dictionary of the applied settings is returned if successfully
                applied.

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
        `agent-config: details <https://cloud.tenable.com/api#/resources/agent-config/details>`_

        Args:
            scanner_id (int, optional): The scanner ID.

        Returns:
            dict: Dictionary of the current settings.
        '''
        if not scanner_id:
            scanner_id = 1
        return self._api.get(
            'scanners/{}/agents/config'.format(
                self._check('scanner_id', scanner_id, int)
            )).json()
