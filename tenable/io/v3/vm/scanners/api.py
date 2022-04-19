'''
Scanners
========

The following methods allow for interaction into the Tenable.io
:devportal:`scanners <scanners>` API.

Methods available on ``tio.v3.vm.scanners``:

.. rst-class:: hide-signature
.. autoclass:: ScannersAPI
    :members:
'''

from typing import Dict, List, Union
from uuid import UUID

from requests import Response
from typing_extensions import Literal

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.vm.scanners.schema import ScannerSchema


class ScannersAPI(ExploreBaseEndpoint):
    '''
    This class contains all the methods related to Scanners Endpoint.
    '''

    _path = 'api/v3/scanners'
    _conv_json = True
    _schema = ScannerSchema()

    def linking_key(self) -> str:
        '''
        The linking key for the Tenable.io instance.

        Returns:
            :obj:`str`:
                The linking key

        Examples:
            >>> tio.v3.vm.scanners.linking_key()
        '''
        id = '00000000-0000-0000-0000-00000000000000000000000000001'
        scanners = self.search(filter=('id', 'eq', id))
        for scanner in scanners:
            if scanner['id'] == id:
                return scanner['key']

    def allowed_scanners(self) -> List:
        '''
        A simple convenience function that returns the list
        of scanners that the current user is allowed to use.

        Returns:
            :obj:`list`:
                List of scanner documents.

        Examples:
            >>> for scanner in tio.v3.vm.scanners.allowed_scanners():
            ...     pprint(scanner)
        '''
        # We want to get the scanners that are available for scanning.
        # To do so, we will want to pull the information from the
        # scan template.  This isn't the prettiest way to handle this,
        # however it will consistently
        # return the results that we are looking for.
        # def get_scanners(tmpl):
        #     for item in tmpl['settings']['basic']['inputs']:
        #         if item['id'] == 'scanner_id':
        #             return item['options']
        #     return []

        # vm_tmpl = self._api.policies.templates().get('advanced', None)
        # was_tmpl = self._api.policies.templates().get('was_scan', None)
        # scanners = get_scanners(
        #    self._api.editor.template_details('scan', vm_tmpl)
        # )
        # if was_tmpl is not None:
        #     scanners.extend(
        #         get_scanners(
        #           self._api.editor.template_details('scan', was_tmpl)
        #         )
        #     )
        # return scanners

        raise NotImplementedError(
            'This method will be updated once Policies and Editor APIs\
                are implemented in v3'
        )

    def control_scan(
        self,
        scanner_id: UUID,
        scan_uuid: UUID,
        action: Literal['resume', 'pause', 'stop'],
    ) -> None:
        '''
        Perform actions against scans on a given scanner.

        :devportal:`scanners: control-scans <scanners-control-scans>`

        Args:
            scanner_id: (uuid):
                The unique identifier for the scanner.
            scan_uuid (uuid):
                The unique identifier for the scan.
            action (str):
                The action to take upon the scan. Valid actions are `stop`,
                `pause`, and `resume`.

        Returns:
            :obj:`None`

        Examples:
            Stop a scan running on the scanner:

            >>> tio.v3.vm.scanners.control_scan(
            ... 1, '00000000-0000-0000-0000-000000000000',
            ... 'stop'
            ... )
        '''
        payload = self._schema.dump(self._schema.load({'action': action}))
        self._post(
            f'{scanner_id}/scans/{scan_uuid}/control',
            json=payload
            )

    def delete(self, id: UUID) -> None:
        '''
        Delete a scanner from Tenable.io.

        :devportal:`scanners: delete <scanners-delete>`

        Args:
            id (uuid):
                The unique identifier for the scanner to delete.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.vm.scanners.delete(1)
        '''
        self._delete(f'{id}')

    def details(self, id: UUID) -> Dict:
        '''
        Retrieve the details for a specified scanner.

        :devportal:`scanners: details <scanners-details>`

        Args:
            id: (uuid):
                The unique identifier for the scanner

        Returns:
            :obj:`dict`:
                The scanner resource record.

        Examples:
            >>> scanner = tio.v3.vm.scanners.details(1)
            >>> pprint(scanner)
        '''
        return super()._details(f'{id}')

    def edit(self, id: UUID, **kwargs) -> None:
        '''
        Modify the scanner.

        :devportal:`scanners: edit <scanners-edit>`

        Args:
            id: (uuid):
                The unique identifier for the scanner.
            force_plugin_update (bool, optional):
                Force the scanner to perform a plugin update .
            force_ui_update (bool, optional):
                Force the scanner to perform a UI update.
            finish_update (bool, optional):
                Force the scanner to reboot to complete the update process.
                This action is only valid when automatic updates are disabled.
            registration_code (str, optional):
                Sets the registration code for the scanner.
            aws_update_interval (int, optional):
                For AWS scanners this will inform the scanner
                how often to check into Tenable.io.

        Returns:
            :obj:`None`

        Examples:
            Force a plugin update on a scanner:

            >>> tio.v3.vm.scanners.edit(1, force_plugin_update=True)
        '''
        payload = dict()
        payload = self._schema.dump(self._schema.load(kwargs))
        self._api.put(f'settings/{id}', json=payload)

    def get_aws_targets(self, id: UUID) -> List:
        '''
        Returns the list of AWS targets the scanner can reach.

        :devportal:`scanners: get-aws-targets <scanners-get-aws-targets>`

        Args:
            id: (uuid): The unique identifier for the scanner.

        Returns:
            :obj:`list`:
                List of aws target resource records.

        Examples:
            >>> for target in tio.v3.vm.scanners.get_aws_targets(1):
            ...      pprint(target)
        '''
        return self._get(f'{id}/aws-targets')['targets']

    def get_scanner_key(self, id: UUID) -> str:
        '''
        Return the key associated with the scanner.

        :devportal:`scanners: get-scanner-key <scanners-get-scanner-key>`

        Args:
            id: (uuid): The unique identifier for the scanner.

        Returns:
            :obj:`str`:
                The scanner key

        Examples:
            >>> print(tio.v3.vm.scanners.get_scanner_key(1))
        '''
        return str(self._get(f'{id}/key')['key'])

    def get_scans(self, id: UUID) -> List:
        '''
        Retrieves the scans associated to the scanner.

        :devportal:`scanners: get-scans <scanners-get-scans>`

        Args:
            id: (uuid): The unique identifier for the scanner.

        Returns:
            :obj:`list`:
                List of scan resource records associated to the scanner.

        Examples:
            >>> for scan in tio.v3.vm.scanners.get_scans(1):
            ...     pprint(scan)
        '''
        return self._get(f'{id}/scans')['scans']

    def search(self,
               **kwargs
               ) -> Union[CSVChunkIterator,
                          SearchIterator,
                          Response
                          ]:
        '''
        Search and retrieve the scanners based on supported conditions.

        :devportal:`scanners: search <scanners-search>`

        Args:
            
            fields (list, optional):
                The list of field names to return from the Tenable API.
            
                Example:
                    >>> ['field1', 'field2']
            
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
                the :py:meth:`tio.v3.definitions.vm.scanners()`
                endpoint to get more details.
            sort (list[tuple], optional):
                sort is a list of tuples in the form of
                ('FIELD', 'ORDER').
                It describes how to sort the data
                that is to be returned.

                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]

            limit (int, optional):
                Number of objects to be returned in each request.
                Default and max_limit is 200.
            next (str, optional):
                The pagination token to use when requesting the next page of
                results. This token is presented in the previous response.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.

        :Returns:

            - Iterable:
                The iterable that handles the pagination for the job.

            - requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        Examples:
            >>> tio.v3.vm.scanners.search( sort=[('received': 'desc)]
            ... fields=['id', 'name', 'users'], limit=2)
        '''
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(iterator_cls=iclass,
                               sort_type=self._sort_type.default,
                               api_path=f'{self._path}/search',
                               resource='scanners',
                               **kwargs
                               )

    def toggle_link_state(self, id: UUID, linked: bool) -> None:
        '''
        Toggles the scanner's activated state.

        :devportal:`scanners: toggle-link-state <scanners-toggle-link-state>`

        Args:
            id: (uuid): The unique identifier for the scanner
            linked (bool):
                The link status of the scanner.
                Setting to `False` will disable
                the link, whereas setting to `True` will enable the link.

        Returns:
            :obj:`None`

        Examples:
            to deactivate a linked scanner:

            >>> tio.v3.vm.scanners.toggle_link_state(1, False)
        '''
        payload = self._schema.dump(self._schema.load({'link': int(linked)}))
        self._put(
            f'{id}/link',
            json=payload,
        )

    def get_permissions(self, id: UUID) -> Dict:
        '''
        Returns the permission list for a given scanner.

        Args:
            id: (uuid): The unique identifier for the scanner.

        Returns:
            :obj:`dict`:
                The permissions resource for the scanner

        Examples:
            >>> tio.v3.vm.scanners.get_permissions(1)
        '''
        return self._api.v3.vm.permissions.list('scanner', id)

    def edit_permissions(self, id: UUID, *acls) -> None:
        '''
        Modifies the permissions list for the given scanner.

        Args:
            id: (uuid):The unique identifier for the scanner.
            *acls (dict): The permissions record(s) for the scanner.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.vm.scanners.edit_permissions(1,
            ...     {'type': 'default, 'permissions': 16},
            ...     {'type': 'user', 'id': 2, 'permissions': 16})
        '''
        self._api.v3.vm.permissions.change('scanner', id, *acls)
