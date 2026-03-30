"""
Export
======

Methods described in this section relate to the attack path export API for TenableOne.
These methods can be accessed at ``TenableOne.attack_path.export``.

.. rst-class:: hide-signature
.. autoclass:: ExportAPI
    :members:

"""

from typing import List, Optional, Union
from io import BytesIO

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.attack_path.export.schema import (
    AttackPathColumnKey,
    AttackPathExportRequest,
    AttackTechniqueColumnKey,
    AttackTechniqueExportRequest,
    ExportFilter,
    ExportFilterCondition,
    ExportRequestId,
    ExportRequestStatus,
    ExportSortParams,
    FileFormat,
)


class ExportAPI(APIEndpoint):
    def attack_paths(
        self,
        file_format: FileFormat,
        sort: Optional[ExportSortParams] = None,
        filters: Optional[Union[ExportFilter, ExportFilterCondition]] = None,
        vector_ids: Optional[List[str]] = None,
        columns: Optional[List[AttackPathColumnKey]] = None,
        file_name: Optional[str] = None,
    ) -> ExportRequestId:
        """
        Export top attack paths

        Args:
            file_format (FileFormat):
                The output file format (CSV or JSON).
            sort (ExportSortParams, optional):
                Sort parameters for the export.
            filters (ExportFilter | ExportFilterCondition, optional):
                Filters to apply to the export. Can be a single filter
                condition or a compound filter with multiple conditions.
            vector_ids (list[str], optional):
                List of vector IDs to filter by.
            columns (list[AttackPathColumnKey], optional):
                Columns to include in the export.
            file_name (str, optional):
                The name of the export file.

        Returns:
            ExportRequestId:
                The export request ID.

        Examples:
            >>> export = tenable_one.attack_path.export.attack_paths(
            ...     file_format=FileFormat.CSV,
            ...     columns=[AttackPathColumnKey.PATH_NAME, AttackPathColumnKey.PRIORITY],
            ... )
            >>> print(export.export_id)

        """
        payload = AttackPathExportRequest(
            file_format=file_format,
            sort=sort,
            filters=filters,
            vector_ids=vector_ids,
            columns=columns,
            file_name=file_name,
        ).model_dump(mode='json', exclude_none=True)

        response = self._post(
            'api/v1/export/attack-path', json=payload
        )
        return ExportRequestId(**response)

    def attack_techniques(
        self,
        file_format: FileFormat,
        filters: Optional[Union[ExportFilter, ExportFilterCondition]] = None,
        sort: Optional[ExportSortParams] = None,
        columns: Optional[List[AttackTechniqueColumnKey]] = None,
        file_name: Optional[str] = None,
        attack_technique_ids: Optional[List[str]] = None,
    ) -> ExportRequestId:
        """
        Export attack techniques

        Args:
            file_format (FileFormat):
                The output file format (CSV or JSON).
            filters (ExportFilter | ExportFilterCondition, optional):
                Filters to apply to the export. Can be a single filter
                condition or a compound filter with multiple conditions.
            sort (ExportSortParams, optional):
                Sort parameters for the export.
            columns (list[AttackTechniqueColumnKey], optional):
                Columns to include in the export.
            file_name (str, optional):
                The name of the export file.
            attack_technique_ids (list[str], optional):
                List of attack technique IDs to filter by.

        Returns:
            ExportRequestId:
                The export request ID.

        Examples:
            >>> export = tenable_one.attack_path.export.attack_techniques(
            ...     file_format=FileFormat.JSON,
            ...     columns=[
            ...         AttackTechniqueColumnKey.MITRE_ID,
            ...         AttackTechniqueColumnKey.TECHNIQUE_NAME,
            ...     ],
            ... )
            >>> print(export.export_id)

        """
        payload = AttackTechniqueExportRequest(
            file_format=file_format,
            filters=filters,
            sort=sort,
            columns=columns,
            file_name=file_name,
            attack_technique_ids=attack_technique_ids,
        ).model_dump(mode='json', exclude_none=True)

        response = self._post(
            'api/v1/export/attack-technique', json=payload
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
            >>> status = tenable_one.attack_path.export.status("export-123")
            >>> print(f"Status: {status.status}")

        """
        response = self._get(
            f'api/v1/export/{export_id}/status'
        )
        return ExportRequestStatus(**response)

    def download(
        self,
        export_id: str,
        fobj: Optional[BytesIO] = None,
    ) -> Union[bytes, BytesIO]:
        """
        Download export results

        Args:
            export_id (str):
                The export ID to download.
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

            >>> data = tenable_one.attack_path.export.download("export-123")
            >>> with open("export.csv", "wb") as f:
            ...     f.write(data)

            Stream to file object:

            >>> fobj = BytesIO()
            >>> tenable_one.attack_path.export.download("export-123", fobj)
            >>> with open("export.csv", "wb") as f:
            ...     f.write(fobj.getvalue())

        """
        response = self._get(
            f'api/v1/export/{export_id}/download',
            stream=True,
        )

        if fobj is not None:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    fobj.write(chunk)
            fobj.seek(0)
            response.close()
            return fobj
        else:
            return response.content
