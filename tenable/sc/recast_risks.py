'''
Recast Risks
============

The following methods allow for interaction into the Tenable Security Center
:sc-api:`Recast Risk <Recast-Risk-Rule.htm>` API.

Methods available on ``sc.recast_risks``:

.. rst-class:: hide-signature
.. autoclass:: RecastRiskAPI
    :members:
'''
from .base import SCEndpoint


class RecastRiskAPI(SCEndpoint):
    def _constructor(self, **kwargs):
        '''
        document creator for recastRisk creation and update calls.
        '''
        if 'repos' in kwargs:
            # as repositories are passed in the API as a series of sub-documents
            # with the ID attribute set, we will convert the simply list that
            # was passed to us into a series of documents as the API expects.
            kwargs['repositories'] = [{'id': self._check('repo:id', r, int)}
                                      for r in self._check('repos', kwargs['repos'], list)]
            del kwargs['repos']

        if 'plugin_id' in kwargs:
            # the plugin parameter
            kwargs['plugin'] = {
                'id': str(self._check('plugin_id', kwargs['plugin_id'], int))}
            del kwargs['plugin_id']

        if 'port' in kwargs:
            # as the port will only be passed if the default of "any" isn't
            # desired, we should check to make sure that the value passed is an
            # integer, and then convert it into a string.
            kwargs['port'] = str(self._check('port', kwargs['port'], int))

        if 'protocol' in kwargs:
            # as the protocol will only be passed if the default of "any" isn't
            # desired, we should check to make sure that the value passed is an
            # integer, and then convert it into a string.
            kwargs['protocol'] = str(self._check('protocol', kwargs['protocol'], int))

        if 'comments' in kwargs:
            # if a comment is attached to the rule, then lets just make sure
            # that we actually have a string here before moving on.
            self._check('comments', kwargs['comments'], str)

        if 'severity_id' in kwargs:
            # What should be the new severity id for the vulnerabilities
            # matching the rule?  Converts severity_id to a newSeverity document
            # with an id parameter matching the id passed.
            kwargs['newSeverity'] = {'id': self._check(
                'severity_id', kwargs['severity_id'], int, choices=[0, 1, 2, 3, 4])}
            del kwargs['severity_id']

        if 'ips' in kwargs:
            # if the ips list is passed, then
            kwargs['hostType'] = 'ip'
            kwargs['hostValue'] = ','.join([self._check('ip:item', i, str)
                                            for i in self._check('ips', kwargs['ips'], list)])
            del kwargs['ips']

        if 'uuids' in kwargs:
            kwargs['hostType'] = 'uuid'
            kwargs['hostValue'] = ','.join([self._check('uuid:item', i, str)
                                            for i in self._check('uuids', kwargs['uuids'], list)])
            del kwargs['uuids']

        if 'asset_list' in kwargs:
            kwargs['hostType'] = 'asset'
            kwargs['hostValue'] = {'id': self._check('asset_list', kwargs['asset_list'], int)}
            del kwargs['asset_list']

        return kwargs

    def list(self, repo_ids=None, plugin_id=None, port=None,
             org_ids=None, fields=None):
        '''
        Retrieves the list of recasted risk rules.

        :sc-api:`recast-risk: list <Recast-Risk-Rule.htm#RecastRiskRuleRESTReference-/recastRiskRule>`

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
            :obj:`list`:
                A list of recast risk rules.

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
            params['organizationIDs'] = ','.join([str(self._check('org:id', i, int))
                                                  for i in self._check('org_ids', org_ids, list)])

        if repo_ids:
            # validating that repo_ids is a list of integer values, then
            # converting the result into a comma-seperated string and assigning
            # it to the appropriate query parameter.
            params['repositoryIDs'] = ','.join([str(self._check('repo:id', i, int))
                                                for i in self._check('repo_ids', repo_ids, list)])

        return self._api.get('recastRiskRule', params=params).json()['response']

    def details(self, risk_id, fields=None):
        '''
        Retrieves the details of an recast risk rule.

        :sc-api:`recast-risk: details <Recast-Risk-Rule.htm#RecastRiskRuleRESTReference-/recastRiskRule/{id}>`

        Args:
            risk_id (int): The identifier for the recast risk rule.
            fields (list, optional):
                A list of attributes to return for each recast risk rule.

        Returns:
            :obj:`dict`:
                The recast risk rule details.

        Examples:
            >>> rule = sc.recast_risks.details(1)
            >>> pprint(rule)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                                         for f in fields])

        return self._api.get('recastRiskRule/{}'.format(self._check('risk_id', risk_id, int)),
                             params=params).json()['response']

    def delete(self, risk_id):
        '''
        Removes the recast risk rule from Tenable Security Center

        :sc-api:`recast-risk: delete <Recast-Risk-Rule.htm#recastRiskRule_id_DELETE>`

        Args:
            risk_id (int): The identifier for the recast risk rule.

        Returns:
            :obj:`str`:
                Empty string response from the API.

        Examples:
            >>> sc.recast_risks.delete(1)
        '''
        return self._api.delete('recastRiskRule/{}'.format(
            self._check('risk_id', risk_id, int))).json()['response']

    def apply(self, risk_id, repo):
        '''
        Applies the recast risk rule for either all repositories, or the
        repository specified.

        :sc-api:`recast-risk: apply <Recast-Risk-Rule.htm#RecastRiskRuleRESTReference-/recastRiskRule/apply>`

        Args:
            risk_id (int): The identifier for the recast risk rule.
            repo (int, optional):
                A specific repository to apply the rule to.  The default if not
                specified is all repositories (``0``).

        Returns:
            :obj:`str`:
                Empty string response from the API.

        Examples:
            >>> sc.recast_risks.apply(1)
        '''
        return self._api.post('recastRiskRule/{}/apply'.format(
            self._check('risk_id', risk_id, int)), json={
            'repository': {'id': self._check('repo', repo, int)}
        }).json()['response']

    def create(self, plugin_id, repos, severity_id, **kwargs):
        '''
        Creates a new recast risk rule.  Either ips, uuids, or asset_list must
        be specified.

        :sc-api:`recast-risk: create <Recast-Risk-Rule.htm#recastRiskRule_POST>`

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
            :obj:`dict`:
                The newly created recast risk rule definition.

        Examples:
            Create a rule to recast 97737 on 2 IPs to informational.

            >>> rule = sc.recast_risks.create(97737, [1], 0
            ...     ips=['192.168.0.101', '192.168.0.102'])
        '''
        kwargs['plugin_id'] = plugin_id
        kwargs['repos'] = repos
        kwargs['severity_id'] = severity_id
        payload = self._constructor(**kwargs)

        return self._api.post('recastRiskRule',
                              json=payload).json()['response'][0]
