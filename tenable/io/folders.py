'''
folders
=======

The following methods allow for interaction into the Tenable.io
:devportal:`folders <folders>` API endpoints.

Methods available on ``tio.folders``:

.. rst-class:: hide-signature
.. autoclass:: FoldersAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: edit
    .. automethod:: list
'''
from typing import List, ClassVar
from .base import TIOEndpoint

class FoldersAPI(TIOEndpoint):
    _path: ClassVar[str] = 'folders'

    def create(
            self,
            name: str
    ) -> int:
        '''
        Create a folder.

        :devportal:`folders: create <folders-create>`

        Args:
            name (str):
                The name of the new folder.

        Returns:
            :obj:`int`:
                The new folder id.

        Examples:
            >>> folder = tio.folders.create('New Folder Name')
        '''
        payload = {'name': self._check('name', name, str)}
        return self._api.post(self._path, json=payload).json()['id']

    def delete(
            self,
            id: int
    ) -> None:
        '''
        Delete a folder.

        :devportal:`folders: delete <folders-delete>`

        Args:
            id (int): The unique identifier for the folder.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.folders.delete(1)
        '''
        self._check('id', id, int)
        self._api.delete(f'{self._path}/{id}')

    def edit(
            self,
            id: int,
            name: str
    ) -> None:
        '''
        Edit a folder.

        :devportal:`folders: edit <folders-edit>`

        Args:
            id (int): The unique identifier for the folder.
            name (str): The new name for the folder.

        Returns:
            :obj:`None`:
                The folder was successfully renamed.

        Examples:
            >>> tio.folders.edit(1, 'Updated Folder Name')
        '''
        self._check('id', id, int)
        payload = {'name': self._check('name', name, str)}
        self._api.put(f'{self._path}/{id}', json=payload)

    def list(self) -> List:
        '''
        Lists the available folders.

        :devportal:`folders: list <folders-list>`

        Returns:
            :obj:`list`:
                List of folder resource records.

        Examples:
            >>> for folder in tio.folders.list():
            ...     pprint(folder)
        '''
        return self._api.get(self._path).json()['folders']
