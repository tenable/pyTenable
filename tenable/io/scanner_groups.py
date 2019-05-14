'''
scanner_groups
==============

The following methods allow for interaction into the Tenable.io
:devportal:`scanner-groups <scanner-groups>` API endpoints.

Methods available on ``tio.scanner_groups``:

.. rst-class:: hide-signature
.. autoclass:: ScannerGroupsAPI

    .. automethod:: add_scanner
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: delete_scanner
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
    .. automethod:: list_scanners
'''
from .base import TIOEndpoint

class ScannerGroupsAPI(TIOEndpoint):
    def add_scanner(self, group_id, scanner_id):
        '''
        Add a scanner to a scanner group.

        :devportal:`scanner-groups: add-scanner <scanner-groups-add-scanner>`

        Args:
            group_id (int):
                The unique identifier of the scanner group.
            scanner_id (int):
                The unique identifier of the scanner.

        Returns:
            :obj:`None`:
                Scanner successfully added to the scanner group.

        Examples:
            >>> tio.scanner_groups.add_scanner(1, 1)
        '''
        self._api.post('scanner-groups/{}/scanners/{}'.format(
            self._check('group_id', group_id, int),
            self._check('scanner_id', scanner_id, int)
        ))

    def create(self, name, group_type=None):
        '''
        Create a scanner group.

        :devportal:`scanner-groups: create <scanner-groups-create>`

        Args:
            name (str): The name of the scanner group to create
            group_type (str, optional):
                The type of scanner group to create.  Currently the only
                supported type is "load_balancing"

        Returns:
            :obj:`dict`:
                The scanner group resource record for the created group.

        Example:
            >>> group = tio.scanner_groups.create('Scanner Group')
        '''
        return self._api.post('scanner-groups', json={
            'name': self._check('name', name, str),
            'type': self._check('group_type', group_type, str,
                default='load_balancing', choices=['load_balancing'])
        }).json()

    def delete(self, id):
        '''
        Deletes a scanner group.

        :devportal:`scanner-groups: delete <scanner-groups-delete>`

        Args:
            id (int): The unique identifier for the scanner group to delete.

        Returns:
            :obj:`None`:
                The scanner group has been successfully deleted.

        Examples:
            >>> tio.scanner_groups.delete(1)
        '''
        self._api.delete('scanner-groups/{}'.format(self._check('id', id, int)))

    def delete_scanner(self, group_id, scanner_id):
        '''
        Removes a scanner from a scanner group.

        :devportal:`scanner-groups: delete-scanner <scanner-groups-delete-scanner>`

        Args:
            group_id (int):
                The unique identifier of the scanner group.
            scanner_id (int):
                The unique identifier of the scanner to remove from the
                requested scanner group.

        Returns:
            :obj:`None`:
                The scanner was successfully removed from the scanner group.

        Examples:
            >>> tio.scanner_groups.delete_scanner(1, 1)
        '''
        self._api.delete('scanner-groups/{}/scanners/{}'.format(
            self._check('group_id', group_id, int),
            self._check('scanner_id', scanner_id, int)
        ))

    def details(self, id):
        '''
        Retrieves the details about a scanner group.

        :devportal:`scanner-groups: details <scanner-groups-details>`

        Args:
            id (int): The unique identifier for the scanner group.

        Returns:
            :obj:`dict`:
                The scanner group resource record.

        Examples:
            >>> group = tio.scanner_groups.details(1)
            >>> pprint(group)
        '''
        return self._api.get('scanner-groups/{}'.format(
            self._check('id', id, int))).json()

    def edit(self, id, name):
        '''
        Modifies a scanner group.

        :devportal:`scanner-groups: edit <scanner-groups-edit>`

        Args:
            id (int): The unique identifier for the scanner group.
            name (str): The new name for the scanner group.

        Returns:
            :obj:`None`:
                The scanner group has been successfully updated.

        Examples:
            >>> tio.scanner_groups.edit(1, 'New Group Name')
        '''
        self._api.put('scanner-groups/{}'.format(
            self._check('id', id, int)), json={
                'name': self._check('name', name, str)
        })

    def list(self):
        '''
        Lists the configured scanner groups.

        :devportal:`scanner-groups: list <scanner-groups-list>`

        Returns:
            :obj:`list`:
                List of scanner group resource records.

        Examples:
            >>> for group in tio.scanner_groups.list():
            ...     pprint(group)
        '''
        return self._api.get('scanner-groups').json()['scanner_pools']

    def list_scanners(self, id):
        '''
        List the scanners within a specific scanner group.

        :devportal:`scanner-groups: list-scanners scanner-groups-list-scanners>`

        Args:
            id (int): The unique identifier of the scanner group.

        Returns:
            :obj:`list`:
                List of scanner resource records associated to the scanner group.

        Examples:
            >>> for scanner in tio.scanner_groups.list_scanners(1):
            ...     pprint(scanner)
        '''
        return self._api.get('scanner-groups/{}/scanners'.format(
            self._check('id', id, int))).json()['scanners']

