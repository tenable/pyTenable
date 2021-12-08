'''
Folders
========

The following methods allow for interaction into the Tenable.io
:devportal:`Web Application Scanning v3 folders <was-v2-folders>` API.

Methods available on ``tio.v3.was.folders``:

.. rst-class:: hide-signature
.. autoclass:: FoldersAPI
    :members:
'''
import uuid
from typing import Dict, List

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class FoldersAPI(ExploreBaseEndpoint):
    _path = 'api/v3/was/folders'
    _conv_json = True

    def create(self, name: str) -> Dict:
        '''
        Create a folder.

        :devportal:`was folders: create <was-v2-folders-create>`

        Args:
            name:
                The name of the new folder.

        Returns:
            :obj:`dict`:
                The resource record of the newly created folder.

        Examples:
            >>> folder = tio.v3.was.folders.create('New Folder Name')
        '''
        return self._post(json={'name': name})

    def delete(self, id: uuid.UUID) -> None:
        '''
        Delete a folder.

        :devportal:`was folders: delete <was-v2-folders-delete>`

        Args:
            id: The unique identifier for the folder.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.was.folders.delete('91843ecb-ecb8-48a3-b623-d4682c28c')
        '''
        self._delete(f'{id}')

    def edit(self, id: uuid.UUID, name: str) -> Dict:
        '''
        Edit a folder.

        :devportal:`was folders: edit <was-v2-folders-update>`

        Args:
            id: The unique identifier for the folder.
            name: The new name for the folder.

        Returns:
            :obj:`dict`:
                The resource record of the updated folder.

        Examples:
            >>> tio.v3.was.folders.edit('91843ecb-ecb8-48a3-b623-d4682c2594',
            ...     'Updated Folder Name')
        '''
        return self._put(f'{id}', json={'name': name})

    def list(self) -> List:
        '''
        Lists the available folders.

        :devportal:`was folders: list <was-v2-folders-list>`

        Returns:
            :obj:`list`:
                List of folder resource records.

        Examples:
            >>> for folder in tio.v3.was.folders.list():
            ...     pprint(folder)
        '''
        return self._get()
