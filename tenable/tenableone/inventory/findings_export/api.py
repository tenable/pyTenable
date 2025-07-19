"""
Findings Export
==============

Methods described in this section relate to the findings export API.
These methods can be accessed at ``TenableOne.findings_export``.

.. rst-class:: hide-signature
.. autoclass:: FindingsExportAPI
    :members:

"""

from typing import Optional, List

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.inventory.findings_export.schema import (
    ExportRequestId,
    ExportRequestStatus,
    PublicDatasetExportRequest,
    PropertyFilter,
)
from tenable.tenableone.inventory.schema import SortDirection


class FindingsExportAPI(APIEndpoint):
    def export(
        self,
        filters: Optional[List[PropertyFilter]] = None,
        properties: Optional[str] = None,
        use_readable_name: Optional[bool] = None,
        max_chunk_file_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[SortDirection] = None,
    ) -> ExportRequestId:
        """
        Export findings

        Args:
            filters (list[PropertyFilter], optional):
                A list of filters to apply to the export. Defaults to None.
            properties (str, optional):
                Properties to include about the findings returned in the search results.
                Comma-separated list of property names. Defaults to None.
            use_readable_name (bool, optional):
                If true, the readable name of the property will be used instead of the internal (key) name.
                Defaults to True.
            max_chunk_file_size (int, optional):
                Maximum size in bytes for each chunk file when exporting large datasets.
                Defaults to 20971520 (20 MB).
            sort_by (str, optional):
                Field to sort by.
            sort_direction (SortDirection, optional):
                Sorting direction, either SortDirection.ASC or SortDirection.DESC.

        Returns:
            ExportRequestId:
                The export request ID.

        Examples:
            >>> export_id = tenable_one.inventory.findings_export.export(
            ...     properties="severity,status,created_at",
            ...     sort_by="severity",
            ...     sort_direction=SortDirection.DESC
            ... )
            >>> print(export_id.export_id)

        """
        # Build query parameters
        params = {}
        if properties is not None:
            params['properties'] = properties
        if use_readable_name is not None:
            params['use_readable_name'] = use_readable_name
        if max_chunk_file_size is not None:
            params['max_chunk_file_size'] = max_chunk_file_size
        if sort_by is not None and sort_direction is not None:
            params['sort'] = f"{sort_by}:{sort_direction.value}"

        # Build request body
        payload = None
        if filters is not None:
            payload = PublicDatasetExportRequest(
                filters=[filter.model_dump(mode='json') for filter in filters]
            ).model_dump(mode='json', exclude_none=True)

        response = self._post(
            'api/v1/t1/inventory/export/findings',
            json=payload,
            params=params
        )
        return ExportRequestId(**response)

    def status(self, export_id: str) -> ExportRequestStatus:
        """
        Get export status

        Args:
            export_id (str):
                The export ID to check status for.

        Returns:
            ExportRequestStatus:
                The export status information.

        Examples:
            >>> status = tenable_one.findings_export.status("export-123")
            >>> print(f"Status: {status.status}")
            >>> print(f"Chunks available: {status.chunks_available}")

        """
        response = self._get(f'api/v1/t1/inventory/export/{export_id}/status')
        return ExportRequestStatus(**response)

    def download(self, export_id: str, chunk_id: str) -> bytes:
        """
        Download export

        Args:
            export_id (str):
                The export ID.
            chunk_id (str):
                The chunk ID to download.

        Returns:
            bytes:
                The exported data as bytes.

        Examples:
            >>> data = tenable_one.findings_export.download("export-123", "0")
            >>> with open("findings_export.csv", "wb") as f:
            ...     f.write(data)

        """
        response = self._get(
            f'api/v1/t1/inventory/export/{export_id}/download/{chunk_id}',
            stream=True
        )
        return response.content 