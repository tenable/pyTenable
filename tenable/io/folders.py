from tenable.tenable_io.base import TIOEndpoint

class FoldersAPI(TIOEndpoint):
    def create(self, name):
        '''
        `folders: create <https://cloud.tenable.com/api#/resources/folders/create>`_

        Args:
            name (str):
                The name of the new folder.

        Returns:
            int: The new folder id.
        '''
        return self._api.post('folders', json={
            'name': self._check('name', name, str)
        }).json()['id']

    def delete(self, id):
        '''
        `folders: delete <https://cloud.tenable.com/api#/resources/folders/delete>`_

        Args:
            id (int): The unique identifier for the folder.

        Returns:
            None
        '''
        self._api.delete('folders/{}'.format(self._check('id', id, int)))

    def edit(self, id, name):
        '''
        `folders: edit <https://cloud.tenable.com/api#/resources/folders/edit>`_

        Args:
            id (int): The unique identifier for the folder.
            name (str): The new name for the folder.

        Returns:
            None: The folder was successfully renamed.
        '''
        self._api.put('folders/{}'.format(self._check('id', id, int)), json={
            'name': self._check('name', name, str)
        })

    def list(self):
        '''
        `folders: list <https://cloud.tenable.com/api#/resources/folders/list>`_

        Returns:
            list: List of folder resource records.
        '''
        return self._api.get('folders').json()['folders']