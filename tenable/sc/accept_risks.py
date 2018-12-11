'''
accept_risks
============

NOTE: not currently tested code.

The following methods allow for interaction into the Tenable.sc 
`Accept Risk <https://docs.tenable.com/sccv/api/Accept-Risk-Rule.html>`_ API.

Methods available on ``sc.accept_risks``:

.. rst-class:: hide-signature
.. autoclass:: AcceptRiskAPI

    .. automethod:: apply
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: list
    .. automethod:: update
'''
from .base import SCEndpoint

class AcceptRiskAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        document creator for acceptRisk creation and update calls.
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
            kw['plugin'] = {'id': self._check('plugin_id', kw['plugin_id'], int)}
            del(kw['plugin_id'])

        if 'port' in kw:
            # as the port will only be passed if the default of "any" isn't
            # desired, we should check to make sure that the value passed is an
            # integer, and then convert it into a string.
            kw['protocol'] = str(self._check('port', kw['port'], int))

        if 'protocol' in kw:
            # as the protocol will only be passed if the default of "any" isn't
            # desired, we should check to make sure that the value passed is an
            # integer, and then convert it into a string.
            kw['protocol'] = str(self._check('protocol', kw['protocol'], int))

        if 'comments' in kw:
            # if a comment is attached to the rule, then lets just make sure
            # that we actually have a string here before moving on.
            self._check('comments', kw['comments'], str)

        if 'expires' in kw:
            # how many days until the accept risk rule expires?  We should
            # simply checkt o see if the value is an integer.
            self._check('expires', kw['expires'], int)

        if 'ips' in kw:
            # if the ips list is passed, then 
            kw['hostType'] = 'ip'
            kw['hostValue'] = ','.join(self._check('ips', kw['ips'], list))
            del(kw['ips'])

        if 'uuids' in kw:
            kw['hostType'] = 'uuid'
            kw['hostValue'] = ','.join(self._check('uuids', kw['uuids'], list))
            del(kw['uuids'])

        if 'asset_list' in kw:
            kw['hostType'] = 'asset'
            kw['hostValue'] = {'id': self._check('asset_list', kw['asset_list'], int)}
            del(kw['asset_list'])

        return kw

    def list(self, fields=None):
        '''
        Retreives the list of accepted risk rules.

        + `SC Accept Risk List <https://docs.tenable.com/sccv/api/Accept-Risk-Rule.html#AcceptRiskRuleRESTReference-/acceptRiskRule>`_

        Args:
            fields (list, optional): 
                A list of attributes to return for each accepted risk rule.

        Returns:
            list: A list of accepted risk rules.

        Examples:
            >>> for rule in sc.accept_risks.list():
            ...     pprint(rule)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in fields])

        return self._api.get('acceptRisk', params=params).json()['response']

    def details(self, id, fields=None):
        '''
        Retreives the details of an accepted risk rule.

        + `SC Accept Risk Details <https://docs.tenable.com/sccv/api/Accept-Risk-Rule.html#AcceptRiskRuleRESTReference-/acceptRiskRule/{id}>`_

        Args:
            id (int): The identifier for the accept risk rule.
            fields (list, optional): 
                A list of attributes to return for each accepted risk rule.

        Returns:
            dict: The accept risk rule details.

        Examples:
            >>> rule = sc.accept_risks.details(1)
            >>> pprint(rule)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in fields])

        return self._api.get('acceptRisk/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def delete(self, id):
        '''
        Removes the accepted risk rule from Tenable.sc

        + `SC Accept Risk Delete <https://docs.tenable.com/sccv/api/Accept-Risk-Rule.html#acceptRiskRule_id_DELETE>`_

        Args:
            id (int): The identifier for the accept risk rule.

        Returns:
            str: Empty string reponse from the API.

        Examples:
            >>> sc.accept_risks.delete(1)
        '''
        return self._api.delete('acceptRisk/{}'.format(
            self._check('id', id, int))).json()['response']

    def apply(self, id, repo=None):
        '''
        Applies the accept risk rule for either all repositories, or the
        repository specified.

        + `SC Accept Risk Apply <https://docs.tenable.com/sccv/api/Accept-Risk-Rule.html#AcceptRiskRuleRESTReference-/acceptRiskRule/apply>`_

        Args:
            id (int): The identifier for the accept risk rule.
            repo (int, optional):
                A specific repository to apply the rule to.  The default if not
                specified is all repositories (``0``).

        Returns:
            str: Empty string reponse from the API.

        Examples:
            >>> sc.accept_risks.apply(1)
        '''
        payload = dict()
        if repo:
            payload['repository'] = {'id': self._check('repo', repo, int)}

        return self._api.post('acceptRisk/{}/apply'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def create(self, plugin_id, repos, **kw):
        '''
        Creates a new accept risk rule.  Either ips, uuids, or asset_list must
        be specified.
        
        + `SC Accept Risk Create <https://docs.tenable.com/sccv/api/Accept-Risk-Rule.html#acceptRiskRule_POST>`_

        Args:
            plugin_id (int): The plugin to apply the accept risk rule to.
            repos (list):
                The list of repositories to apply this accept risk rule to.
            asset_list (int, optional):
                The asset list id to apply the accept risk rule to.  Please note
                that ``asset_list``, ``ips``, and ``uuids`` are mutually
                exclusive.
            comments (str, optional): 
                The comment associated to the accept risk rule.
            expires (int, optional):
                When should the rule expire?  if no expiration is set, the rule
                will never expire.
            ips (list, optional):
                A list of IPs to apply the accept risk rule to.  Please note
                that ``asset_list``, ``ips``, and ``uuids`` are mutually
                exclusive.
            port (int, optional):  
                The port to restrict this accept risk rule to.  The default is
                unrestricted.
            protocol (int, optional): 
                The protocol to restrict the accept risk rule to.  The default
                is unrestricted.
            uuids (list, optional):
                The agent uuids to apply the accept risk rule to.  Please note
                that ``asset_list``, ``ips``, and ``uuids`` are mutually
                exclusive.

        Returns:
            dict: The newly created accept risk rule definition.

        Examples:
            Create a rule to accept 97737 on 2 IPs for 90 days.

            >>> rule = sc.accept_risks.create(97737, [1],
            ...     ips=['192.168.0.101', '192.168.0.102'], expires=90)
        '''
        kw['plugin_id'] = plugin_id
        kw['repos'] = repos
        payload = self._constructor(**kw)

        return self._api.post('acceptRisk', json=payload).json()['response']

    def update(self, id, **kw):
        '''
        Creates a new accept risk rule.  Either ips, uuids, or asset_list must
        be specified.
        
        + `SC Accept Risk Create <https://docs.tenable.com/sccv/api/Accept-Risk-Rule.html#acceptRiskRule_POST>`_

        Args:
            id (int):
                The identifier for the accept risk rule.
            asset_list (int, optional):
                The asset list id to apply the accept risk rule to.  Please note
                that ``asset_list``, ``ips``, and ``uuids`` are mutually
                exclusive.
            comments (str, optional): 
                The comment associated to the accept risk rule.
            expires (int, optional):
                When should the rule expire?  if no expiration is set, the rule
                will never expire.
            ips (list, optional):
                A list of IPs to apply the accept risk rule to.  Please note
                that ``asset_list``, ``ips``, and ``uuids`` are mutually
                exclusive.
            plugin_id (int, optional): 
                The plugin to apply the accept risk rule to.
            port (int, optional):  
                The port to restrict this accept risk rule to.  The default is
                unrestricted.
            protocol (int, optional): 
                The protocol to restrict the accept risk rule to.  The default
                is unrestricted.
            repos (list):
                The list of repositories to apply this accept risk rule to.
            uuids (list, optional):
                The agent uuids to apply the accept risk rule to.  Please note
                that ``asset_list``, ``ips``, and ``uuids`` are mutually
                exclusive.

        Returns:
            dict: The newly created accept risk rule definition.

        Examples:
            Update the rule to accept 97737 on 2 IPs for 90 days.

            >>> rule = sc.accept_risks.update(1,
            ...     ips=['192.168.0.101', '192.168.0.102'], expires=90)
        '''
        payload = self._constructor(**kw)

        return self._api.patch('acceptRisk/{}'.format(
            self._check('id', id, int)), json=payload).json()['response']
