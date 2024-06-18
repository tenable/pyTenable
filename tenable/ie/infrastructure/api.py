'''
Infrastructure
==============

Methods described in this section relate to the infrastructure API.
These methods can be accessed at ``TenableIE.infrastructure``.

.. rst-class:: hide-signature
.. autoclass:: InfrastructureAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.infrastructure.schema import InfrastructureSchema
from tenable.base.endpoint import APIEndpoint


class InfrastructureAPI(APIEndpoint):
    _path = 'infrastructures'
    _schema = InfrastructureSchema()

    def list(self) -> List[Dict]:
        '''
        Retrieves the list of infrastructures.

        Returns:
            list:
                List of infrastructure instances.

        Examples:

            >>> tie.infrastructure.list()
        '''
        return self._schema.load(self._get(), many=True)

    def create(self, name: str, login: str, password: str) -> List[Dict]:
        '''
        Creates a new infrastructure instance with inputs of name, username
        and password.

        Args:
            name (str):
                The new name for the infrastructure instance.
            login (str):
                The login name for the infrastructure instance.
            password (str):
                The password for the infrastructure instance.

        Returns:
            list:
                Newly created infrastructure instance.

        Examples:

            >>> tie.infrastructure.create(
            ...     name='test_user',
            ...     login='test_user@gmail.com',
            ...     password='tenable.ad'))
        '''
        payload = [
            self._schema.dump(self._schema.load({
                'name': name,
                'login': login,
                'password': password
            }))
        ]
        return self._schema.load(self._post(json=payload), many=True)

    def details(self, infrastructure_id: str) -> Dict:
        '''
        Gets the details of particular infrastructure instance.

        Args:
            infrastructure_id (str):
                The infrastructure instance identifier.

        Returns:
            dict:
                Details of particular ``infrastructure_id``.

        Examples:

            >>> tie.infrastructure.details(infrastructure_id='1')
        '''
        return self._schema.load(self._get(f'{infrastructure_id}'))

    def update(self, infrastructure_id: str, **kwargs) -> Dict:
        '''
        Updates the infrastructure of the specific infrastructure instance.

        Args:
            infrastructure_id (str):
                The infrastructure instance identifier.
            name (optional, str):
                New name to be updated.
            login (optional, str):
                New login name to be updated.
            password (optional, str):
                New password to be updated.

        Returns:
            dict:
                Updated infrastructure instance.

        Examples:

            >>> tie.infrastructure.update(
            ...     infrastructure_id='1',
            ...     login='updated_login@tenable.com',
            ...     name='updated_user')
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(
            self._patch(f'{infrastructure_id}', json=payload))

    def delete(self, infrastructure_id: str):
        '''
        Deletes the particular infrastructure instance.

        Args:
            infrastructure_id (str):
                The infrastructure instance identifier.

        Returns:
            None:

        Examples:

            >>> tie.infrastructure.delete(infrastructure_id='1')
        '''
        return self._schema.load(self._delete(f'{infrastructure_id}'),
                                 many=True)
