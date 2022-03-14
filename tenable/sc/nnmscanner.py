'''
NNM
========

The following methods allow for interaction into the Tenable.sc
:sc-api:`NNM <Passive-Scanner.html>` API.  These items are typically seen under the
**Passive Scanner** section of Tenable.sc.

Methods available on ``sc.nnm``:

.. rst-class:: hide-signature
.. autoclass:: NNMAPI
    :members:
'''
from .base import SCEndpoint
from tenable.utils import dict_merge


class NNMAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns an NNM definition document
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

        return kw

    def create(self, name, address, **kw):
        '''
        Creates a NNM in SC.

        :sc-api:`NNM: create <Passive-Passive-Scanner.html#passivescanner_POST>`

        Args:
            address (str): The address of the nnm
            name (str): The name of the nnm
            description (str, optional):
                The description of the nnm.
            enabled (bool, optional):
                Is this NNM enabled?  If left unspecified, the default is
                ``True``.
            port (int, optional):
                What is the port that the Nessus service is running on.  If left
                unspecified, then the default is ``8834``.
            proxy (bool, optional):
                Is this NNM behind a proxy?  If left unspecified then the
                default is ``False``.
            repository_ids (list, optional):
                Lists repository ID.
            username (str)
                Define username of NNM user.
            password (str)
                Define password of NNM user.

        Returns:
            :obj:`dict`:
                The newly created NNM.

        Examples:
            >>> nnm = sc.nnm.create('Example NNM', '192.168.0.1', username='admin', password='C0mp13xP@ss)
        '''
        payload = {
            'port': 8835,
            'proxy': False,
            'verify': False,
            'name': name,
            'address': address,
        }
        payload = self._constructor(**dict_merge(payload, kw))
        return self._api.post('passivescanner', json=payload).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific NNM.

        :sc-api:`NNM: details <Passive-Scanner.html#passivescanner_POST>`

        Args:
            id (int): The identifier for the NNM.
            fields (list, optional): A list of attributes to return.

        Returns:
            :obj:`dict`:
                The NNM resource record.

        Examples:
            >>> nnm = sc.nnm.details(1)
            >>> pprint(nnm)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('passivescanner/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def edit(self, id, **kw):
        '''
        Edits a NNM.

        :sc-api:`NNM: edit <Passive-Scanner.html#passivescanner_id_PATCH>`

        Args:
            id (int): The numeric identifier for the NNM.
            address (str, optional): The address of the NNM
            description (str, optional):
                The description of the NNM.
            enabled (bool, optional):
                Is this NNM enabled?  If left unspecified, the default is
                ``True``.
            name (str, optional): The name of the NNM.
            port (int, optional):
                What is the port that the NNM service is running on.  If left
                unspecified, then the default is ``8835``.
            proxy (bool, optional):
                Is this scanner behind a proxy?  If left unspecified then the
                default is ``False``.
            repository_ids (list, optional):
                Lists repository ID. 

        Returns:
            :obj:`dict`:
                The newly updated NNM.

        Examples:
            >>> nnm = sc.nnm.edit(1, enabled=True)
        '''
        payload = self._constructor(**kw)
        return self._api.patch('passivescanner/{}'.format(id),
            json=payload).json()['response']

    def delete(self, id):
        '''
        Removes the specified NNM.

        :sc-api:`NNM: delete <Passive-Scanner.html#passivescanner_id_DELETE>`

        Args:
            id (int): The numeric identifier for the NNM to remove.

        Returns:
            :obj:`str`:
                An empty response.

        Examples:
            >>> sc.nnm.delete(1)
        '''
        return self._api.delete('passivescanner/{}'.format(
            self._check('id', id, int))).json()['response']

    def list(self, fields=None):
        '''
        Retrieves the list of NNM definitions.

        :sc-api:`NNM: list <Passive-Scanner.html#passivescanner_GET>`

        Args:
            fields (list, optional):
                A list of attributes to return for each NNM.

        Returns:
            :obj:`list`:
                A list of NNM resources.

        Examples:
            >>> for nnm in sc.nnm.list():
            ...     pprint(nnm)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('passivescanner', params=params).json()['response']
        '''
        Returns:
            :obj:`list`:
                The list of scans that match the search criteria.
        '''
    def update_status(self):
        '''
        Starts an on-demand NNM status update.

        :sc-api:`NNM: update-status <Passive-Scanner.html#passiveScannerRESTReference-/passivescanner/updateStatus>`

        Returns:
            :obj:`list`:
                The updated NNM status for all NNM instances.

        Examples:
            >>> status = sc.nnm.update_status()
        '''
        return self._api.post('passivescanner/updateStatus',
            json={}).json()['response']['status']
