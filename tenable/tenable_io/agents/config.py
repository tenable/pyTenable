from tenable.base import APIEndpoint

class AgentConfigAPI(APIEndpoint):
    def edit(self, scanner_id=None, software_update=None, auto_unlink=None, 
             unlink_exp=None):
        '''
        agent-config: edit
        https://cloud.tenable.com/api#/resources/agent-config/edit

        Args:
            scanner_id (int): The scanner ID.
            software_update (:obj:`bool`, optional): 
                If True, software updates are enabled for agents (exclusions may
                override this).  If false, software updates for all agents are
                disabled.
            auto_unlink (:obj:`bool`, optional):
                If true, agent auto-unlinking is enabled, allowing agents to
                automatically unlink themselves after a given period of time.
            unkink_exp (:obj:`int`, optional):
                The expiration time for agents to auto-unlink in days. Agents
                will be removed from Tenable.io automatically after the
                inactivity age of the agent crosses this threshold.  Valid
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
        if self._check('auto_unlink', auto_unlink, bool):
            payload['auto_unlink']['enabled'] = auto_unlink
        if self._check('unlink_exp', unlink_exp, int, range(1, 366)):
            payload['auto_unlink']['expiration'] = unlink_exp

        # Now to run the API call and get the response
        return self._api.put(
            'scanners/{}/agents/config'.format(
                self._check('scanner_id', scanner_id, int)
            )).json()

    def details(self, scanner_id=None):
        '''
        agent-config: details
        https://cloud.tenable.com/api#/resources/agent-config/details

        Args:
            scanner_id (int): The scanner ID.

        Returns:
            dict: Dictionary of the current settings.
        '''
        if not scanner_id:
            scanner_id = 1
        return self._api.get(
            'scanners/{}/agents/config'.format(
                self._check('scanner_id', scanner_id, int)
            )).json()
