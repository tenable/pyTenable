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
    ExportRequestStatus, ExportType
)
from tenable.tenableone.inventory.schema import PropertyFilter
from tenable.tenableone.inventory.schema import SortDirection


class ExportAPI(APIEndpoint):
    def _export(
        self,
        export_type: ExportType,
        filters: Optional[List[PropertyFilter]] = None,
        properties: Optional[List[str]] = None,
        use_readable_name: Optional[bool] = None,
        max_chunk_file_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[SortDirection] = None,
        file_format: Optional[DatasetFileFormat] = None,
    ) -> ExportRequestId:
        """
        Internal method to export data from TenableOne inventory.

        Args:
            export_type (ExportType): The type of export to perform ('assets' or 'findings').
            filters (list[PropertyFilter], optional): A list of filters to apply.
            properties (list[str], optional): List of property names.
            use_readable_name (bool, optional): Use readable property names.
            max_chunk_file_size (int, optional): Maximum chunk file size in bytes.
            sort_by (str, optional): Field to sort by.
            sort_direction (SortDirection, optional): Sorting direction.
            file_format (DatasetFileFormat, optional): Output file format.

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

        # Build request body
        payload = None
        if filters is not None:
            payload = DatasetExportRequest(
                filters=[filter.model_dump(mode='json') for filter in filters]
            ).model_dump(mode='json', exclude_none=True)

        response = self._post(
            f'api/v1/t1/inventory/export/{export_type.value}', json=payload, params=params
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
            >>> status = tenable_one.inventory.export.status("export-123")
            >>> print(f"Status: {status.status}")
            >>> print(f"Chunks available: {status.chunks_available}")

        """
        response = self._get(f'api/v1/t1/inventory/export/{export_id}/status')
        return ExportRequestStatus(**response)

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
        properties: Optional[List[str]] = None,
        use_readable_name: Optional[bool] = None,
        max_chunk_file_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[SortDirection] = None,
        file_format: Optional[DatasetFileFormat] = None,
    ) -> ExportRequestId:
        """
        Export assets from TenableOne inventory

        Args:
            filters (list[PropertyFilter], optional):
                A list of filters to apply to the export. Defaults to None.
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
            properties=properties,
            use_readable_name=use_readable_name,
            max_chunk_file_size=max_chunk_file_size,
            sort_by=sort_by,
            sort_direction=sort_direction,
            file_format=file_format,
        )

    def findings(
        self,
        filters: Optional[List[PropertyFilter]] = None,
        properties: Optional[List[str]] = None,
        use_readable_name: Optional[bool] = None,
        max_chunk_file_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[SortDirection] = None,
        file_format: Optional[DatasetFileFormat] = None,
    ) -> ExportRequestId:
        """
        Export findings from TenableOne inventory

        Args:
            filters (list[PropertyFilter], optional):
                A list of filters to apply to the export. Defaults to None.
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
            properties=properties,
            use_readable_name=use_readable_name,
            max_chunk_file_size=max_chunk_file_size,
            sort_by=sort_by,
            sort_direction=sort_direction,
            file_format=file_format,
        ) 