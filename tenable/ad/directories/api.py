'''
'''
from typing import List, Dict
from tenable.base.endpoint import APIEndpoint
from .schema import DirectorySchema


class DirectoriesAPI(APIEndpoint):
    _path = 'directories'

    def list(self) -> List:
        '''
        Retrieve all directory instances

        Returns:
            list:
                The list of directory objects

        Examples:

            >>> tad.directories.list()
        '''
        schema = DirectorySchema()
        return schema.load(self._get(), many=True)

    def create(self,
               infrastructure_id: int,
               name: str,
               ip: str,
               directory_type: str,
               dns: str,
               ldap_port: int = 389,
               global_catalog_port: int = 3268,
               smb_port: int = 445,
               ) -> Dict:
        '''
        Create a new directory instance

        Args:
            infrastructure_id:
                The infrastructure object to bind this directory to.
            name:
                Name of the directory instance.
            ip:
                The IP Address of the directory server.
            directory_type:
                ???
            dns:
                The DNS domain that this directory is tied to.
            ldap_port:
                The port number associated to the LDAP service on the directory
                server.
            global_catalog_port:
                The port number associated to the Global Catalog service
                running on the directory server.
            smb_port:
                The port number associated to the Server Messaging Block (SMB)
                service running on the directory server.

        Returns:
            dict:
                The created directory instance.

        Examples:

            >>> tad.directories.create(
            ...     infrastructure_id=1,
            ...     name='ExampleServer',
            ...     ip='172.16.0.1',
            ...     directory_type='????',
            ...     dns='company.tld',
            ...     )
        '''
        schema = DirectorySchema()
        payload = schema.dump(schema.load({
            'infrastructureId': infrastructure_id,
            'name': name,
            'ip': ip,
            'type': directory_type,
            'dns': dns,
            'ldapPort': ldap_port,
            'globalCatalogPort': global_catalog_port,
            'smbPort': smb_port,
        }))
        return schema.load(self._post(json=payload))

    def details(self, directory_id: int) -> Dict:
        '''
        Retrieves the details for a specific directory instance.

        Args:
            directory_id: The directory instance identifier.

        Returns:
            dict:
                the directory object.

        Examples:

            >>> tad.directories.details(1)
        '''
        return self._get(directory_id)

    def update(self,
               infrastructure_id: int,
               directory_id: int,
               **kwargs
               ) -> Dict:
        '''
        '''
        schema = DirectorySchema()
        payload = schema.dump(schema.load(kwargs))
        return schema.load(
            self._api.patch((f'infrastructures/{infrastructure_id}'
                             f'/directories/{directory_id}'),
                            json=payload))

    def delete(self, infrastructure_id: int, directory_id: int) -> None:
        '''
        '''
        self._api.delete((f'infrastructures/{infrastructure_id}'
                          f'/directories/{directory_id}'))

    # NOTE: Get All Directories for a Given Infrastructure is located within
    #       the infrastructures module.
    #
    # NOTE: Get Directory instance by id is located within the infrastructures
    #       module.
