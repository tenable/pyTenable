from tenable.tenable_io.base import TIOEndpoint

class ScannerGroupsAPI(TIOEndpoint):
    def add_scanner(self, group_id, scanner_id):
        '''
        `scanner-groups: add-scanner <https://cloud.tenable.com/api#/resources/scanner-groups/add-scanner>`_

        Args:
            group_id (int):
                The unique identifier of the scanner group.
            scanner_id (int):
                The unique identifier of the scanner.

        Returns:
            None: Scanner successfully added to the scanner group.
        '''
        self._api.post('scanner-groups/{}/scanners/{}'.format(
            self._check('group_id', group_id, int),
            self._check('scanner_id', scanner_id, int)
        ))

    def create(self, name, group_type=None):
        '''
        `scanner-groups: create <https://cloud.tenable.com/api#/resources/scanner-groups/create>`_

        Args:
            name (str): The name of the scanner group to create
            group_type (str, optional):
                The type of scanner group to create.  Currently the only 
                supported type is "load_balancing"

        Returns:
            dict: The scanner group resouce record for the created group.
        '''
        return self._api.post('scanner-groups', json={
            'name': self._check('name', name, str),
            'type': self._check('group_type', group_type, str, 
                default='load_balancing', choices=['load_balancing'])
        }).json()

    def delete(self, id):
        '''
        `scanner-groups: delete <https://cloud.tenable.com/api#/resources/scanner-groups/delete>`_

        Args:
            id (int): The unique identifier for the scanner group to delete.

        Returns:
            None: The scanner group has been successfully deleted.
        '''
        self._api.delete('scanner-groups/{}'.format(self._check('id', id, int)))

    def delete_scanner(self, group_id, scanner_id):
        '''
        `scanner-groups: delete-scanner <https://cloud.tenable.com/api#/resources/scanner-groups/delete-scanner>`_

        Args:
            group_id (int): 
                The unique identifier of the scanner group.
            scanner_id (int):
                The unique identifier of the scanner to remove from the
                requested scanner group.

        Returns:
            None: The scanner was successfully removed from the scanner group.
        '''
        self._api.delete('scanner-groups/{}/scanners/{}'.format(
            self._check('group_id', group_id, int),
            self._check('scanner_id', scanner_id, int)
        ))

    def details(self, id):
        '''
        `scanner-groups: details <https://cloud.tenable.com/api#/resources/scanner-groups/details>`_

        Args:
            id (int): The unique identifier for the scanner group.

        Returns:
            dict: The scanner group resource record.
        '''
        return self._api.get('scanner-groups/{}'.format(
            self._check('id', id, int))).json()

    def edit(self, id, name):
        '''
        `scanner-groups: edit <https://cloud.tenable.com/api#/resources/scanner-groups/edit>`_

        Args:
            id (int): The unique identifier for the scanner group.
            name (str): The new name for the scanner group.

        Returns:
            None: The scanner group has been successfully updated.
        '''
        self._api.put('scanner-groups/{}'.format(
            self._check('id', id, int)), json={
                'name': self._check('name', name, str)
        })

    def list(self):
        '''
        `scanner-groups: list <https://cloud.tenable.com/api#/resources/scanner-groups/list>`_

        Returns:
            list: List of scanner group resource records.
        '''
        return self._api.get('scanner-groups').json()['scanner_pools']

    def list_scanners(self, id):
        '''
        `scanner-groups: list-scanners <https://cloud.tenable.com/api#/resources/scanner-groups/list-scanners>`_

        Args:
            id (int): The unique identifier of the scanner group.

        Returns:
            list: 
                List of scanner resource records associated to the scanner group.
        '''
        return self._api.get('scanner-groups/{}/scanners'.format(
            self._check('id', id, int))).json()['scanners']
    
