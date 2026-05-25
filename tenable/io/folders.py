"""
Folders
=======

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`folders <folders>` API endpoints.

Methods available on ``tio.folders``:

.. rst-class:: hide-signature
.. autoclass:: FoldersAPI
    :members:
"""

from tenable.utils import scrub

from .base import TIOEndpoint


class FoldersAPI(TIOEndpoint):
    def create(self, name):
        """
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
        """
        return self._api.post('folders', json={'name': str(name)}).json()['id']

    def delete(self, id):
        """
        Delete a folder.

        :devportal:`folders: delete <folders-delete>`

        Args:
            id (int): The unique identifier for the folder.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.folders.delete(1)
        """
        self._api.delete(f'folders/{scrub(id)}')

    def edit(self, id, name):
        """
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
        """
        self._api.put(f'folders/{scrub(id)}', json={'name': str(name)})

    def list(self):
        """
        Lists the available folders.

        :devportal:`folders: list <folders-list>`

        Returns:
            :obj:`list`:
                List of folder resource records.

        Examples:
            >>> for folder in tio.folders.list():
            ...     pprint(folder)
        """
        return self._api.get('folders').json()['folders']
