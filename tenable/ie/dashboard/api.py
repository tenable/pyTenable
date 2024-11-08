'''
Dashboard
=========

Methods described in this section relate to the dashboard API.
These methods can be accessed at ``TenableIE.dashboard``.

.. rst-class:: hide-signature
.. autoclass:: DashboardAPI
    :members:
'''
from typing import List, Dict
from tenable.ie.dashboard.schema import DashboardSchema
from tenable.base.endpoint import APIEndpoint


class DashboardAPI(APIEndpoint):
    _path = 'dashboards'
    _schema = DashboardSchema()

    def list(self) -> List[Dict]:
        '''
        Retrieve all dashboard instances.

        Returns:
            list:
                The list of dashboard objects.

        Examples:

            >>> tie.dashboard.list()
        '''
        return self._schema.load(self._get(), many=True)

    def create(self, name: str, order: int) -> Dict:
        '''
        Create a new dashboard instance.

        Args:
            name (str):
                The name of the new dashboard.
            order (int):
                order of the dashboard.

        Returns:
            dict:
                The created dashboard instance.

        Examples:

            >>> tie.dashboard.create(
            ...     name='new_dashboard',
            ...     order=10)
        '''
        payload = {
            'name': name,
            'order': order
        }
        return self._schema.load(self._post(json=payload))

    def details(self, dashboard_id: str) -> Dict:
        '''
        Retrieves the details for a specific dashboard instance.

        Args:
            dashboard_id (str):
                The dashboard instance identifier.

        Returns:
            dict:
                The details of the dashboard object of specified dashboard_id.

        Examples:

            >>> tie.dashboard.details(dashboard_id='1')
        '''
        return self._schema.load(self._get(f'{dashboard_id}'))

    def update(self, dashboard_id: str, **kwargs):
        '''
        Updates the dashboard instance based on ``dashboard_id``.

        Args:
            dashboard_id (str):
                The dashboard instance identifier.
            name (optional, str):
                The updated name.
            order (optional, int):
                The order of the dashboard.

        Examples:

            >>> tie.dashboard.update(
            ...     dashboard_id='23',
            ...     name='updated_dashboard_name',
            ...     order=1)
        '''
        payload = self._schema.dump(self._schema.load(kwargs))
        return self._schema.load(
            self._patch(f'{dashboard_id}', json=payload),
            many=True)

    def delete(self, dashboard_id: str) -> None:
        '''
        Deletes the dashboard instance

        Args:
            dashboard_id (str):
                The dashboard instance identifier.

        Examples:
            >>> tie.dashboard.delete(dashboard_id='22')
        '''
        self._delete(f'{dashboard_id}')
