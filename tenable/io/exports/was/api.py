"""
WAS-Exports
=======

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`was exports <exports>` API endpoints.

Methods available on ``tio.exports``:

.. rst-class:: hide-signature
.. autoclass:: ExportsAPI
    :members:
"""
from json import JSONDecodeError
from uuid import UUID
from typing import Dict, Union, List, Optional
from marshmallow import Schema
from restfly.errors import RequestConflictError
from tenable.base.endpoint import APIEndpoint
from .schema import WASVulnExportSchema
from .iterator import WASExportsIterator


class WASVulnsExportsAPI(APIEndpoint):
    def _export(
        self,
        schema: Optional[Schema] = None,
        use_iterator: bool = True,
        when_done: bool = False,
        iterator: WASExportsIterator = WASExportsIterator,
        timeout: Optional[int] = None,
        export_uuid: Optional[UUID] = None,
        adopt_existing: bool = True,
        **kwargs
    ):
        version = kwargs.pop('version', '')
        schemas = {
            'v1': WASVulnExportSchema
        }

        if not schema:
            schema = schemas[version]()

        payload = schema.dump(schema.load(kwargs))

        if not export_uuid:
            try:
                export_uuid = self._api.post(f'was/{version}/export/vulns', json=payload, box=True).export_uuid
                self._log.debug(
                    f'WAS {version} vulns export job {export_uuid} initiated'
                )
            except RequestConflictError as conflict:
                if not adopt_existing:
                    raise conflict
                resp = conflict.response.json()
                export_uuid = resp['active_job_id']
                msg = resp['failure_reason']
                self._log.warning(
                    f'Adopted WAS vulns {version} export job {export_uuid}.  '
                    f'Original message from platform was "{msg}"'
                )

        if use_iterator:
            return iterator(self._api, type='was-vulns', uuid=export_uuid, _wait_for_complete=when_done,  timeout=timeout)

        return UUID(export_uuid)

    def export(self, **kwargs) -> Union[WASExportsIterator, UUID]:
        """
        Initiate a WAS vulnerability export.

        :devportal:`API Documentation <exports-was-vulns-request-export>`

        Args:
            first_found (int, optional):
                Findings first discovered after this timestamp will be
                returned.
            indexed_at (int, optional):
                Findings indexed into Tenable Vulnerability Management after this timestamp will
                be returned.
            last_fixed (int, optional):
                Findings fixed after this timestamp will be returned.  Note
                that this filter only applies to fixed data and should not be
                used when searching for active findings.
            last_found (int, optional):
                Findings last observed after this timestamp will be returned.
            since (int, optional):
                Findings last observed in any state after this timestamp will
                be returned.  Cannot be used with ``last_found``,
                ``first_found``, or ``last_fixed``.
            plugin_ids (list[int], optional):
                Only return findings from the specified plugin ids.
            asset_uuid (list[str], optional):
                Only return findings for the assets with specific asset-uuids.
            asset_name (str, optional):
                Only return findings for the asset with given name.
            owasp_2010 (list[str], optional):
                A list of chapters from the OWASP Categories 2010 report for which you want to filter findings returned in the findings export.
            owasp_2013 (list[str], optional):
                A list of chapters from the OWASP Categories 2013 report for which you want to filter findings returned in the findings export.
            owasp_2017 (list[str], optional):
                A list of chapters from the OWASP Categories 2017 report for which you want to filter findings returned in the findings export.
            owasp_2021 (list[str], optional):
                A list of chapters from the OWASP Categories 2021 report for which you want to filter findings returned in the findings export.
            owasp_api_2019 (list[str], optional):
                A list of chapters from the OWASP Categories API 2019 report for which you want to filter findings returned in the findings export.
            severity_modification_type (list[str], optional):
                Only return vulnerabilities with the specified severity modification type.
            severity (list[str], optional):
                Only return findings with the specified severities.
            state (list[str], optional):
                Only return findings with the specified states.
            vpr_score (dict, optional):
                Only returns findings that meet the specified VPR criteria.
                The filter is formatted as a dictionary with the mathematical
                operation as the key.  Supported operations are:

                .. list-table:: Supported Operations
                    :widths: auto
                    :header-rows: 1

                    * - Operation
                      - Type
                      - Description
                    * - ``eq``
                      - list[float]
                      - List of VPR scores that the findings must match.
                    * - ``neq``
                      - list[float]
                      - List of VPR scores that the findings can not match.
                    * - ``gt``
                      - float
                      - VPR scores must be greater than the specified value.
                    * - ``gte``
                      - float
                      - VPR scores must be greater than or equal to the
                        specified value.
                    * - ``lt``
                      - float
                      - VPR scores must be less than the specified value.
                    * - ``lte``
                      - float
                      - VPR scores must be less than or equal to the
                        specified value.
            ipv4s (list[str], optional):
                Restrict the export to only vulns assigned to assets with specific
                ip-addresses.
            include_unlicensed (bool, optional):
                Should findings for assets that are not licensed be included in
                the results?
            num_assets (int, optional):
                As findings are grouped by asset, how many assets' findings
                should exist within each data chunk?  If left unspecified the
                default is ``500``.
            uuid (str, optional):
                A predefined export UUID to use for generating an
                ExportIterator.  Using this parameter will ignore all the
                filter arguments.
            use_iterator (bool, optional):
                Determines if we should return an iterator, or simply the
                export job UUID.  The default is to return an iterator.
            when_done (bool, optional):
                When creating the iterator, setting this flag to true will tell
                the iterator to wait until the export job has completed before
                processing the first chunk.  The default behaviour is to start
                processing chunks of data as soon as they become available.
            timeout (int, optional):
                If specified, determines a timeout in seconds to wait for the
                export job to sit in the queue before cancelling the job and
                raising a ``TioExportsTimeout`` error.  Once a job has started
                to be processed, the timeout is ignored.
            iterator (Iterator, optional):
                Supports overloading the iterator class to be used to process
                the datachunks.
            adopt_existing (bool, optional):
                Should we automatically adopt an existing Job UUID with we
                receive a 409 conflict?  Defaults to True.

        Examples:

            Examples:

            Iterating over the results of a WAS vuln export:
            >>> from tenable.io import TenableIO
            >>> tio = TenableIO("<apiKey>", "secret")
            >>> for vuln in tio.was_exports.export():
            ...     print(vuln)

            Getting findings that have been observed within the last 24 hours
            >>> import arrow
            >>> vulns = tio.was_exports.export(
            ...     since=int(arrow.now().shift(days=-1).timestamp())
            ... )

            Getting findings that have the ``Region:Chicago`` tag:

            >>> vulns = tio.was_exports.export(
            ...     tags=[('Region', 'Chicago')]
            ... )
        """
        return self._export(WASVulnExportSchema(), version='v1', **kwargs)

    def status(self, export_uuid: str) -> Dict:
        """
        Gets the status of the export job.

        API Documentation for the status of an export job for the
        :devportal:`vulnerabilities <exports-was-vulns-export-status>` datatypes.

        Args:
            export_uuid (str):
                The UUID of the export job.

        Examples:
            >>> from tenable.io import TenableIO
            >>> tio = TenableIO("<apiKey>", "secret")
            >>> status = tio.was_exports.status('{UUID}')
        """
        return self._api.get(f'was/v1/export/vulns/{export_uuid}/status', box = True)

    def cancel(self, export_uuid: str) -> str:
        """
        Cancels the specified export job.

        API Documentation for cancel export jobs with
        :devportal:`vulnerabilities <exports-was-vulns-export-cancel>` datatypes.

        Args:
            export_uuid:
                The export job's unique identifier.

        Returns:
            str:
                The status of the job.

        Example:
            >>> from tenable.io import TenableIO
            >>> tio = TenableIO("<apiKey>", "secret")
            >>> tio.was_exports.cancel('{UUID}')
            'CANCELLED'
        """
        return self._api.post(f'was/v1/export/vulns/{export_uuid}/cancel', box=True).status

    def download_chunk(self, export_uuid: str, chunk_id: int, retries: int = 3) -> List:
        """
        Downloads an export chunk from the specified job.

        API Documentation for downloading an export chunk for
        :devportal:`vulnerabilities <exports-was-vulns-download-chunk>`.

        Args:
            export_uuid:
                The export job's unique identifier.
            chunk_id:
                The identifier for the specific chunk to download.
            retries:
                Number of max times, chunk download should be retried in case of failures.

        Returns:
            List:
                The list of objects that entail the chunk of data requested.

        Example:
            >>> from tenable.io import TenableIO
            >>> tio = TenableIO("<apiKey>", "secret")
            >>> chunk = tio.was_exports.download_chunk('{UUID}', 1)
        """
        downloaded = False
        counter = 0
        resp = []
        while not downloaded and counter <= retries:
            try:
                resp = self._api.get(f'was/v1/export/vulns/{export_uuid}/chunks/{chunk_id}').json()
                downloaded = True
            except JSONDecodeError:
                self._log.warning((
                    f'was-vulns export {export_uuid} encountered an '
                    f'invalid chunk on chunk id {chunk_id}'
                ))
                counter += 1

        if len(resp) < 1:
            self._log.warning((
                f'was-vulns export {export_uuid} encountered an empty '
                f'chunk on chunk id {chunk_id}'
            ))
        return resp

    def jobs(self) -> Dict:
        """
        Returns the list of WAS vulns export jobs available..

        API Documentation for the job listing APIs for WAS vulns exports.
        :devportal:`WAS vulnerabilities <exports-was-vulns-export-status-recent>`
        datatypes.

        Examples:
            >>> jobs = tio.was_exports.jobs()
        """
        return self._api.get(f'was/v1/export/vulns/status', box=True).exports
