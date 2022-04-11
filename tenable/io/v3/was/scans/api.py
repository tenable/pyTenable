'''
Scans
=====

The following methods allow for interaction into the Tenable.io
:devportal:`Web Application Scanning v3 scans <was-v2-scans>` API.

Methods available on ``tio.v3.was.scans``:

.. rst-class:: hide-signature
.. autoclass:: ScansAPI
    :members:
'''
from io import BytesIO
from typing import Dict, Optional, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.was_iterator import (CSVChunkIterator,
                                                       SearchIterator)
from tenable.io.v3.was.scans.schema import ScanReportSchema, ScanStatusSchema


class ScansAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Scans API
    '''
    _path = 'api/v3/was'
    _conv_json = True

    def delete(self, id: UUID) -> None:
        '''
        Delete a scan.

        :devportal:`was scans: delete scan <was-v2-scans-delete>`

        Args:
            id (uuid.UUID): The UUID of the scan for which you want to delete.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.was.scans.delete('91843ecb-ecb8-48a3-b623-d4682c2594')
        '''
        self._delete(f'scans/{id}')

    def details(self, id: UUID) -> Dict:
        '''
        Fetch a scan record.

        :devportal:`was scans: get scan details <was-v2-scans-details>`

        Args:
            id (uuid.UUID): The UUID of the scan for which you want to view details.

        Returns:
            :obj:`dict`:
                The record object of the scan.

        Examples:
            >>> tio.v3.was.scans.details('91843ecb-ecb8-48a3-b623-d4682c2594')
        '''
        return super()._details(f'scans/{id}')

    def download(self,
                 id: UUID,
                 content_type: Optional[str] = 'application/json',
                 fobj: Optional[BytesIO] = None
                 ) -> BytesIO:
        '''
        Download exported scan report.

        :devportal:`was scans: download exported scan
        <was-v2-scans-download-export>`

        Args:
            id (uuid.UUID): The UUID of the scan for which you want to view a
                report.
            content_type (str, optional):
                The format you want the report returned in. You can request
                reports in one of the following formats:
                application/json, application/pdf
                text/csv, text/html, text/xml
            fobj (FileObject):
                A file-like object to write the contents of the report to.  If
                none is provided a BytesIO object will be returned with the
                report.

        Returns:
            :obj:`requests.Response`:
                The Response object based for the requested attachment.

        Examples:
            >>> with open('report_001.json', 'wb') as report:
            ...     tio.v3.was.scans.download(
            ...         '00000000-0000-0000-0000-000000000000',
            ...         'application/json',
            ...         report
            ...     )
        '''
        if not fobj:
            fobj = BytesIO()

        headers = {
            'content_type': content_type
        }
        schema = ScanReportSchema()
        headers = schema.dump(schema.load(headers))
        headers['Content-Type'] = headers.pop('content_type')

        resp = self._get(f'scans/{id}/report', headers=headers, stream=True)

        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)

        fobj.seek(0)
        resp.close()

        return fobj

    def export(self, id: UUID, content_type: str = None) -> None:
        '''
        Export scan details.

        :devportal:`was scans: export scan results <was-v2-scans-export>`

        Args:
            id (uuid.UUID):
                The UUID of the scan for which you want to generate a report.
            content_type (str, optional):
                The format you want the report returned in.
                Defaults to application/json.
                You can request reports in one of the following formats:
                application/json, application/pdf,
                text/csv, text/html, text/xml

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.was.scans.export('91843ecb-ecb8-48a3-b623-d4682c2594')
        '''
        headers = {
            'content_type': content_type
        }
        schema = ScanReportSchema()
        headers = schema.dump(schema.load(headers))
        headers['Content-Type'] = headers.pop('content_type')
        self._put(f'scans/{id}/report', headers=headers)

    def launch(self, config_id: UUID) -> None:
        '''
        Launch a scan.

        :devportal:`was scans: launch scan <was-v2-scans-launch>`

        Args:
            config_id (uuid.UUID):
            The UUID of the scan configuration to use to launch a scan.

        Returns:
            :obj:`uuid.UUID`:
                UUID of the scan initiated.

        Examples:
            >>> folder = tio.v3.was.folders.create('New Folder Name')
        '''
        return self._post(f'configs/{config_id}/scans').get('id')

    def notes(self,
              scan_id: UUID,
              **kwargs
              ) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Returns a list of notes for the specified scan.

        :devportal:`was scans: scans notes list <was-v2-scans-notes-list>`

        Args:

            scan_id (uuid.UUID):
                The UUID of the config that was used for the scan.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.\

        :Returns:

            - Iterable:
                The iterable that handles the pagination for the job.

            - requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        Examples:
            >>> tio.v3.was.scans.notes(scan_id=scan_id)

        '''
        api_path = f'{self._path}/scans/{scan_id}/notes'
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search_was(resource='items',
                                   iterator_cls=iclass,
                                   api_path=api_path,
                                   sort_type=self._sort_type.name_based,
                                   **kwargs
                                   )

    def search(self, config_id: UUID,
               **kwargs) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Retrieves the Scans data

        :devportal:`was scans: scans search <was-v2-scans-search>`

        Args:

            config_id (uuid.UUID):
                The UUID of the config that was used for the scan.
            fields (list, optional):
                The list of field names to return from the Tenable API.

                Example:
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
                the :py:meth: `tio.v3.definitions.was.scans()`
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

        :Returns:

            - Iterable:
                The iterable that handles the pagination for the job.

            - requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        Examples:
            >>> tio.v3.was.scans.search(config_id=config_id,
            ...     filter=('name','eq','value'),
            ...     fields=['name', 'field_one', 'field_two'],
            ...     limit=2,
            ...     sort=[('name', 'asc')]
            ... )
        '''
        api_path = f'{self._path}/configs/{config_id}/scans/search'
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search_was(resource='items',
                                   iterator_cls=iclass,
                                   api_path=api_path,
                                   sort_type=self._sort_type.name_based,
                                   **kwargs
                                   )

    def search_vulnerabilities(self,
                               scan_id: UUID,
                               **kwargs
                               ) -> Union[
                                   SearchIterator,
                                   CSVChunkIterator,
                                   Response]:
        '''
        Retrieves the list of vulnerabilities for the specified scan.

        :devportal:`was scans:scan vulns <was-v2-scans-details-vulns-search>`

        Args:

            scan_id (uuid.UUID):
                The UUID of the scan for which you want to view
                vulnerabilities.
            fields (list, optional):
                The list of field names to return from the Tenable API.

                Example:
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
                the :py:meth: `tio.v3.definitions.was.scan_vulnerabilities()`
                endpoint
                to get more details.
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

        :Returns:

            - Iterable:
                The iterable that handles the pagination for the job.

            - requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        Examples:
            >>> tio.v3.was.scans.search_vulnerabilities(scan_id=scan_id,
            ...     filter=('name','eq','value'),
            ...     fields=['name', 'field_one', 'field_two'],
            ...     limit=2,
            ...     sort=[('name', 'asc')]
            ... )
        '''
        api_path = f'{self._path}/scans/{scan_id}/vulnerabilities/search'
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search_was(resource='items',
                                   iterator_cls=iclass,
                                   api_path=api_path,
                                   sort_type=self._sort_type.name_based,
                                   **kwargs
                                   )

    def update_status(self, id: UUID, requested_action: str) -> None:
        '''
        Update the requested_action attribute for a scan. The requested action
        must be valid for the scan's current status. This request creates an
        asynchronous update job.

        :devportal:`was scans: update scan status <was-v2-scans-status-update>`

        Args:
            id (uuid.UUID): The UUID of the scan for which you want to update
                status.
            requested_action (str): The action to apply to the scan.
                The only supported action is stop.

        Returns:
            :obj:`None`

        Examples:
            >>> tio.v3.was.scans.update_status(
            ...     '91843ecb-ecb8-48a3-b623-d4682c2594'
            ... )
        '''
        schema = ScanStatusSchema()
        payload = {
            'requested_action': requested_action
        }
        payload = schema.dump(schema.load(payload))
        self._patch(f'scans/{id}', json=payload)
