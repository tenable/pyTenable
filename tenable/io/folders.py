'''
folders
=======

The following methods allow for interaction into the Tenable.io 
`folders <https://cloud.tenable.com/api#/resources/folders>`_ API endpoints.

Methods available on ``tio.folders``:

.. rst-class:: hide-signature
.. autoclass:: FoldersAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: edit
    .. automethod:: list
'''
from .base import TIOEndpoint

class FoldersAPI(TIOEndpoint):
    def create(self, name):
        '''
        Create a folder.

        `folders: create <https://cloud.tenable.com/api#/resources/folders/create>`_

        Args:
            name (str):
                The name of the new folder.

        Returns:
            int: The new folder id.

        Examples:
            >>> folder = tio.folders.create('New Folder Name')
        '''
        return self._api.post('folders', json={
            'name': self._check('name', name, str)
        }).json()['id']

    def delete(self, id):
        '''
        Delete a folder.

        `folders: delete <https://cloud.tenable.com/api#/resources/folders/delete>`_

        Args:
            id (int): The unique identifier for the folder.

        Returns:
            None

        Examples:
            >>> tio.folders.delete(1)
        '''
        self._api.delete('folders/{}'.format(self._check('id', id, int)))

    def edit(self, id, name):
        '''
        Edit a folder.

        `folders: edit <https://cloud.tenable.com/api#/resources/folders/edit>`_

        Args:
            id (int): The unique identifier for the folder.
            name (str): The new name for the folder.

        Returns:
            None: The folder was successfully renamed.

        Examples:
            >>> tio.folders.edit(1, 'Updated Folder Name')
        '''
        self._api.put('folders/{}'.format(self._check('id', id, int)), json={
            'name': self._check('name', name, str)
        })

    def list(self):
        '''
        Lists the available folders.

        `folders: list <https://cloud.tenable.com/api#/resources/folders/list>`_

        Returns:
            list: List of folder resource records.

        Examples:
            >>> for folder in tio.folders.list():
            ...     pprint(folder)
        '''
        return self._api.get('folders').json()['folders']