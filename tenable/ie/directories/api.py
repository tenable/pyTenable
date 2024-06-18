'''
Directory
=========

Methods described in this section relate to the directory API.
These methods can be accessed at ``TenableIE.directories``.

.. rst-class:: hide-signature
.. autoclass:: DirectoriesAPI
    :members:
'''
from typing import List, Dict
from restfly.utils import dict_clean
from tenable.base.endpoint import APIEndpoint
from .schema import DirectorySchema


class DirectoriesAPI(APIEndpoint):
    _path = 'directories'
    _schema = DirectorySchema()

    def list(self) -> List[Dict]:
        '''
        Retrieves all directory instances.

        Returns:
            list:
                The list of directory objects

        Examples:

            >>> tie.directories.list()
        '''
        return self._schema.load(self._get(), many=True)

    def create(self,
               infrastructure_id: int,
               name: str,
               ip: str,
               dns: str,
               **kwargs
               ) -> List[Dict]:
        '''
        Creates a new directory instance.

        Args:
            infrastructure_id (int):
                The infrastructure object to bind this directory to.
            name (str):
                Name of the directory instance.
            ip (str):
                The IP Address of the directory server.
            dns (str):
                The DNS domain that this directory is tied to.
            directory_type (optional, str):
                The directory's type.
            ldap_port (optional, str):
                The port number associated to the LDAP service on the
                directory server.
            global_catalog_port (optional, str):
                The port number associated to the Global Catalog service
                running on the directory server.
            smb_port (optional, str):
                The port number associated to the Server Messaging
                Block (SMB) service running on the directory server.

        Returns:
            dict:
                The created directory instance.

        Examples:
            >>> tie.directories.create(
            ...     infrastructure_id=1,
            ...     name='ExampleServer',
            ...     ip='172.16.0.1',
            ...     directory_type='????',
            ...     dns='company.tld',
            ...     )
        '''
        payload = [self._schema.dump(self._schema.load(
            dict_clean({
                'infrastructureId': infrastructure_id,
                'name': name,
                'ip': ip,
                'type': kwargs.get('directory_type'),
                'dns': dns,
                'ldapPort': kwargs.get('ldap_port'),
                'globalCatalogPort': kwargs.get('global_catalog_port'),
                'smbPort': kwargs.get('smb_port')
            })
        ))]
        return self._schema.load(self._post(json=payload), many=True)

    def details(self, directory_id: str) -> Dict:
        '''
        Retrieves the details for a specific directory instance.

        Args:
            directory_id (str): The directory instance identifier.

        Returns:
            dict:
                the directory object.

        Examples:
            >>> tie.directories.details(directory_id='1')
        '''
        return self._schema.load(self._get(f'{directory_id}'))

    def update(self,
               infrastructure_id: int,
               directory_id: int,
               **kwargs
               ) -> Dict:
        '''
        Updates the directory instance based on infrastrcture_id and
        directory_id.

        Args:
            infrastructure_id (int):
                The infrastructure instance identifier.
            directory_id (int):
                The directory instance identifier.
            name (optional, str):
                Name of the directory instance.
            ip (optional, str):
                The IP Address of the directory server.
            directory_type (optional, str):
                The directory's type.
            dns (optional, str):
                The DNS domain that this directory is tied to.
            ldap_port (optional, int):
                The port number associated to the LDAP service on the
                directory server.
            global_catalog_port (optional, str):
                The port number associated to the Global Catalog service
                running on the directory server.
            smb_port (optional, str):
                The port number associated to the Server Messaging
                Block (SMB) service running on the directory server.

        Returns:
            dict:
                The updated directory object.

        Examples:
            >>> tie.directories.update(
            ...     infrastructure_id=2,
            ...     directory_id=9,
            ...     name='updated_new_name'
            ...     )

            >>> tie.directories.update(
            ...     infrastructure_id=2,
            ...     directory_id=9,
            ...     name='updated_new_name',
            ...     ldap_port=390
            ...     )
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(
            self._api.patch((f'infrastructures/{infrastructure_id}'
                             f'/directories/{directory_id}'),
                            json=payload))

    def delete(self, infrastructure_id: int, directory_id: int) -> None:
        '''
        Deletes the directory instance.

        Args:
            infrastructure_id (int):
                The infrastructure instance identifier.
            directory_id (int):
                The directory instance identifier.

        Returns:
            None:

        Examples:
            >>> tie.directories.delete(
            ...     infrastructure_id=2,
            ...     directory_id='12'
            ...     )
        '''
        self._api.delete((f'infrastructures/{infrastructure_id}'
                          f'/directories/{directory_id}'))

    # NOTE: Get All Directories for a Given Infrastructure is located within
    #       the infrastructures module.
    #
    # NOTE: Get Directory instance by id is located within the infrastructures
    #       module.
