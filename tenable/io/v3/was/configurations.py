'''
Configurations
========

The following methods allow for interaction into the Tenable.io
:devportal:`configurations <was-v2-configurations>` API.

Methods available on ``tio.v3.was.configurations``:

.. rst-class:: hide-signature
.. autoclass:: FoldersAPI
    :members:
'''
from typing import Dict, List, Union
from uuid import UUID

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class ConfigurationsAPI(ExploreBaseEndpoint):
    _path = 'api/v3/was/configs'
    _conv_json = True

    def create(
        self,
        name: str,
        targets: List[str],
        template_id: str,
        settings: Dict,
        **kw
    ) -> Dict:
        '''
        Create a folder.

        :devportal:`folders: create <folders-create>`

        Args:
            name:
                The name of the new folder.

        Returns:
            :obj:`dict`:
                The resource record of the newly created folder.

        Examples:
            >>> folder = tio.v3.was.folders.create('New Folder Name')
        '''
        return self._post('webapp', json={'name': name})

    def details(self, obj_id: Union[str, UUID]) -> Dict:
        '''
        '''

        return self._get(obj_id)
    # def search(
    #         self,
    #         *,
    #         fields: Optional[List[str]] = None,
    #         sort: Optional[List[Dict]] = None,
    #         filter: Optional[Dict] = None, limit: int = 1000,
    #         next: Optional[str] = None, return_resp: bool = False,
    #         iterator_cls=None,
    #         schema_cls: Optional[Type[SearchSchema]] = None,
    #         **kwargs
    # ):
    #     '''
    #     '''
    #     raise NotImplementedError("Search is yet to be implemented")

    # def update(
    #     self,
    #     config_id: UUID
    # )
    def delete(self, id: UUID) -> None:
        '''
        Delete a folder.

        :devportal:`folders: delete <folders-delete>`

        Args:
            id: The unique identifier for the folder.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.was.folders.delete('91843ecb-ecb8-48a3-b623-d4682c28c')
        '''
        self._delete('{}/webapp'.format(id))

    def edit(self, id: UUID, name: str) -> Dict:
        '''
        Edit a folder.

        :devportal:`folders: edit <folders-edit>`

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
        return self._put('{}/webapp'.format(id), json={'name': name})

    def list(self) -> List:
        '''
        Lists the available folders.

        :devportal:`folders: list <folders-list>`

        Returns:
            :obj:`list`:
                List of folder resource records.

        Examples:
            >>> for folder in tio.v3.was.folders.list():
            ...     pprint(folder)
        '''
        return self._get('webapp')
