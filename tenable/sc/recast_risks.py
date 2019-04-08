'''
recast_risks
============

The following methods allow for interaction into the Tenable.sc 
`Recast Risk <https://docs.tenable.com/sccv/api/Recast-Risk-Rule.html>`_ API.

Methods available on ``sc.recast_risks``:

.. rst-class:: hide-signature
.. autoclass:: RecastRiskAPI

    .. automethod:: apply
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: list
'''
from .base import SCEndpoint

class RecastRiskAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        document creator for recastRisk creation and update calls.
        '''
        if 'repos' in kw:
            # as repositories are passed in the API as a series of sub-documents
            # with the ID attribute set, we will convert the simply list that
            # was passed to us into a series of documents as the API expects.
            kw['repositories'] = [{'id': self._check('repo:id', r, int)} 
                for r in self._check('repos', kw['repos'], list)]
            del(kw['repos'])

        if 'plugin_id' in kw:
            # the plugin parameter
            kw['plugin'] = {
                'id': str(self._check('plugin_id', kw['plugin_id'], int))}
            del(kw['plugin_id'])

        if 'port' in kw:
            # as the port will only be passed if the default of "any" isn't
            # desired, we should check to make sure that the value passed is an
            # integer, and then convert it into a string.
            kw['port'] = str(self._check('port', kw['port'], int))

        if 'protocol' in kw:
            # as the protocol will only be passed if the default of "any" isn't
            # desired, we should check to make sure that the value passed is an
            # integer, and then convert it into a string.
            kw['protocol'] = str(self._check('protocol', kw['protocol'], int))

        if 'comments' in kw:
            # if a comment is attached to the rule, then lets just make sure
            # that we actually have a string here before moving on.
            self._check('comments', kw['comments'], str)

        if 'severity_id' in kw:
            # What should be the new severity id for the vulnerabilities
            # matching the rule?  Converts severity_id to a newSeverity document
            # with an id parameter matching the id passed.
            kw['newSeverity'] = {'id': self._check(
                'severity_id', kw['severity_id'], int, choices=[0, 1, 2, 3, 4])}
            del(kw['severity_id'])

        if 'ips' in kw:
            # if the ips list is passed, then 
            kw['hostType'] = 'ip'
            kw['hostValue'] = ','.join([self._check('ip:item', i, str) 
                for i in self._check('ips', kw['ips'], list)])
            del(kw['ips'])

        if 'uuids' in kw:
            kw['hostType'] = 'uuid'
            kw['hostValue'] = ','.join([self._check('uuid:item', i, str) 
                for i in self._check('uuids', kw['uuids'], list)])
            del(kw['uuids'])

        if 'asset_list' in kw:
            kw['hostType'] = 'asset'
            kw['hostValue'] = {'id': self._check('asset_list', kw['asset_list'], int)}
            del(kw['asset_list'])

        return kw

    def list(self, repo_ids=None, plugin_id=None, port=None, 
             org_ids=None, fields=None):
        '''
        Retrieves the list of recasted risk rules.

        + `recast-risk: list <https://docs.tenable.com/sccv/api/Recast-Risk-Rule.html#RecastRiskRuleRESTReference-/recastRiskRule>`_

        Args:
            fields (list, optional): 
                A list of attributes to return for each recast risk rule.
            plugin_id (int, optional):
                Plugin id to filter the response on.
            port (int, optional):
                Port number to filter the response on.
            org_ids (list, optional):
                List of organization ids to filter on.
            repo_ids (list, optional):
                List of repository ids to filter the response on.

        Returns:
            list: A list of recast risk rules.

        Examples:
            >>> for rule in sc.recast_risks.list():
            ...     pprint(rule)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in fields])
        
        if plugin_id:
            # validating that the plugin_id is an integer and assigning it to
            # the appropriate query parameter.
            params['pluginID'] = self._check('plugin_id', plugin_id, int)
    
        if port:
            # validating that port is an integer and assigning it to the
            # appropriate query parameter.
            params['port'] = self._check('port', port, int)
        
        if org_ids:
            # validating that org_ids is a list of integer values, then
            # converting the result into a comma-seperated string and assigning
            # it to the appropriate query parameter.
            params['organizationIDs'] = ','.join([self._check('org:id', i, int)
                for i in self._check('org_ids', org_ids, list)])
        
        if repo_ids:
            # validating that repo_ids is a list of integer values, then
            # converting the result into a comma-seperated string and assigning
            # it to the appropriate query parameter.
            params['repositoryIDs'] = ','.join([self._check('repo:id', i, int)
                for i in self._check('repo_ids', repo_ids, list)])

        return self._api.get('recastRiskRule', params=params).json()['response']

    def details(self, id, fields=None):
        '''
        Retrieves the details of an recast risk rule.

        + `recast-risk: details <https://docs.tenable.com/sccv/api/Recast-Risk-Rule.html#RecastRiskRuleRESTReference-/recastRiskRule/{id}>`_

        Args:
            id (int): The identifier for the recast risk rule.
            fields (list, optional): 
                A list of attributes to return for each recast risk rule.

        Returns:
            dict: The recast risk rule details.

        Examples:
            >>> rule = sc.recast_risks.details(1)
            >>> pprint(rule)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in fields])

        return self._api.get('recastRiskRule/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def delete(self, id):
        '''
        Removes the recast risk rule from Tenable.sc

        + `recast-risk: delete <https://docs.tenable.com/sccv/api/Recast-Risk-Rule.html#recastRiskRule_id_DELETE>`_

        Args:
            id (int): The identifier for the recast risk rule.

        Returns:
            str: Empty string response from the API.

        Examples:
            >>> sc.recast_risks.delete(1)
        '''
        return self._api.delete('recastRiskRule/{}'.format(
            self._check('id', id, int))).json()['response']

    def apply(self, id, repo):
        '''
        Applies the recast risk rule for either all repositories, or the
        repository specified.

        + `recast-risk: apply <https://docs.tenable.com/sccv/api/Recast-Risk-Rule.html#RecastRiskRuleRESTReference-/recastRiskRule/apply>`_

        Args:
            id (int): The identifier for the recast risk rule.
            repo (int, optional):
                A specific repository to apply the rule to.  The default if not
                specified is all repositories (``0``).

        Returns:
            str: Empty string response from the API.

        Examples:
            >>> sc.recast_risks.apply(1)
        '''
        return self._api.post('recastRiskRule/{}/apply'.format(
            self._check('id', id, int)), json={
                'repository': {'id': self._check('repo', repo, int)}
            }).json()['response']

    def create(self, plugin_id, repos, severity_id, **kw):
        '''
        Creates a new recast risk rule.  Either ips, uuids, or asset_list must
        be specified.
        
        + `recast-risk: create <https://docs.tenable.com/sccv/api/Recast-Risk-Rule.html#recastRiskRule_POST>`_

        Args:
            plugin_id (int): The plugin to apply the recast risk rule to.
            repos (list):
                The list of repositories to apply this recast risk rule to.
            severity_id (int):
                The new severity that vulns matching this rule should be recast
                to.  Valid values are: ``0``: Info, ``1``: Low, ``2``: Medium,
                ``3``: High, and ``4``: Critical.
            asset_list (int, optional):
                The asset list id to apply the recast risk rule to.  Please note
                that ``asset_list``, ``ips``, and ``uuids`` are mutually
                exclusive.
            comments (str, optional): 
                The comment associated to the recast risk rule.
            ips (list, optional):
                A list of IPs to apply the recast risk rule to.  Please note
                that ``asset_list``, ``ips``, and ``uuids`` are mutually
                exclusive.
            port (int, optional):  
                The port to restrict this recast risk rule to.  The default is
                unrestricted.
            protocol (int, optional): 
                The protocol to restrict the recast risk rule to.  The default
                is unrestricted.
            uuids (list, optional):
                The agent uuids to apply the recast risk rule to.  Please note
                that ``asset_list``, ``ips``, and ``uuids`` are mutually
                exclusive.

        Returns:
            dict: The newly created recast risk rule definition.

        Examples:
            Create a rule to recast 97737 on 2 IPs to informational.

            >>> rule = sc.recast_risks.create(97737, [1], 0
            ...     ips=['192.168.0.101', '192.168.0.102'])
        '''
        kw['plugin_id'] = plugin_id
        kw['repos'] = repos
        kw['severity_id'] = severity_id
        payload = self._constructor(**kw)

        return self._api.post('recastRiskRule', 
            json=payload).json()['response'][0]