"""
Export
======

Methods described in this section relate to the unified export API for TenableOne.
These methods can be accessed at ``TenableOne.inventory.export``.

.. rst-class:: hide-signature
.. autoclass:: ExportAPI
    :members:

"""

from typing import List, Optional, Union
from io import BytesIO

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.inventory.export.schema import (
    DatasetExportRequest,
    DatasetFileFormat,
    ExportRequestId,
    ExportRequestStatus,
    ExportType,
    ExportJobsResponse
)
from tenable.tenableone.inventory.schema import PropertyFilter, QueryMode, Query
from tenable.tenableone.inventory.schema import SortDirection


class ExportAPI(APIEndpoint):
    def _export(
        self,
        export_type: ExportType,
        filters: Optional[List[PropertyFilter]] = None,
        query: Optional[Query] = None,
        properties: Optional[List[str]] = None,
        use_readable_name: Optional[bool] = None,
        max_chunk_file_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[SortDirection] = None,
        file_format: Optional[DatasetFileFormat] = None,
        compress: Optional[bool] = None,
    ) -> ExportRequestId:
        """
        Internal method to export data from TenableOne inventory.

        Args:
            export_type (ExportType): The type of export to perform ('assets' or 'findings').
            filters (list[PropertyFilter], optional): A list of filters to apply.
            query (Query, optional): The query to apply.
            properties (list[str], optional): List of property names.
            use_readable_name (bool, optional): Use readable property names.
            max_chunk_file_size (int, optional): Maximum chunk file size in bytes.
            sort_by (str, optional): Field to sort by.
            sort_direction (SortDirection, optional): Sorting direction.
            file_format (DatasetFileFormat, optional): Output file format.
            compress (bool, optional): Whether to compress the export using GZIP compression. 
                Compressed files are smaller but require decompression before processing.

        Returns:
            ExportRequestId: The export request ID.
        """

        # Build query parameters
        params = {}
        if properties is not None:
            params['properties'] = ','.join(properties)
        if use_readable_name is not None:
            params['use_readable_name'] = use_readable_name
        if max_chunk_file_size is not None:
            params['max_chunk_file_size'] = max_chunk_file_size
        if sort_by is not None and sort_direction is not None:
            params['sort'] = f'{sort_by}:{sort_direction.value}'
        if file_format is not None:
            params['file_format'] = file_format.value
        if compress is not None:
            params['compress'] = compress
        # Build request body
        payload = None
        if filters is not None or query is not None:
            payload = DatasetExportRequest(
                filters=filters,
                query=query
            ).model_dump(mode='json', exclude_none=True)

        response = self._post(
            f'api/v1/t1/inventory/export/{export_type.value}', json=payload, params=params
        )
        return ExportRequestId(**response)

    def _list_jobs(
        self,
        export_type: ExportType,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> ExportJobsResponse:
        """
        Internal method to list export jobs for a given export type.

        Args:
            export_type (ExportType): The type of export ('assets' or 'findings').
            status (str, optional): Filter by export status.
            limit (int, optional): Maximum number of export jobs to return.

        Returns:
            ExportJobsResponse: The list of export jobs.
        """
        params = {}
        if status is not None:
            params['status'] = status
        if limit is not None:
            params['limit'] = limit

        response = self._get(f'api/v1/t1/inventory/export/{export_type.value}/status', params=params)
        return ExportJobsResponse(**response)

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
            >>> status = tenable_one.inventory.export.status("export-123")
            >>> print(f"Status: {status.status}")
            >>> print(f"Chunks available: {status.chunks_available}")

        """
        response = self._get(f'api/v1/t1/inventory/export/{export_id}/status')
        return ExportRequestStatus(**response)

    def assets_status(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> ExportJobsResponse:
        """
        List asset export jobs submitted in the last 3 days

        This endpoint only returns asset export jobs that were submitted within the last 3 days.
        Results are sorted by last refreshed time (newest first).

        Args:
            status (str, optional):
                Filter by export status (e.g., 'FINISHED', 'PROCESSING', 'ERROR').
                Multiple values can be provided as a comma-separated string (e.g., 'FINISHED,PROCESSING').
            limit (int, optional):
                Maximum number of export jobs to return from the last 3 days.
                Note: This endpoint only returns jobs submitted within the last 3 days,
                so the actual number of results may be less than the limit if fewer jobs
                exist within that time window. Defaults to 1000 if not specified.
                Minimum: 1, Maximum: 1000.

        Returns:
            ExportJobsResponse:
                Response containing list of asset export job information from the last 3 days.

        Examples:
            >>> response = tenable_one.inventory.export.assets_status()
            >>> for job in response.exports:
            ...     print(f"Export ID: {job.export_id}, Status: {job.status}")

            >>> # Filter by status
            >>> finished_jobs = tenable_one.inventory.export.assets_status(status='FINISHED')

            >>> # Limit results to 100 most recent jobs
            >>> recent_jobs = tenable_one.inventory.export.assets_status(limit=100)

        """
        return self._list_jobs(ExportType.ASSETS, status, limit)

    def findings_status(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> ExportJobsResponse:
        """
        List finding export jobs submitted in the last 3 days

        This endpoint only returns finding export jobs that were submitted within the last 3 days.
        Results are sorted by last refreshed time (newest first).

        Args:
            status (str, optional):
                Filter by export status (e.g., 'FINISHED', 'PROCESSING', 'ERROR').
                Multiple values can be provided as a comma-separated string (e.g., 'FINISHED,PROCESSING').
            limit (int, optional):
                Maximum number of export jobs to return from the last 3 days.
                Note: This endpoint only returns jobs submitted within the last 3 days,
                so the actual number of results may be less than the limit if fewer jobs
                exist within that time window. Defaults to 1000 if not specified.
                Minimum: 1, Maximum: 1000.

        Returns:
            ExportJobsResponse:
                Response containing list of finding export job information from the last 3 days.

        Examples:
            >>> response = tenable_one.inventory.export.findings_status()
            >>> for job in response.exports:
            ...     print(f"Export ID: {job.export_id}, Status: {job.status}")

            >>> # Filter by status
            >>> finished_jobs = tenable_one.inventory.export.findings_status(status='FINISHED')

            >>> # Limit results to 100 most recent jobs
            >>> recent_jobs = tenable_one.inventory.export.findings_status(limit=100)

        """
        return self._list_jobs(ExportType.FINDINGS, status, limit)

    def download(
        self, 
        export_id: str, 
        chunk_id: str, 
        fobj: Optional[BytesIO] = None
    ) -> Union[bytes, BytesIO]:
        """
        Download export chunk

        Args:
            export_id (str):
                The export ID.
            chunk_id (str):
                The chunk ID to download.
            fobj (BytesIO, optional):
                A file-like object to write the downloaded data to. If not provided,
                the data will be returned as bytes. If provided, the data will be
                streamed directly to the file object and the file object will be returned.

        Returns:
            Union[bytes, BytesIO]:
                The exported data as bytes if fobj is not provided, or the file object
                if fobj is provided.

        Examples:
            Download to bytes:
            >>> data = tenable_one.inventory.export.download("export-123", "0")
            >>> with open("export.csv", "wb") as f:
            ...     f.write(data)

            Stream to file object:
            >>> with open("export.csv", "wb") as f:
            ...     fobj = BytesIO()
            ...     tenable_one.inventory.export.download("export-123", "0", fobj)
            ...     f.write(fobj.getvalue())

        """
        response = self._get(
            f'api/v1/t1/inventory/export/{export_id}/download/{chunk_id}', 
            stream=True
        )
        
        if fobj is not None:
            # Stream the data directly to the file object
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    fobj.write(chunk)
            fobj.seek(0)
            response.close()
            return fobj
        else:
            # Return the content as bytes (loads entire response into memory)
            return response.content

    def assets(
        self,
        filters: Optional[List[PropertyFilter]] = None,
        query: Optional[Query] = None,
        properties: Optional[List[str]] = None,
        use_readable_name: Optional[bool] = None,
        max_chunk_file_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[SortDirection] = None,
        file_format: Optional[DatasetFileFormat] = None,
        compress: Optional[bool] = None,
    ) -> ExportRequestId:
        """
        Export assets from TenableOne inventory

        Args:
            filters (list[PropertyFilter], optional):
                A list of filters to apply to the export. Defaults to None.
            query (Query, optional): The query to apply.
            properties (list[str], optional):
                Properties to include about the assets returned in the search results.
                List of property names. Defaults to None.
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
            file_format (DatasetFileFormat, optional):
                The file format to be received. If not specified, the default format will be JSON.
                Supported formats include: CSV and JSON. Defaults to DatasetFileFormat.JSON.
            compress (bool, optional): Whether to compress the export using GZIP compression. 
                Compressed files are smaller but require decompression before processing.

        Returns:
            ExportRequestId:
                The export request ID.

        Examples:
            >>> export_id = tenable_one.inventory.export.assets(
            ...     properties=["cpe", "version", "file_location"],
            ...     sort_by="name",
            ...     sort_direction=SortDirection.ASC,
            ...     file_format=DatasetFileFormat.CSV
            ... )
            >>> print(export_id.export_id)

        """
        return self._export(
            export_type=ExportType.ASSETS,
            filters=filters,
            query=query,
            properties=properties,
            use_readable_name=use_readable_name,
            max_chunk_file_size=max_chunk_file_size,
            sort_by=sort_by,
            sort_direction=sort_direction,
            file_format=file_format,
            compress=compress,
        )

    def findings(
        self,
        filters: Optional[List[PropertyFilter]] = None,
        query: Optional[Query] = None,
        properties: Optional[List[str]] = None,
        use_readable_name: Optional[bool] = None,
        max_chunk_file_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[SortDirection] = None,
        file_format: Optional[DatasetFileFormat] = None,
        compress: Optional[bool] = None,
    ) -> ExportRequestId:
        """
        Export findings from TenableOne inventory

        Args:
            filters (list[PropertyFilter], optional):
                A list of filters to apply to the export. Defaults to None.
            query (Query, optional): The query to apply.
            properties (list[str], optional):
                Properties to include about the findings returned in the search results.
                List of property names. Defaults to None.
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
            file_format (DatasetFileFormat, optional):
                The file format to be received. If not specified, the default format will be JSON.
                Supported formats include: CSV and JSON. Defaults to DatasetFileFormat.JSON.
            compress (bool, optional): Whether to compress the export using GZIP compression. 
                Compressed files are smaller but require decompression before processing.
        Returns:
            ExportRequestId:
                The export request ID.

        Examples:
            >>> export_id = tenable_one.inventory.export.findings(
            ...     properties=["severity", "status", "created_at"],
            ...     sort_by="severity",
            ...     sort_direction=SortDirection.DESC,
            ...     file_format=DatasetFileFormat.CSV
            ... )
            >>> print(export_id.export_id)

        """
        return self._export(
            export_type=ExportType.FINDINGS,
            filters=filters,
            query=query,
            properties=properties,
            use_readable_name=use_readable_name,
            max_chunk_file_size=max_chunk_file_size,
            sort_by=sort_by,
            sort_direction=sort_direction,
            file_format=file_format,
            compress=compress,
        )