'''
Folders
=======

The following methods allow for interaction into the Tenable.io
:devportal:`folders <folders>` API endpoints.

Methods available on ``tio.v3.vm.folders``:

.. rst-class:: hide-signature
.. autoclass:: FoldersAPI
    :members:
'''
from typing import List

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.vm.folders.schema import FolderSchema


class FoldersAPI(ExploreBaseEndpoint):

    _path = 'api/v3/scans/folders'
    _conv_json = True
    _schema = FolderSchema()

    def create(self, name: str) -> int:
        '''
        Create a folder.

        :devportal:`folders: create <folders-create>`

        Args:
            name (str): The name of the new folder.

        Returns:
            :obj:`int`:
                The new folder id.

        Examples:
            >>> folder = tio.v3.vm.folders.create('New Folder Name')
        '''
        payload = self._schema.dump(self._schema.load({'name': name}))
        return self._post(json=payload)['id']

    def delete(self, id: int) -> None:
        '''
        Delete a folder.

        :devportal:`folders: delete <folders-delete>`

        Args:
            id (int): The unique identifier for the folder.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.vm.folders.delete(1)
        '''
        self._delete(f'{id}')

    def edit(self, id: int, name: str) -> None:
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
            >>> tio.v3.vm.folders.edit(1, 'Updated Folder Name')
        '''
        payload = self._schema.dump(self._schema.load({'name': name}))
        self._put(f'{id}', json=payload)

    def search(self, **kwargs) -> List:
        '''
        Searches from the available folders.

        :devportal:`folders: search <folders-search>`

        Returns:
            :obj:`list`: List of folder resource records.

        Examples:
            >>> for folder in tio.v3.vm.folders.list():
            ...     pprint(folder)
        '''
        raise NotImplementedError(
            'This method will be updated once ExploreSearchIterator is \
                implemented for v3'
        )
