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
from typing import Dict, Optional
from uuid import UUID

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.was.scans.schema import ScanReportSchema, ScanStatusSchema


class ScansAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Networks API
    '''
    _path = 'api/v3/was'
    _conv_json = True

    def delete(self, id: UUID) -> None:
        '''
        Delete a scan.

        :devportal:`was scans: delete scan <was-v2-scans-delete>`

        Args:
            id (UUID): The UUID of the scan for which you want to delete.

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
            id (UUID): The UUID of the scan for which you want to view details.

        Returns:
            obj:`dict`: The record object of the scan.

        Examples:
            >>> tio.v3.was.scans.details('91843ecb-ecb8-48a3-b623-d4682c2594')
        '''
        return super().details(f'scans/{id}')

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
            id (UUID): The UUID of the scan for which you want to view a
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
            :obj:`Response`
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
            id (UUID):
                The UUID of the scan for which you want to generate a report.
            content_type (str, optional):
                The format you want the report returned in.
                Defaults to application/json.
                You can request reports in one of the following formats:
                application/json, application/pdf,
                text/csv, text/html, text/xml

        Returns:
            obj:`None`

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
            config_id (UUID):
            The UUID of the scan configuration to use to launch a scan.

        Returns:
            obj:`UUID`: UUID of the scan initiated.

        Examples:
            >>> folder = tio.v3.was.folders.create('New Folder Name')
        '''
        return self._post(f'configs/{config_id}/scans').get('id')

    # TODO: Requires search iterator
    def notes(self,
              id: UUID,
              limit: int = 10,
              offset: int = 0,
              sort: str = None
              ) -> None:
        '''
        Not Implemented
        '''
        raise NotImplementedError(
            'This method will be updated once ExploreSearchIterator is \
                implemented for v3'
        )

    # TODO: Requires search iterator
    def search(self, config_id: UUID, **kwargs) -> None:
        '''
        Not Implemented
        '''
        raise NotImplementedError(
            'This method will be updated once ExploreSearchIterator is \
                implemented for v3'
        )

    # TODO: Requires search iterator
    def search_vulnerabilities(self, id: UUID, **kwargs) -> None:
        '''
        Not Implemented
        '''
        raise NotImplementedError(
            'This method will be updated once ExploreSearchIterator is \
                implemented for v3'
        )

    def update_status(self, id: UUID, requested_action: str) -> None:
        '''
        Update the requested_action attribute for a scan. The requested action
        must be valid for the scan's current status. This request creates an
        asynchronous update job.

        :devportal:`was scans: update scan status <was-v2-scans-status-update>`

        Args:
            id (UUID): The UUID of the scan for which you want to update
                status.
            requested_action (str): The action to apply to the scan.
                The only supported action is stop.

        Returns:
            obj:`None`

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
