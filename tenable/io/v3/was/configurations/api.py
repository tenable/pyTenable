'''
Configurations
==============

The following methods allow for interaction with Tenable.io
:devportal:`configurations <was-v2-configurations>` API.

Methods available on ``tio.v3.was.configurations``:

.. rst-class:: hide-signature
.. autoclass:: ConfigurationsAPI
    :members:
'''
from typing import Dict, List, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.was_iterator import (CSVChunkIterator,
                                                       SearchIterator)
from tenable.io.v3.base.schema.explore.search import SortType
from tenable.io.v3.was.configurations.schema import ConfigurationSchema


class ConfigurationsAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Configurations API
    '''

    _path = 'api/v3/was/configs'
    _conv_json = True
    _schema = ConfigurationSchema()

    def create(self,
               name: str,
               owner_id: UUID,
               template_id: UUID,
               targets: List[str],
               settings: Dict,
               **kw
               ) -> Dict:
        '''
        Create a scan configuration.

        :devportal:`configuration: create <was-v2-config-create>`

        Args:
            name (str):
                The name of the scan configuration.
            owner_id (uuid.UUID):
                The UUID of the owner of the scan configuration.
            template_id (uuid.UUID):
                The UUID of the Tenable-provided configuration template.
            targets (list[str]):
                A List of distinct absolute URLs that were targeted in the
                scan.
            settings (dict):
                The scan configuration settings.
            description (str):
                A description of the scan configuration.
            folder_id (str):
                The UUID of the folder to assign for the scan configuration.
            user_template_id (str):
                The UUID of the user-defined configuration template from which
                this configuration is derived.
            scanner_id (int):
                The ID of the scanner (if the type is set to managed_webapp),
                or scanner group (if the type is pool or local) that performs
                the scan.
            schedule (dict):
                The schedule when the scan configuration will be run.
            notifications (dict):
                Contact information used to send scan notifications
                upon scan completion.
            permissions (list):
                The permissions for the scan configuration.

        Returns:
            :obj:`dict`:
                The resource record of the newly created scan configuration.

        Examples:
            >>> configuration_settings = {
            ...     'description': 'Test Security Scan Configuration'
            ... }
            >>> targets = [
            ...     'https://example.com',
            ...     'https://example1.com'
            ... ]
            >>> scan_configuration = tio.v3.was.configurations.create(
            ...     'New Scan Configuration Name',
            ...     '00000000-0000-0000-0000-000000000000',
            ...     settings=configuration_settings,
            ...     targets=targets,
            ...     template_id='00000000-0000-0000-0000-000000000000'
            ... )
        '''
        payload = {
            'name': name,
            'owner_id': owner_id,
            'template_id': template_id,
            'targets': targets,
            'settings': settings
        }
        payload.update(kw)

        payload = self._schema.dump(self._schema.load(payload))
        return self._post(json=payload)

    def delete(self, config_id: UUID) -> None:
        '''
        Delete a scan configuration.

        :devportal:`configuration: delete <was-v2-config-delete>`

        Args:
            config_id (uuid.UUID):
                The unique identifier for the scan configuration.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.was.configurations.delete(
            ...     '00000000-0000-0000-0000-000000000000'
            ... )
        '''

        return self._delete(f'{config_id}')

    def details(self, config_id: UUID) -> Dict:
        '''
        Returns details for the specified scan configuration.

        :devportal:`configuration: details <was-v2-config-details>`

        Args:
            config_id (uuid.UUID):
                The UUID of the scan configuration that you want to
                retrieve details for.

        Returns:
            :obj:`dict`:
                The details of the specified scan configuration.

        Examples:
            >>> tio.v3.was.configurations.details(
            ...     '00000000-0000-0000-0000-000000000000'
            ... )
        '''

        return super()._details(config_id)

    def get_processing_status(self,
                              config_id: UUID,
                              tracking_id: UUID
                              ) -> Dict:
        '''
        Tracks the current status of a scan configuration
        creation, update, or upsert process.

        :devportal:`configuration: processing status <was-v2-config-status>`

        Args:
            config_id (uuid.UUID):
                The UUID of the scan configuration.
                NOTE: The config_id can be retrieved from the URI provided in
                the Location header of the 202 Accepted response from the POST
                /was/v2/configs or PUT /was/v2/configs/{config_id} request
                used to create or update the scan configuration.
            tracking_id (uuid.UUID):
                The tracking UUID for the request you want to retrieve
                the status for.
                NOTE: The tracking_id can be retrieved from the URI provided in
                the Location header of the 202 Accepted response from the POST
                /was/v2/configs or PUT /was/v2/configs/{config_id} request
                used to create or update the scan configuration.

        Returns:
            :obj:`dict`:
                The procesing status for the scan configuration.

        Examples:
            >>> tio.v3.was.configurations.get_processing_status(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     '00000000-0000-0000-0000-000000000000'
            ... )
        '''

        return self._get(f'{config_id}/status/{tracking_id}')

    def move(self, config_id: UUID, folder_name: str) -> None:
        '''
        Moves the scan configuration to the specified folder.

        :devportal:`configuration: move <was-v2-config-move>`

        Args:
            config_id (uuid.UUID):
                The UUID of the scan configuration you want to update.
            folder_name (str):
                The name of the folder to set for the scan configuration.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.was.configurations.move(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     'Destination Folder'
            ... )

        '''
        payload = self._schema.dump(self._schema.load(
            {
                'folder_name': folder_name
            }
        ))
        return self._patch(f'{config_id}', json=payload)

    def search(self,
               **kwargs
               ) -> Union[CSVChunkIterator,
                          SearchIterator,
                          Response]:
        '''
        Search and retrieve the configurations based on supported conditions.

        Args:
            fields (list, optional):
                The list of field names returned from the Tenable API.

                Examples:
                    >>> ['field1', 'field2']
            sort (list[tuple], optional):
                sort is a list of tuples in the form of
                ('FIELD', 'ORDER').
                It describes how to sort the data
                that is to be returned.

                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]
            filter (tuple, dict, optional):
                A nestable filter object detailing how to filter the results
                down to the desired subset.

                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                    ...                 ('test', 'oper', '2')
                    ...             ),
                    ...     'and', ('test', 'oper', 3)
                    ... )
                    >>> {
                    ...  'or': [{
                    ...      'and': [{
                    ...              'value': '1',
                    ...              'operator': 'oper',
                    ...              'property': '1'
                    ...          },
                    ...          {
                    ...              'value': '2',
                    ...              'operator': 'oper',
                    ...              'property': '2'
                    ...          }
                    ...      ]
                    ...  }],
                    ...  'and': [{
                    ...      'value': '3',
                    ...      'operator': 'oper',
                    ...      'property': 3
                    ...  }]
                    ... }

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth: `tio.v3.definitions.was.configurations()`
                endpoint to get more details.
            limit (int, optional):
                Number of objects to be returned in each request.
                Default and maximum limit is 200.
            offset (int, optional):
                The pagination offset to use when requesting the next page of
                results.
            num_pages (int, optional):
                The total number of pages to request before stopping the
                iterator.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.

        Returns:
            Iterable:
                The iterable that handles the pagination for the job.
            requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        Examples:

            >>> tio.v3.was.configurations.search(
            ...     filter=('name','eq','value'),
            ...     fields=['name', 'field_one', 'field_two'],
            ...     limit=2,
            ...     sort=[('name', 'asc')]
            ... )
        '''

        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator

        return super()._search_was(iterator_cls=iclass,
                                   api_path=f'{self._path}/search',
                                   resource='items',
                                   sort_type=SortType.default,
                                   **kwargs
                                   )

    def upsert(self,
               config_id: UUID,
               name: str,
               owner_id: UUID,
               template_id: str,
               targets: List[str],
               settings: Dict,
               **kw
               ) -> Dict:
        '''
        Updates an existing scan configuration or creates a new
        scan configuration.

        :devportal:`configuration: updsert <was-v2-config-upsert>`

        Args:
            config_id (uuid.UUID):
                If updating an existing scan configuration, the UUID of the
                scan configuration you want to update. If creating a new scan
                configuration, a new UUID generated with a tool like uuidgen.
            name (str):
                The name of the scan configuration.
            owner_id (uuid.UUID):
                The UUID of the owner of the scan configuration.
            template_id (str):
                The UUID of the Tenable-provided configuration template.
            targets (list[str]):
                A List of distinct absolute URLs that were targeted in
                the scan.
            settings (dict):
                The scan configuration settings.
            description (str):
                A description of the scan configuration.
            folder_id (str):
                The UUID of the folder to assign for the scan configuration.
            user_template_id (str):
                The UUID of the user-defined configuration template from which
                this configuration is derived.
            scanner_id (int):
                The ID of the scanner (if the type is set to managed_webapp),
                or scanner group (if the type is pool or local) that performs
                the scan.
            schedule (dict):
                The schedule when the scan configuration will be run.
            notifications (dict):
                Contact information used to send scan notifications upon scan
                completion.
            permissions (list):
                The permissions for the scan configuration.

        Returns:
            :obj:`dict`:
                The resource record of the updated scan configuration.

        Examples:
            >>> configuration_settings = {
            ...     'description': 'Update Scan Configuration Description'
            ... }
            >>> targets = [
            ...     'https://example.com',
            ...     'https://example1.com'
            ... ]
            >>> scan_configuration = tio.v3.was.configurations.upsert(
            ...     '00000000-0000-0000-0000-000000000000',
            ...     'Updated Configuration Name',
            ...     '00000000-0000-0000-0000-000000000000',
            ...     settings=configuration_settings,
            ...     targets=targets,
            ...     template_id='00000000-0000-0000-0000-000000000000'
            ... )
        '''

        payload = {
            'name': name,
            'owner_id': owner_id,
            'template_id': template_id,
            'targets': targets,
            'settings': settings
        }
        payload.update(kw)

        payload = self._schema.dump(self._schema.load(payload))

        return self._put(f'{config_id}', json=payload)
