'''
Folders
=======

Methods described in this section relate to the folders API.
These methods can be accessed at ``Nessus.folders``.

.. rst-class:: hide-signature
.. autoclass:: FoldersAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from typing import List


class FoldersAPI(APIEndpoint):
    _path = 'folders'

    def create(self, name: str) -> int:
        '''
        Create a new folder

        Args:
            name (str): The name of the new folder

        Returns:
            int:
                The id for the created folder.

        Example:

            >>> id = nessus.folders.create('Example')
        '''
        return self._post(json={'name': name})['id']

    def delete(self, folder_id: int) -> None:
        '''
        Deletes a user-defined folder

        Args:
            folder_id (int): The unique identifier for the folder to delete

        Example:

            >>> nessus.folders.delete(id)
        '''
        self._delete(f'{folder_id}')

    def edit(self, folder_id: int, name: str) -> None:
        '''
        Updated the name of the specified folder.

        Args:
            folder_id (int): Unique identifier for the folder to edit
            name (str): New name for the folder

        Example:

            >>> nessus.folders.edit(id, name='New Example')
        '''
        self._put(f'{folder_id}', json={'name': name})

    def list(self) -> List:
        '''
        Gets the list of available folders

        Returns:
            List: List of folder objects

        Example:

            >>> for folder in nessus.folders.list():
            ...     print(folder)
        '''
        return self._get()['folders']