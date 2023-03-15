'''
Exports
=======

The following methods allow for interaction into the Tenable.io
:devportal:`exports <exports>` API endpoints.

Methods available on ``tio.exports``:

.. rst-class:: hide-signature
.. autoclass:: ExportsAPI
    :members:
'''
from uuid import UUID
from json.decoder import JSONDecodeError
from typing_extensions import Literal
from typing import Dict, Union, List
from marshmallow import Schema
from tenable.base.endpoint import APIEndpoint
from .schema import AssetExportSchema, VulnExportSchema, ComplianceExportSchema
from .iterator import ExportsIterator


class ExportsAPI(APIEndpoint):
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
                              ).get('status')

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
                        **kwargs):
        """
        Initiate an export job of the specified export type, and return the export UUID.

        This method accepts the key-value arguments supported by the methods assets(), vulns(), and compliance()
        for the matching export_type. For example, when the export_type is "assets", this function will only support the
        kwargs supported by the assets() method; if export_type is "vulns", the method will accept only those
        supported by the vulns() method, and so forth.

        Args:
            export_type (str):
                The datatype of export to get the jobs for.

        Examples:

            Initiating an assets export with no extra params.

            >>> export_uuid = tio.exports.initiate_export("assets")

            Initiating a vulns export with the params supported by vulns()

            >>> export_uuid = tio.exports.initiate_export("vulns", timeout=10)
        """

        # Setting the schema for the specified export type.
        if export_type == "vulns":
            schema = VulnExportSchema()
        elif export_type == "assets":
            schema = AssetExportSchema()
        elif export_type == "compliance":
            schema = ComplianceExportSchema()

        payload = schema.dump(schema.load(kwargs))

        # Initiating the export and returning the returned export UUID.
        return self._api.post(f'{export_type}/export', json=payload, box=True).export_uuid

    def _export(self,
                export_type: Literal['vulns', 'assets', 'compliance'],
                schema: Schema,
                **kwargs
                ) -> Union[ExportsIterator, UUID]:
        '''
        Get the list of jobs for for the specified datatype.

        API Documentation for the job listings for
        :devportal:`assets <exports-assets-request-export>`,
        :devportal:`compliance <io-exports-compliance-create>`, and
        :devportal:`vulnerabilities <exports-vulns-request-export>` datatypes.
        '''
        export_uuid = kwargs.pop('uuid', None)
        use_iterator = kwargs.pop('use_iterator', True)
        when_done = kwargs.pop('when_done', False)
        Iterator = kwargs.pop('iterator', ExportsIterator)  # noqa: PLC0103
        timeout = kwargs.pop('timeout', None)
        payload = schema.dump(schema.load(kwargs))

        if not export_uuid:
            export_uuid = self._api.post(f'{export_type}/export',
                                         json=payload,
                                         box=True
                                         ).export_uuid
            self._log.debug(
                f'{export_type} export job {export_uuid} initiated'
            )
        if use_iterator:
            return Iterator(self._api,
                            type=export_type,
                            uuid=export_uuid,
                            _wait_for_complete=when_done,
                            timeout=timeout
                            )
        return UUID(export_uuid)

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
                Findings indexed into Tenable.io after this timestamp will
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
