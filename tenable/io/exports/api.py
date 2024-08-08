'''
Exports
=======

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`exports <exports>` API endpoints.

Methods available on ``tio.exports``:

.. rst-class:: hide-signature
.. autoclass:: ExportsAPI
    :members:
'''
from uuid import UUID
from json.decoder import JSONDecodeError
from typing_extensions import Literal
from typing import Dict, Union, List, Optional
from marshmallow import Schema
from restfly.errors import RequestConflictError
from tenable.base.endpoint import APIEndpoint
from .schema import AssetExportSchema, VulnExportSchema, ComplianceExportSchema
from .iterator import ExportsIterator


class ExportsAPI(APIEndpoint):
    def _export(self,
                export_type: Literal['vulns', 'assets', 'compliance'],
                schema: Optional[Schema] = None,
                use_iterator: bool = True,
                when_done: bool = False,
                iterator: ExportsIterator = ExportsIterator,
                timeout: Optional[int] = None,
                export_uuid: Optional[UUID] = None,
                adopt_existing: bool = True,
                **kwargs
                ) -> Union[ExportsIterator, UUID]:
        '''
        Get the list of jobs for for the specified datatype.

        API Documentation for the job listings for
        :devportal:`assets <exports-assets-request-export>`,
        :devportal:`compliance <io-exports-compliance-create>`, and
        :devportal:`vulnerabilities <exports-vulns-request-export>` datatypes.
        '''
        schemas = {
            'vulns': VulnExportSchema,
            'assets': AssetExportSchema,
            'compliance': ComplianceExportSchema,
        }
        if not schema:
            schema = schemas[export_type]()
        payload = schema.dump(schema.load(kwargs))

        if not export_uuid:
            try:
                export_uuid = self._api.post(f'{export_type}/export',
                                             json=payload,
                                             box=True
                                             ).export_uuid
                self._log.debug(
                    f'{export_type} export job {export_uuid} initiated'
                )
            except RequestConflictError as conflict:
                if not adopt_existing:
                    raise conflict
                resp = conflict.response.json()
                export_uuid = resp['active_job_id']
                msg = resp['failure_reason']
                self._log.warning(
                    f'Adopted {export_type} export job {export_uuid}.  '
                    f'Original message from platform was "{msg}"'
                )
        if use_iterator:
            return iterator(self._api,
                            type=export_type,
                            uuid=export_uuid,
                            _wait_for_complete=when_done,
                            timeout=timeout
                            )
        return UUID(export_uuid)

    def cancel(self,
               export_type: Literal['vulns', 'assets', 'compliance'],
               export_uuid: UUID,
               ) -> str:
        '''
        Cancels the specified export job.

        API Documentation for cancel export jobs with
        :devportal:`assets <exports-assets-export-cancel>`,
        :devportal:`compliance <io-exports-compliance-cancel>`, and
        :devportal:`vulnerabilities <exports-vulns-export-cancel>` datatypes.

        Args:
            export_type:
                The type of export job that we are to cancel.
            export_uuid:
                The export job's unique identifier.

        Returns:
            str:
                The status of the job.

        Example:

            >>> tio.exports.cancel('vuln', '{UUID}')
            'CANCELLED'
        '''
        return self._api.post(f'{export_type}/export/{export_uuid}/cancel',
                              box=True
                              ).status

    def download_chunk(self,
                       export_type: Literal['vulns', 'assets', 'compliance'],
                       export_uuid: UUID,
                       chunk_id: int,
                       retries: int = 3
                       ) -> List:
        '''
        Downloads an export chunk from the specified job.

        API Documentation for downloading an export chunk for
        :devportal:`assets <exports-assets-download-chunk>`,
        :devportal:`compliance <io-exports-compliance-download>`, and
        :devportal:`vulnerabilities <exports-vulns-download-chunk>`.

        Args:
            export_type:
                The type of export job
            export_uuid:
                The export job's unique identifier.
            chunk_id:
                The identifier for the specific chunk to download.

        Returns:
            List:
                The list of objects that entail the chunk of data requested.

        Example:

            >>> chunk = tio.exports.download_chunk('vulns', '{UUID}', 1)
        '''
        # We will attempt to download a chunk of data and convert it into JSON.
        # If the conversion fails, then we will increment our own retry counter
        # and attempt to download the chunk again.  After 3 attempts, we will
        # assume that the chunk is dead and return an empty list.
        downloaded = False
        counter = 0
        resp = []
        while not downloaded and counter <= retries:
            try:
                resp = self._api.get(
                    f'{export_type}/export/{export_uuid}/chunks/{chunk_id}'
                ).json()
                downloaded = True
            except JSONDecodeError:
                self._log.warning((
                    f'{export_type} export {export_uuid} encountered an '
                    f'invalid chunk on chunk id {chunk_id}'
                ))
                counter += 1
        if len(resp) < 1:
            self._log.warning((
                f'{export_type} export {export_uuid} encoundered an empty '
                f'chunk on chunk id {chunk_id}'
            ))
        return resp

    def status(self,
               export_type: Literal['vulns', 'assets', 'compliance'],
               export_uuid: UUID,
               ) -> Dict:
        '''
        Gets the status of the export job.

        API Documentation for the status of an export job for the
        :devportal:`assets <exports-assets-export-status>`,
        :devportal:`compliance <io-exports-compliance-status>`, and
        :devportal:`vulnerabilities <exports-vulns-export-status>` datatypes.

        Args:
            export_type (str):
                The datatype of the export job.
            export_uuid (str):
                The UUID of the export job.

        Examples:

            >>> status = tio.exports.status('vulns', {UUID}')
        '''
        return self._api.get(f'{export_type}/export/{export_uuid}/status',
                             box=True,
                             )

    def jobs(self,
             export_type: Literal['vulns', 'assets'],
             ) -> Dict:
        '''
        Returns the list of jobs available for a given datatype.

        API Documentation for the job listing APIs for
        :devportal:`assets <exports-assets-export-status-recent>`, and
        :devportal:`vulnerabilities <exports-vulns-export-status-recent>`
        datatypes.

        Args:
            export_type (str):
                The datatype of export to get the jobs for.

        Examples:

            >>> jobs = tio.exports.jobs('vulns')
        '''
        return self._api.get(f'{export_type}/export/status', box=True).exports

    def initiate_export(self,
                        export_type: Literal['vulns', 'assets', 'compliance'],
                        **kwargs
                        ):
        """
        Initiate an export job of the specified export type, and return the
        export UUID.

        This method accepts the key-value arguments supported by the methods
        assets(), vulns(), and compliance() for the matching export_type. For
        example, when the export_type is "assets", this function will only
        support the kwargs supported by the assets() method; if export_type is
        "vulns", the method will accept only those supported by the vulns()
        method, and so forth.

        Args:
            export_type (str):
                The datatype of export to get the jobs for.

        Examples:

            Initiating an assets export with no extra params.

            >>> export_uuid = tio.exports.initiate_export("assets")

            Initiating a vulns export with the params supported by vulns()

            >>> export_uuid = tio.exports.initiate_export("vulns", timeout=10)
        """
        return self._export(export_type=export_type,
                            use_iterator=False,
                            **kwargs
                            )

    def assets(self, **kwargs) -> Union[ExportsIterator, UUID]:
        '''
        Initiate an asset export.

        :devportal:`API Documentation <exports-assets-request-export>`

        Args:
            last_scan_id (str, optional):
                Scan uuid of the scan to be exported.
            created_at (int, optional):
                Assets created after this timestamp will be returned.
            deleted_at (int, optional):
                Assets deleted after this timestamp will be returned.
            first_scan_time (int, optional):
                Assets with a first_scan time later that this timestamp
                will be returned.
            last_assessed (int, optional):
                Assets last scanned after this timestamp will be returned.
            last_authenticated_scan_time (int, optional):
                Assets last scanned with an authenticated scan after this
                timestamp will be returned.
            terminated_at (int, optional):
                Assets terminated after this timestamp will be returned.
            updated_at (int, optional):
                Assets updated after this timestamp will be returned.
            has_plugin_results (bool, optional):
                Should assets only be returned if they have plugin results?
            is_deleted (bool, optional):
                Should we return only assets that have been deleted?
            is_licensed (bool, optional):
                Should we return only assets that are licensed?
            is_terminated (bool, optional):
                Should we return assets that have been terminated?
            servicenow_sysid (bool, optional):
                Should we return assets that have a ServiceNOW sysid?
                if ``True`` only assets with an id will be returned.
                if ``False`` only assets without an id will be returned.
            include_open_ports (bool, optional):
                Should we include open ports of assets in the exported chunks?
            chunk_size (int, optional):
                How many asset objects should be returned per chunk of data?
                The default is ``1000``.
            network_id (str, optional):
                Only assets within the specified network UUID will be returned.
            sources (list[str], optional):
                Only assets with a source matching one of these source values
                will be returned.  Note that this value is case-sensitive.
            tags (list[tuple[str, str]], optional):
                A list of tag pairs to filter the results on.  The tag pairs
                should be presented as ``('CATEGORY', 'VALUE')``.
            uuid (str, optional):
                A predefined export UUID to use for generating an
                ExportIterator.  Using this parameter will ignore all of the
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

            Iterating over the results of an asset export:

            >>> for asset in tio.exports.assets():
            ...     print(asset)

            Getting hosts that have been updated within the last 24 hours

            >>> assets = tio.exports.assets(
            ...     updated_at=int(arrow.now().shift(days=-1).timestamp())
            ... )

            Getting assets that have the the ``Region:Chicago`` tag:

            >>> assets = tio.exports.assets(
            ...     tags=[('Region', 'Chicago')]
            ... )
        '''
        return self._export('assets', AssetExportSchema(), **kwargs)

    def compliance(self, **kwargs) -> Union[ExportsIterator, UUID]:
        '''
        Initiate a compliance export.

        :devportal:`API Documentation <io-exports-compliance-create>`

        Args:
            asset (list[str], optional):
                A list of assets to return compliance results for.
            first_seen (int, optional):
                Returns findings with a first seen time newer than the
                specified unix timestamp.
            last_seen (int, optional):
                Returns findings with a last seen time newer than the
                specified unix timestamp.
            ipv4_addresses (list[str], optional):
                Returns Compliance findings found for the provided list of ipv4 addresses.
            ipv6_addresses (list[str], optional):
                Returns Compliance findings found for the provided list of ipv6 addresses.
            plugin_name (list[str], optional):
                Returns Compliance findings for the specified list of plugin names.
            plugin_id (list[int], optional):
                Returns Compliance findings for the specified list of plugin IDs.
            audit_name (str, optional):
                Restricts compliance findings to those associated with the specified audit.
            audit_file_name (str, optional):
                Restricts compliance findings to those associated with the specified audit file name.
            compliance_results (list[str], optional):
                Restricts compliance findings to those associated with the specified list of compliance results,
                such as PASSED, FAILED, SKIPPED, ERROR, UNKNOWN etc.
            last_observed (int,optional):
                Restricts compliance findings to those that were last observed on or after the specified unix timestamp.
            indexed_at (int, optional):
                Restricts compliance findings to those that were updated or indexed into Tenable Vulnerability Management
                 on or after the specified unix timestamp.
            since (int, optional):
                Same as indexed_at. Restricts compliance findings to those that were updated or indexed into Tenable
                Vulnerability Management on or after the specified unix timestamp.
            state (list[str], optional):
                Restricts compliance findings to those associated with the provided list of states, such as open, reopened and fixed.
            tags (list[tuple[str, list[str]]], optional):
                A list of tag pairs to filter the results on.  The tag pairs
                should be presented as ``('CATEGORY', ['VALUE'])``.
            network_id (str, optional):
                Returns Compliance findings for the specified network ID.
            num_findings (int):
                The number of findings to return per chunk of data.  If left
                unspecified, the default is ``5000``.
            uuid (str, optional):
                A predefined export UUID to use for generating an
                ExportIterator.  Using this parameter will ignore all of the
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

            >>> for findings in tio.exports.compliance():
            ...     print(finding)
        '''
        return self._export('compliance', ComplianceExportSchema(), **kwargs)

    def vulns(self, **kwargs) -> Union[ExportsIterator, UUID]:
        '''
        Initiate a vulnerability export.

        :devportal:`API Documentation <exports-vulns-request-export>`

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
            plugin_family (list[str], optional):
                Only return findings from the specified plugin families.
            plugin_id (list[int], optional):
                Only return findings from the specified plugin ids.
            plugin_type (str, optional):
                Only return findings with the specified plugin type.
            scan_uuid (uuid, optional):
                Only return findings with the specified scan UUID.
            source (list[str], optional):
                Only return vulnerabilities for assets that have the specified scan source.
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
            network_id (str, optional):
                Only findings within the specified network UUID will be
                returned.
            cidr_range (str, optional):
                Restrict the export to only vulns assigned to assets within the
                CIDR range specified.
            tags (list[tuple[str, str]], optional):
                A list of tag pairs to filter the results on.  The tag pairs
                should be presented as ``('CATEGORY', 'VALUE')``.
            include_unlicensed (bool, optional):
                Should findings for assets that are not licensed be included in
                the results?
            num_assets (int, optional):
                As findings are grouped by asset, how many assets's findings
                should exist within each data chunk?  If left unspecified the
                default is ``500``.
            uuid (str, optional):
                A predefined export UUID to use for generating an
                ExportIterator.  Using this parameter will ignore all of the
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

            Iterating over the results of an vuln export:

            >>> for vuln in tio.exports.vulns():
            ...     print(vuln)

            Getting findings that have been observed within the last 24 hours

            >>> vulns = tio.exports.vulns(
            ...     since=int(arrow.now().shift(days=-1).timestamp())
            ... )

            Getting findings that have the the ``Region:Chicago`` tag:

            >>> vulns = tio.exports.vulns(
            ...     tags=[('Region', 'Chicago')]
            ... )
        '''
        return self._export('vulns', VulnExportSchema(), **kwargs)

    def list_compliance_export_jobs(self):
        """
        Returns a list of the last 1,000 compliance export requests along with their statuses
        and related metadata.

        Returns:
            :obj:`list`:
                List of job records.

        Examples:
            >>> for compliance_job in tio.exports.list_compliance_export_jobs():
            ...     pprint(compliance_job)
        """
        return self._api.get('compliance/export/status').json()["exports"]