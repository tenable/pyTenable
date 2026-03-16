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
    AttackPathExportParams,
    AttackPathExportRequest,
    AttackTechniqueColumnKey,
    AttackTechniqueExportRequest,
    ExportRequestId,
    ExportRequestStatus,
    ExportSortParams,
    FileFormat,
    MultipleFilters,
    SingleFilter,
    SortDirection,
)


class ExportAPI(APIEndpoint):
    def attack_paths(
        self,
        export_type: str,
        file_format: FileFormat,
        params: Optional[AttackPathExportParams] = None,
        columns: Optional[List[AttackPathColumnKey]] = None,
        file_name: Optional[str] = None,
    ) -> ExportRequestId:
        """
        Export top attack paths

        Args:
            export_type (str):
                The type of export to perform. Use ``VECTORS`` to export
                pre-computed top attack paths.
            file_format (FileFormat):
                The output file format (CSV or JSON).
            params (AttackPathExportParams):
                Export parameters including sort, filters, vector_ids,
                page_number, and max_entries_per_page.
            columns (list[AttackPathColumnKey], optional):
                Columns to include in the export.
            file_name (str, optional):
                The name of the export file.

        Returns:
            ExportRequestId:
                The export request ID.

        Examples:
            >>> export = tenable_one.attack_path.export.attack_paths(
            ...     export_type='VECTORS',
            ...     file_format=FileFormat.CSV,
            ...     params=AttackPathExportParams(),
            ...     columns=[AttackPathColumnKey.PATH_NAME, AttackPathColumnKey.PRIORITY],
            ... )
            >>> print(export.export_id)

        """
        payload = AttackPathExportRequest(
            export_type=export_type,
            file_format=file_format,
            params=params,
            columns=columns,
            file_name=file_name,
        ).model_dump(mode='json', exclude_none=True)

        response = self._post(
            'api/v1/t1/apa/export/attack-path', json=payload
        )
        return ExportRequestId(**response)

    def attack_techniques(
        self,
        file_format: FileFormat,
        filter: Optional[Union[SingleFilter, MultipleFilters]] = None,
        sort: Optional[List[ExportSortParams]] = None,
        columns: Optional[List[AttackTechniqueColumnKey]] = None,
        file_name: Optional[str] = None,
        page_number: Optional[int] = None,
        max_findings_per_page: Optional[int] = None,
        attack_technique_ids: Optional[List[str]] = None,
    ) -> ExportRequestId:
        """
        Export attack techniques

        Args:
            file_format (FileFormat):
                The output file format (CSV or JSON).
            filter (SingleFilter | MultipleFilters, optional):
                Filters to apply to the export. Can be a single filter
                condition or a compound filter with multiple conditions.
            sort (ExportSortParams, optional):
                Sort parameters for the export.
            columns (list[AttackTechniqueColumnKey], optional):
                Columns to include in the export.
            file_name (str, optional):
                The name of the export file.
            page_number (int, optional):
                The page number to export.
            max_findings_per_page (int, optional):
                Maximum number of findings per page.
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
            filter=filter,
            sort=sort,
            columns=columns,
            file_name=file_name,
            page_number=page_number,
            max_findings_per_page=max_findings_per_page,
            attack_technique_ids=attack_technique_ids,
        ).model_dump(mode='json', exclude_none=True)

        response = self._post(
            'api/v1/t1/apa/export/attack-technique', json=payload
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
            f'api/v1/t1/apa/export/{export_id}/status'
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
            f'api/v1/t1/apa/export/{export_id}/download',
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
