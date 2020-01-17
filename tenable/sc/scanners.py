'''
scanners
========

The following methods allow for interaction into the Tenable.sc
:sc-api:`Scanner <Scanner.html>` API.  These items are typically seen under the
**Scanners** section of Tenable.sc.

Methods available on ``sc.scanners``:

.. rst-class:: hide-signature
.. autoclass:: ScannerAPI

    .. automethod:: agent_scans
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
    .. automethod:: update_status
'''
from .base import SCEndpoint
from tenable.utils import dict_merge


class ScannerAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a scanner definition document
        '''
        if 'name' in kw:
            # Validate that the name parameter is a string.
            self._check('name', kw['name'], str)

        if 'description' in kw:
            # Validate that the description parameter is a string.
            self._check('description', kw['description'], str)

        # Make sure that the appropriate authentication  type is set.
        if 'username' in kw:
            kw['authType'] = 'password'
        elif 'cert' in kw:
            kw['authType'] = 'certificate'

        if 'cert' in kw:
            # Validate that the cert parameter is a string.
            self._check('cert', kw['cert'], str)

        if 'username' in kw:
            # Validate that the username parameter is a string.
            self._check('username', kw['username'], str)

        if 'password' in kw:
            # Validate that the password parameter is a string.
            self._check('password', kw['password'], str)

        if 'address' in kw:
            # Validate that the address parameter is a string and store it
            # within the ip parameter
            kw['ip'] = self._check('address', kw['address'], str)
            del(kw['address'])

        if 'port' in kw:
            # Validate that the port parameter is a integer.
            self._check('port', kw['port'], int)

        if 'proxy' in kw:
            # Validate that the proxy parameter is a boolean flag and store it
            # as a lowercased string in useProxy.
            kw['useProxy'] = str(self._check(
                'proxy', kw['proxy'], bool)).lower()
            del(kw['proxy'])

        if 'verify' in kw:
            # Validate that the verify parameter is a boolean flag and store it
            # as a lowercased string in verifyHost.
            kw['verifyHost'] = str(self._check(
                'verify', kw['verify'], bool)).lower()
            del(kw['verify'])

        if 'enabled' in kw:
            # Validate that the enabled parameter is a boolean flag and store it
            # as a lowercased string.
            kw['enabled'] = str(self._check(
                'enabled', kw['enabled'], bool)).lower()

        if 'managed' in kw:
            # Validate that the managed parameter is a boolean flag and store it
            # as a lowercased string in managedPlugins.
            kw['managedPlugins'] = str(self._check(
                'managed', kw['managed'], bool)).lower()
            del(kw['managed'])

        if 'agent_capable' in kw:
            # Validate that the agent_capable parameter is a boolean flag and
            # store it as a lowercased string in agentCapable.
            kw['agentCapable'] = str(self._check(
                'agent_capable', kw['agent_capable'], bool)).lower()
            del(kw['agent_capable'])

        if 'zone_ids' in kw:
            # Validate that the zone_ids parameter is a list and expand it to
            # list of dictionaries with the id attribute set to each of the
            # scan zone integer ids.  Store this in the zones parameter.
            kw['zones'] = [{'id': self._check('zone:id', i, int)}
                for i in self._check('zone_id', kw['zone_ids'], list)]
            del(kw['zone_ids'])

        if 'orgs' in kw:
            # Validate that the orgs parameter is a list and expand it into a
            # list of dictionaries with the id attribute set to each of the
            # organization integer ids.  Store this in the nessusManagerOrgs
            # parameter.
            kw['nessusManagerOrgs'] = [{'id': self._check('orgs:id', i, int)}
                for i in self._check('orgs', kw['orgs'], list)]
            del(kw['orgs'])

        return kw

    def create(self, name, address, **kw):
        '''
        Creates a scanner.

        :sc-api:`scanner: create <Scanner.html#scanner_POST>`

        Args:
            address (str): The address of the scanner
            name (str): The name of the scanner
            agent_capable (bool, optional):
                Is this scanner an agent capable scanner?  If left unspecified
                the default is ``False``.
            description (str, optional):
                The description of the scanner.
            enabled (bool, optional):
                Is this scanner enabled?  If left unspecified, the default is
                ``True``.
            managed (bool, optional):
                Is the plugin set for this scanner managed?  If left unspecified
                then the default is ``False``.
            orgs (list, optional):
                If the scanner is an agent capable scanner, then a list of
                organization ids is to be specified to attach the scanner for
                the purposes of agent scanning.
            port (int, optional):
                What is the port that the Nessus service is running on.  If left
                unspecified, then the default is ``8834``.
            proxy (bool, optional):
                Is this scanner behind a proxy?  If left unspecified then the
                default is ``False``.
            zone_ids (list, optional):
                List of scan zones that this scanner is to be a member of.

        Returns:
            :obj:`dict`:
                The newly created scanner.

        Examples:
            >>> scanner = sc.scanners.create('Example Scanner', '192.168.0.1')
        '''
        payload = {
            'port': 8834,
            'proxy': False,
            'verify': False,
            'enabled': True,
            'managed': False,
            'agent_capable': False,
            'name': name,
            'address': address,
        }
        payload = self._constructor(**dict_merge(payload, kw))
        return self._api.post('scanner', json=payload).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific scanner.

        :sc-api:`scanner: details <Scanner.html#scanner_POST>`

        Args:
            id (int): The identifier for the scanner.
            fields (list, optional): A list of attributes to return.

        Returns:
            :obj:`dict`:
                The scanner resource record.

        Examples:
            >>> scanner = sc.scan_zones.details(1)
            >>> pprint(scanner)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('scanner/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def edit(self, id, **kw):
        '''
        Edits a scanner.

        :sc-api:`scanner: edit <Scanner.html#scanner_id_PATCH>`

        Args:
            id (int): The numeric identifier for the scanner.
            address (str, optional): The address of the scanner
            agent_capable (bool, optional):
                Is this scanner an agent capable scanner?  If left unspecified
                the default is ``False``.
            description (str, optional):
                The description of the scanner.
            enabled (bool, optional):
                Is this scanner enabled?  If left unspecified, the default is
                ``True``.
            managed (bool, optional):
                Is the plugin set for this scanner managed?  If left unspecified
                then the default is ``False``.
            name (str, optional): The name of the scanner
            orgs (list, optional):
                If the scanner is an agent capable scanner, then a list of
                organization ids is to be specified to attach the scanner for
                the purposes of agent scanning.
            port (int, optional):
                What is the port that the Nessus service is running on.  If left
                unspecified, then the default is ``8834``.
            proxy (bool, optional):
                Is this scanner behind a proxy?  If left unspecified then the
                default is ``False``.
            zone_ids (list, optional):
                List of scan zones that this scanner is to be a member of.

        Returns:
            :obj:`dict`:
                The newly updated scanner.

        Examples:
            >>> scanner = sc.scanners.edit(1, enabled=True)
        '''
        payload = self._constructor(**kw)
        return self._api.patch('scanner/{}'.format(id),
            json=payload).json()['response']

    def delete(self, id):
        '''
        Removes the specified scanner.

        :sc-api:`scanner: delete <Scanner.html#scanner_id_DELETE>`

        Args:
            id (int): The numeric identifier for the scanner to remove.

        Returns:
            :obj:`str`:
                An empty response.

        Examples:
            >>> sc.scanners.delete(1)
        '''
        return self._api.delete('scanner/{}'.format(
            self._check('id', id, int))).json()['response']

    def list(self, fields=None):
        '''
        Retrieves the list of scanner definitions.

        :sc-api:`scanner: list <Scanner.html#scanner_GET>`

        Args:
            fields (list, optional):
                A list of attributes to return for each scanner.

        Returns:
            :obj:`list`:
                A list of scanner resources.

        Examples:
            >>> for scanner in sc.scanners.list():
            ...     pprint(scanner)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('scanner', params=params).json()['response']

    def agent_scans(self, id, search, results=None):
        '''
        Retrieves the list of agent scans that meed the specified search
        criteria.

        :sc-api:`scanner: test-scans-query <Scanner.html#ScannerRESTReference-/scanner/{id}/testScansQuery>`

        Args:
            id (int): The numeric id of the scanner.
            search (str):
                The search string to send to the scanner.
            results (list, optonal):
                The list of results ids to test.

        Returns:
            :obj:`list`:
                The list of scans that match the search criteria.

        Examples:
            >>> scans = sc.scanners.agent_scans('*')
        '''
        payload = dict(scansGlob=self._check('search', search, str))
        if results:
            payload['resultsSync'] = [{'id': self._check('results:id', i, int)}
                for i in self._check('results', results, list)]
        return self._api.post('scanner/{}/testScansQuery'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def update_status(self):
        '''
        Starts an on-demand scanner status update.

        :sc-api:`scanner: update-status <Scanner.html#ScannerRESTReference-/scanner/updateStatus>`

        Returns:
            :obj:`list`:
                The updated scanner status for all scanners.

        Examples:
            >>> status = sc.scanners.update_status()
        '''
        return self._api.post('scanner/updateStatus',
            json={}).json()['response']['status']