"""
Exports
=======

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`exports <exports>` API endpoints.

Methods available on ``tio.exports``:

.. rst-class:: hide-signature
.. autoclass:: ExportsAPI
    :members:
"""

import warnings
from datetime import datetime
from ipaddress import IPv4Address, IPv4Network, IPv6Address
from json.decoder import JSONDecodeError
from typing import Any, Literal, Type
from uuid import UUID

from restfly.errors import RequestConflictError

from tenable.base.endpoint import APIEndpoint

from . import models
from .iterator import ExportsIterator

EXPORTS_MAP = {
    'vulns': {
        None: {'path': 'vulns/export', 'job_path': 'vulns/export'},
    },
    'assets': {
        None: {'path': 'assets/export', 'job_path': 'assets/export'},
        'v2': {'path': 'assets/v2/export', 'job_path': 'assets/export'},
    },
    'compliance': {
        None: {'path': 'compliance/export', 'job_path': 'compliance/export'},
    },
    'was': {
        None: {'path': 'was/v1/export/vulns', 'job_path': 'was/v1/export/vulns'},
    },
}


class ExportsAPI(APIEndpoint):
    def _export(
        self,
        *,
        export_type: Literal['vulns', 'assets', 'compliance', 'was'],
        payload: dict[str, Any],
        version: str | None = None,
        when_done: bool = False,
        iterator: Type[ExportsIterator] | None = ExportsIterator,
        timeout: int | None = None,
        export_uuid: UUID | None = None,
        adopt_existing: bool = True,
    ) -> ExportsIterator | UUID:
        """
        Submit new export job for the specified datatype.

        API Documentation for the job listings for
        :devportal:`assets <exports-assets-request-export>`,
        :devportal:`compliance <io-exports-compliance-create>`, and
        :devportal:`vulnerabilities <exports-vulns-request-export>` datatypes.
        """
        exmap = EXPORTS_MAP[export_type][version]
        path = exmap['path']
        if not export_uuid:
            try:
                export_uuid = self._api.post(path, json=payload, box=True).export_uuid
                self._log.debug(
                    f'{export_type} {version} export job {export_uuid} initiated'
                )

            except RequestConflictError as conflict:
                if not adopt_existing:
                    raise conflict
                resp = conflict.response.json()
                export_uuid = resp['active_job_id']
                msg = resp['failure_reason']
                self._log.warning(
                    f'Adopted {export_type} {version} export job {export_uuid}.  '
                    f'Original message from platform was "{msg}"'
                )

        if iterator:
            return iterator(
                self._api,
                type=export_type,
                uuid=export_uuid,
                version=version,
                _wait_for_complete=when_done,
                timeout=timeout,
            )

        return UUID(str(export_uuid))

    def cancel(
        self,
        export_type: Literal['vulns', 'assets', 'compliance', 'was'],
        export_uuid: UUID,
        version: str | None = None,
    ) -> str:
        """
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
            version:
                The export type version.
        Returns:
            str:
                The status of the job.

        Example:

            >>> tio.exports.cancel('vuln', '{UUID}')
            'CANCELLED'
        """
        path = EXPORTS_MAP[export_type][version]['job_path']
        return self._api.post(f'{path}/{export_uuid}/cancel', box=True).status

    def download_chunk(
        self,
        export_type: Literal['vulns', 'assets', 'compliance', 'was'],
        export_uuid: UUID,
        chunk_id: int,
        version: str | None = None,
        retries: int = 3,
    ) -> list[dict[str, Any]]:
        """
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
            version:
                The export type version.

        Returns:
            The list of objects that entail the chunk of data requested.

        Example:

            >>> chunk = tio.exports.download_chunk('vulns', '{UUID}', 1)
        """
        # We will attempt to download a chunk of data and convert it into JSON.
        # If the conversion fails, then we will increment our own retry counter
        # and attempt to download the chunk again. After 3 attempts, we will
        # assume that the chunk is dead and return an empty list.
        downloaded = False
        counter = 0
        resp = []
        path = EXPORTS_MAP[export_type][version]['job_path']
        while not downloaded and counter <= retries:
            try:
                resp = self._api.get(f'{path}/{export_uuid}/chunks/{chunk_id}').json()
                downloaded = True
            except JSONDecodeError:
                self._log.warning(
                    (
                        f'{export_type} {version} export {export_uuid} encountered an '
                        f'invalid chunk on chunk id {chunk_id}'
                    )
                )
                counter += 1
        if len(resp) < 1:
            self._log.warning(
                (
                    f'{export_type} {version} export {export_uuid} encoundered an empty '
                    f'chunk on chunk id {chunk_id}'
                )
            )
        return resp

    def status(
        self,
        export_type: Literal['vulns', 'assets', 'compliance', 'was'],
        export_uuid: UUID,
        version: str | None = None,
    ) -> dict[str, Any]:
        """
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
            version:
                The export type version.

        Examples:

            >>> status = tio.exports.status('vulns', '{UUID}')
        """
        path = EXPORTS_MAP[export_type][version]['job_path']
        return self._api.get(
            f'{path}/{export_uuid}/status',
            box=True,
        )

    def jobs(
        self,
        export_type: Literal['vulns', 'assets', 'was'],
        version: str | None = None,
    ) -> dict[str, Any]:
        """
        Returns the list of jobs available for a given datatype.

        API Documentation for the job listing APIs for
        :devportal:`assets <exports-assets-export-status-recent>`, and
        :devportal:`vulnerabilities <exports-vulns-export-status-recent>`
        datatypes.

        Args:
            export_type (str):
                The datatype of export to get the jobs for.
            version:
                The export type version.

        Examples:

            >>> jobs = tio.exports.jobs('vulns')
        """
        path = EXPORTS_MAP[export_type][version]['job_path']
        return self._api.get(f'{path}/status', box=True).exports

    def initiate_export(
        self,
        export_type: Literal['vulns', 'assets', 'compliance', 'was'],
        *,
        version: str | None = None,
        when_done: bool = False,
        iterator: Type[ExportsIterator] | None = ExportsIterator,
        timeout: int | None = None,
        export_uuid: UUID | None = None,
        uuid: UUID | None = None,
        adopt_existing: bool = True,
        **payload,
    ) -> UUID:
        """
        Initiate an export job of the specified export type, and return the
        export UUID.

        This method accepts the key-value arguments supported by the methods
        assets(), vulns(), and compliance() for the matching export_type. For
        example, when the export_type is "assets", this function will only
        support the kwargs supported by the assets() method; if export_type is
        "vulns", the method will accept only those supported by the vulns()
        method, and so forth.

        .. deprecated:: 1.9.0
            This method duplicates functionality that has existed within the bespoke
            export methods since 1.4.x. Thereforce this method has been flagged for
            removal. Please switch to using the appropriate export method and pass
            ``iterator=None`` in order to return a UUID instead of ``ExportIterator``.

        Args:
            export_type:
                The datatype of export to get the jobs for.
            version:
                The export type version.

        Examples:

            Initiating an assets export with no extra params.

            >>> export_uuid = tio.exports.initiate_export("assets")

            Initiating a vulns export with the params supported by vulns()

            >>> export_uuid = tio.exports.initiate_export("vulns", timeout=10)
        """
        warnings.warn(
            (
                'This method is deprecated in favor of using the appropriate export '
                'method instead. If a UUID is expected to be returned, then simply '
                'set the `iterator` parameter to `None`.'
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return self._export(
            export_type=export_type,
            version=version,
            when_done=when_done,
            iterator=None,
            timeout=timeout,
            export_uuid=export_uuid if export_uuid else uuid,
            adopt_existing=adopt_existing,
            payload=payload,
        )

    def assets(
        self,
        *,
        chunk_size: int = 1000,
        include_open_ports: bool | None = None,
        include_resource_tags: bool | None = None,
        created_at: datetime | int | None = None,
        updated_at: datetime | int | None = None,
        deleted_at: datetime | int | None = None,
        terminated_at: datetime | int | None = None,
        first_scan_time: datetime | int | None = None,
        last_authenticated_scan_time: datetime | int | None = None,
        last_assessed: datetime | int | None = None,
        is_deleted: bool | None = None,
        is_licensed: bool | None = None,
        is_terminated: bool | None = None,
        has_plugin_results: bool | None = None,
        last_scan_id: str | None = None,
        network_id: UUID | str | None = None,
        sources: list[str] | None = None,
        tags: list[tuple[str, list[str] | str]] | None = None,
        servicenow_sysid: bool | None = None,
        uuid: UUID | str | None = None,
        timeout: int | None = None,
        when_done: bool = False,
        adopt_existing: bool = True,
        iterator: Type[ExportsIterator] | None = ExportsIterator,
    ) -> ExportsIterator | UUID:
        """
        Initiate an asset export.

        :devportal:`API Documentation <exports-assets-request-export>`

        Args:
            last_scan_id:
                Scan uuid of the scan to be exported.
            created_at:
                Assets created after this timestamp will be returned.
            deleted_at:
                Assets deleted after this timestamp will be returned.
            first_scan_time:
                Assets with a first_scan time later that this timestamp
                will be returned.
            last_assessed:
                Assets last scanned after this timestamp will be returned.
            last_authenticated_scan_time:
                Assets last scanned with an authenticated scan after this
                timestamp will be returned.
            terminated_at:
                Assets terminated after this timestamp will be returned.
            updated_at:
                Assets updated after this timestamp will be returned.
            has_plugin_results:
                Should assets only be returned if they have plugin results?
            is_deleted:
                Should we return only assets that have been deleted?
            is_licensed:
                Should we return only assets that are licensed?
            is_terminated:
                Should we return assets that have been terminated?
            servicenow_sysid:
                Should we return assets that have a ServiceNOW sysid?
                if ``True`` only assets with an id will be returned.
                if ``False`` only assets without an id will be returned.
            include_open_ports:
                Should we include open ports of assets in the exported chunks?
            chunk_size:
                How many asset objects should be returned per chunk of data?
            network_id:
                Only assets within the specified network UUID will be returned.
            sources:
                Only assets with a source matching one of these source values
                will be returned.  Note that this value is case-sensitive.
            tags (list[tuple[str, str]], optional):
                A list of tag pairs to filter the results on.  The tag pairs
                should be presented as ``('CATEGORY', 'VALUE')``.
            uuid:
                A predefined export UUID to use for generating an
                ExportIterator.  Using this parameter will ignore all of the
                filter arguments.
            when_done:
                When creating the iterator, setting this flag to true will tell
                the iterator to wait until the export job has completed before
                processing the first chunk.  The default behaviour is to start
                processing chunks of data as soon as they become available.
            timeout:
                If specified, determines a timeout in seconds to wait for the
                export job to sit in the queue before cancelling the job and
                raising a ``TioExportsTimeout`` error.  Once a job has started
                to be processed, the timeout is ignored.
            iterator:
                Supports overloading the iterator class to be used to process the
                datachunks. If set to ``None``, then the job UUID will be returned
                instead of an iterator.
            adopt_existing:
                Should we automatically adopt an existing Job UUID with we
                receive a 409 conflict?

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
        """
        return self._export(
            export_type='assets',
            version=None,
            iterator=iterator,
            timeout=timeout,
            export_uuid=uuid,
            adopt_existing=adopt_existing,
            payload=models.AssetExportV1(
                chunk_size=chunk_size,
                include_open_ports=include_open_ports,
                include_resource_tags=include_resource_tags,
                filters=models.AssetExportFiltersV1(
                    created_at=created_at,
                    updated_at=updated_at,
                    deleted_at=deleted_at,
                    terminated_at=terminated_at,
                    first_scan_time=first_scan_time,
                    last_authenticated_scan_time=last_authenticated_scan_time,
                    last_assessed=last_assessed,
                    is_deleted=is_deleted,
                    is_licensed=is_licensed,
                    is_terminated=is_terminated,
                    has_plugin_results=has_plugin_results,
                    servicenow_sysid=servicenow_sysid,
                    last_scan_id=last_scan_id,
                    network_id=network_id,  # ty: ignore[invalid-argument-type]
                    sources=sources,
                    tags=tags,
                ),
            ).model_dump(mode='json', exclude_none=True),
        )

    def assets_v2(
        self,
        *,
        chunk_size: int = 1000,
        include_open_ports: bool | None = None,
        include_resource_tags: bool | None = None,
        since: datetime | int | None = None,
        created_at: datetime | int | None = None,
        updated_at: datetime | int | None = None,
        deleted_at: datetime | int | None = None,
        terminated_at: datetime | int | None = None,
        first_scan_time: datetime | int | None = None,
        last_authenticated_scan_time: datetime | int | None = None,
        last_assessed: datetime | int | None = None,
        is_deleted: bool | None = None,
        is_licensed: bool | None = None,
        is_terminated: bool | None = None,
        has_plugin_results: bool | None = None,
        servicenow_sysid: bool | None = None,
        last_scan_id: str | None = None,
        network_id: UUID | str | None = None,
        sources: list[str] | None = None,
        types: list[str] | None = None,
        iterator: Type[ExportsIterator] | None = ExportsIterator,
        timeout: int | None = None,
        adopt_existing: bool = True,
        when_done: bool = False,
        uuid: UUID | str | None = None,
    ) -> ExportsIterator | UUID:
        """
        Initiate an asset v2 export.

        :devportal:`API Documentation <exports-v2-assets-request-export>`

        Args:
            last_scan_id:
                Scan uuid of the scan to be exported.
            created_at:
                Assets created after this timestamp will be returned.
            deleted_at:
                Assets deleted after this timestamp will be returned.
            first_scan_time:
                Return Assets with a first_scan time later that this timestamp will.
            last_assessed:
                Assets last scanned after this timestamp will be returned.
            last_authenticated_scan_time:
                Return Assets last scanned with an authenticated scan after this
                timestamp.
            terminated_at:
                Assets terminated after this timestamp will be returned.
            updated_at:
                Assets updated after this timestamp will be returned.
            has_plugin_results:
                Should assets only be returned if they have plugin results?
            is_deleted:
                Should we return only assets that have been deleted?
            is_licensed:
                Should we return only assets that are licensed?
            is_terminated:
                Should we return assets that have been terminated?
            servicenow_sysid:
                Should we return assets that have a ServiceNOW sysid?
                If ``True`` only assets with an id will be returned.
                If ``False`` only assets without an id will be returned.
            include_open_ports:
                Should we include open ports of assets in the exported chunks?
            chunk_size:
                How many asset objects should be returned per chunk of data?
            network_id:
                Only assets within the specified network UUID will be returned.
            sources:
                Only assets with a source matching one of these source values will be
                returned. Note that this value is case-sensitive.
            types:
                Only assets with specified type will be returned.
            since:
                Returns all assets that were updated, deleted, or terminated since the
                specified date regardless of state. The timestamp is specified in
                seconds since epoc (unix timestamp).
            uuid:
                A predefined export UUID to use for generating an ExportIterator. Using
                this parameter will ignore all of the filter arguments.
            when_done:
                When creating the iterator, setting this flag to true will tell the
                iterator to wait until the export job has completed before processing
                the first chunk.  The default behaviour is to start processing chunks
                of data as soon as they become available.
            timeout:
                If specified, determines a timeout in seconds to wait for the export \
                job to sit in the queue before cancelling the job and raising a
                ``TioExportsTimeout`` error.  Once a job has started o be processed,
                the timeout is ignored.
            iterator:
                Supports overloading the iterator class to be used to process the
                datachunks. If set to ``None``, then the job UUID will be returned
                instead of an iterator.
            adopt_existing:
                Should we automatically adopt an existing Job UUID with we
                receive a 409 conflict?

        Examples:

            Iterating over the results of an asset export:

            >>> for asset in tio.exports.assets_v2():
            ...     print(asset)

            Getting hosts that have been updated within the last 24 hours

            >>> assets = tio.exports.assets_v2(
            ...     updated_at=int(arrow.now().shift(days=-1).timestamp())
            ... )

            Getting assets that have the the ``host`` type:

            >>> assets = tio.exports.assets_v2(
            ...     types=['host']
            ... )
        """
        return self._export(
            export_type='assets',
            version='v2',
            when_done=when_done,
            iterator=iterator,
            timeout=timeout,
            export_uuid=uuid,
            adopt_existing=adopt_existing,
            payload=models.AssetExportV2(
                chunk_size=chunk_size,
                include_open_ports=include_open_ports,
                include_resource_tags=include_resource_tags,
                filters=models.AssetExportFiltersV2(
                    created_at=created_at,
                    updated_at=updated_at,
                    deleted_at=deleted_at,
                    terminated_at=terminated_at,
                    first_scan_time=first_scan_time,
                    last_authenticated_scan_time=last_authenticated_scan_time,
                    last_assessed=last_assessed,
                    is_deleted=is_deleted,
                    is_licensed=is_licensed,
                    is_terminated=is_terminated,
                    has_plugin_results=has_plugin_results,
                    servicenow_sysid=servicenow_sysid,
                    last_scan_id=last_scan_id,
                    network_id=network_id,  # ty: ignore[invalid-argument-type]
                    sources=sources,
                    types=types,
                    since=since,
                ),
            ).model_dump(mode='json', exclude_none=True),
        )

    def compliance(
        self,
        *,
        num_findings: int = 5000,
        asset: list[UUID | str] | None = None,
        last_seen: datetime | int | None = None,
        first_seen: datetime | int | None = None,
        last_observed: datetime | int | None = None,
        indexed_at: datetime | int | None = None,
        since: datetime | int | None = None,
        audit_name: str | None = None,
        audit_file_name: str | None = None,
        compliance_results: list[
            Literal['PASSED', 'FAILED', 'WARNING', 'SKIPPED', 'ERROR', 'UNKNOWN']
        ]
        | None = None,
        ipv4_addresses: list[str | IPv4Address] | None = None,
        ipv6_addresses: list[str | IPv6Address] | None = None,
        network_id: UUID | str | None = None,
        plugin_id: list[int] | None = None,
        state: list[Literal['info', 'low', 'medium', 'high', 'critical']] | None = None,
        tags: list[tuple[str, list[str] | str]] | None = None,
        iterator: Type[ExportsIterator] | None = ExportsIterator,
        when_done: bool = False,
        uuid: UUID | str | None = None,
        timeout: int | None = None,
        adopt_existing: bool = True,
    ) -> ExportsIterator | UUID:
        """
        Initiate a compliance export.

        :devportal:`API Documentation <io-exports-compliance-create>`

        Args:
            asset:
                A list of assets to return compliance results for.
            first_seen:
                Returns findings with a first seen time newer than the specified unix
                timestamp.
            last_seen:
                Returns findings with a last seen time newer than the specified unix
                timestamp.
            ipv4_addresses:
                Returns Compliance findings found for the provided list of ipv4 addresses.
            ipv6_addresses:
                Returns Compliance findings found for the provided list of ipv6 addresses.
            plugin_name:
                Returns Compliance findings for the specified list of plugin names.
            plugin_id:
                Returns Compliance findings for the specified list of plugin IDs.
            audit_name:
                Restricts compliance findings to those associated with the specified
                audit.
            audit_file_name:
                Restricts compliance findings to those associated with the specified
                audit file name.
            compliance_results:
                Restricts compliance findings to those associated with the specified
                list of compliance results, such as PASSED, FAILED, SKIPPED, ERROR,
                UNKNOWN etc.
            last_observed:
                Restricts compliance findings to those that were last observed on or
                after the specified unix timestamp.
            indexed_at:
                Restricts compliance findings to those that were updated or indexed
                into Tenable Vulnerability Management on or after the specified unix
                timestamp.
            since:
                Same as indexed_at. Restricts compliance findings to those that were
                updated or indexed into Tenable Vulnerability Management on or after
                the specified unix timestamp.
            state:
                Restricts compliance findings to those associated with the provided
                list of states, such as open, reopened and fixed.
            tags:
                A list of tag pairs to filter the results on.  The tag pairs should be
                presented as ``('CATEGORY', ['VALUE'])``.
            network_id:
                Returns Compliance findings for the specified network ID.
            num_findings:
                The number of findings to return per chunk of data.
            uuid:
                A predefined export UUID to use for generating an ExportIterator. Using
                this parameter will ignore all of the filter arguments.
            when_done:
                When creating the iterator, setting this flag to true will tell the
                iterator to wait until the export job has completed before processing
                the first chunk.  The default behaviour is to start processing chunks
                of data as soon as they become available.
            timeout:
                If specified, determines a timeout in seconds to wait for the export
                job to sit in the queue before cancelling the job and raising a
                ``TioExportsTimeout`` error. Once a job has started to be processed,
                the timeout is ignored.
            iterator:
                Supports overloading the iterator class to be used to process the
                datachunks. If set to None, then the job ID will be returned instead
                of an iterator.
            adopt_existing:
                Should we automatically adopt an existing Job UUID with we receive a
                409 conflict?

        Examples:

            >>> for findings in tio.exports.compliance():
            ...     print(finding)
        """
        return self._export(
            export_type='compliance',
            version=None,
            iterator=iterator,
            timeout=timeout,
            export_uuid=uuid,
            adopt_existing=adopt_existing,
            when_done=when_done,
            payload=models.ComplianceExportV1(
                num_findings=num_findings,
                asset=asset,  # ty: ignore[invalid-argument-type]
                filters=models.ComplianceExportFiltersV1(
                    last_seen=last_seen,
                    first_seen=first_seen,
                    last_observed=last_observed,
                    indexed_at=indexed_at,
                    since=since,
                    audit_name=audit_name,
                    audit_file_name=audit_file_name,
                    compliance_results=compliance_results,
                    ipv4_addresses=ipv4_addresses,  # ty: ignore[invalid-argument-type]
                    ipv6_addresses=ipv6_addresses,  # ty: ignore[invalid-argument-type]
                    network_id=network_id,  # ty: ignore[invalid-argument-type]
                    plugin_id=plugin_id,
                    state=state,
                    tags=tags,
                ),
            ).model_dump(mode='json', exclude_none=True),
        )

    def vulns(
        self,
        *,
        num_assets: int = 500,
        include_unlicensed: bool = True,
        since: datetime | int | None = None,
        first_found: datetime | int | None = None,
        first_seen: datetime | int | None = None,
        last_found: datetime | int | None = None,
        last_seen: datetime | int | None = None,
        last_fixed: datetime | int | None = None,
        resurfaced_date: datetime | int | None = None,
        indexed_at: datetime | int | None = None,
        time_taken_to_fix: dict[str, int] | None = None,
        cvss4_base_score: dict[str, float] | None = None,
        epss_score: dict[str, float] | None = None,
        cidr_range: IPv4Network | str | None = None,
        cve_id: list[str] | None = None,
        cve_category: list[
            Literal[
                'cisa known exploitable',
                'emerging threats',
                'in the news',
                'persistently exploited',
                'ransomware',
                'recent active exploitation',
                'top 50 vpr',
            ]
        ]
        | None = None,
        exploit_maturity: list[Literal['high', 'functional', 'poc', 'unproven']]
        | None = None,
        initiative_id: UUID | str | None = None,
        network_id: UUID | str | None = None,
        plugin_family: list[str] | None = None,
        plugin_id: list[int] | None = None,
        plugin_type: str | None = None,
        scan_uuid: UUID | str | None = None,
        severity: list[Literal['info', 'low', 'medium', 'high', 'critical']]
        | None = None,
        severity_modification_type: list[Literal['NONE', 'ACCEPTED', 'RECASTED']]
        | None = None,
        state: list[Literal['OPEN', 'REOPENED', 'FIXED']] | None = None,
        source: list[str] | None = None,
        vpr_score: dict[str, float] | None = None,
        vpr_v2_score: dict[str, float] | None = None,
        vpr_threat_intensity: list[
            Literal['very high', 'high', 'medium', 'low', 'very low']
        ]
        | None = None,
        weaponization: list[
            Literal['apt', 'botnet', 'malware', 'ransomware', 'rootkit']
        ]
        | None = None,
        tags: list[tuple[str, list[str] | str]] | None = None,
        uuid: UUID | str | None = None,
        timeout: int | None = None,
        when_done: bool = False,
        adopt_existing: bool = True,
        iterator: Type[ExportsIterator] | None = ExportsIterator,
    ) -> ExportsIterator | UUID:
        """
        Initiate a vulnerability export.

        :devportal:`API Documentation <exports-vulns-request-export>`

        Args:
            first_found:
                Findings first discovered after this timestamp will be returned.
            indexed_at:
                Findings indexed into Tenable Vulnerability Management after this
                timestamp will be returned.
            last_fixed:
                Findings fixed after this timestamp will be returned. Note that this
                filter only applies to fixed data and should not be used when searching
                for active findings.
            last_found:
                Findings last observed after this timestamp will be returned.
            since:
                Findings last observed in any state after this timestamp will be
                returned.  Cannot be used with ``last_found``, ``first_found``,
                or ``last_fixed``.
            resurfaced_date:
                Returns findings that have been resurfaced on or after this datetime.
            time_taken_to_fix:
                Returns findings based on how long that it took the organization to
                resolve. The export will only inclucled ``FIXED`` findings when this
                filter is applied.  Supported keys are
                ``lte`` for *Less Than or Equal to* or
                ``gte`` for *Greater Than or Equal to*.
                The values should be in seconds.
            plugin_family:
                Only return findings from the specified plugin families.
            plugin_id:
                Only return findings from the specified plugin ids.
            plugin_type:
                Only return findings with the specified plugin type.
            scan_uuid:
                Only return findings with the specified scan UUID.
            source:
                Only return vulnerabilities for assets that have the specified scan source.
            severity_modification_type:
                Only return vulnerabilities with the specified severity modification type.
            severity:
                Only return findings with the specified severities.
            state:
                Only return findings with the specified states.
            vpr_score:
                Only returns findings that meet the specified VPR criteria. The filter
                is formatted as a dictionary with the mathematical operation as the
                key. Supported operations are:

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
            network_id:
                Only findings within the specified network UUID will be
                returned.
            cidr_range:
                Restrict the export to only vulns assigned to assets within the
                CIDR range specified.
            tags:
                A list of tag pairs to filter the results on.  The tag pairs should be
                presented as ``('CATEGORY', 'VALUE')``.
            include_unlicensed:
                Should findings for unlicensed assets that be included in the results?
            num_assets:
                As findings are grouped by asset, how many assets's findings should
                exist within each data chunk?
            uuid:
                A predefined export UUID to use for generating an ExportIterator. Using
                this parameter will ignore all of the filter arguments.
            when_done:
                When creating the iterator, setting this flag to true will tell the
                iterator to wait until the export job has completed before processing
                the first chunk.  The default behaviour is to start processing chunks
                of data as soon as they become available.
            timeout:
                If specified, determines a timeout in seconds to wait for the export
                job to sit in the queue before cancelling the job and raising a
                ``TioExportsTimeout`` error. Once a job has started to be processed,
                the timeout is ignored.
            iterator:
                Supports overloading the iterator class to be used to process the
                datachunks. If set to None, then the job ID will be returned instead
                of an iterator.
            adopt_existing:
                Should we automatically adopt an existing Job UUID with we receive a
                409 conflict?
            cve_id:
                Returns findings that match the specified CVE IDs.
            cve_category:
                Returns findings the match the specified CVE category. For more
                information about categories, see the *Vulnerability Categories*
                section in the _Tenable Vulnerability Management User Guide_.
            exploit_maturity:
                Returns findings that match the specified exploit maturity. Tenable
                assigns exploit maturity values to vulnerabilities based on the
                availability and sophistication of exploit code. Supported values are
                ``high``, ``functional``, ``poc``, ``unproven``.
            vpr_threat_intensity:
                Returns findings that match the specified threat intensity. The threat
                intensity of a vulnerability is based onf the number and frequency of
                recently observed events. Supported values are ``very high``, ``high``,
                ``medium``, ``low``, ``very low``.
            weaponization:
                Returns findings that match the specified weaponizations. Weaponized
                vulnerabilities are vulnerabilities that are ready for use in a
                particular type of attack. Supported values are ``apt``, ``botnet``,
                ``malware``, ``ransomware``, ``rootkit``.

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
        """
        return self._export(
            export_type='vulns',
            version=None,
            when_done=when_done,
            iterator=iterator,
            timeout=timeout,
            export_uuid=uuid,
            adopt_existing=adopt_existing,
            payload=models.VulnerabilityExportV1(
                num_assets=num_assets,
                include_unlicensed=include_unlicensed,
                filters=models.VulnerabilityExportFiltersV1(
                    since=since,
                    first_found=first_found,
                    first_seen=first_seen,
                    last_found=last_found,
                    last_seen=last_seen,
                    indexed_at=indexed_at,
                    last_fixed=last_fixed,
                    resurfaced_date=resurfaced_date,
                    time_taken_to_fix=time_taken_to_fix,  # ty: ignore[invalid-argument-type]
                    cidr_range=cidr_range,  # ty: ignore[invalid-argument-type]
                    cve_id=cve_id,
                    cve_category=cve_category,
                    cvss4_base_score=cvss4_base_score,  # ty: ignore[invalid-argument-type]
                    epss_score=epss_score,  # ty: ignore[invalid-argument-type]
                    exploit_maturity=exploit_maturity,
                    initiative_id=initiative_id,  # ty: ignore[invalid-argument-type]
                    network_id=network_id,  # ty: ignore[invalid-argument-type]
                    plugin_family=plugin_family,
                    plugin_id=plugin_id,
                    plugin_type=plugin_type,
                    scan_uuid=scan_uuid,  # ty: ignore[invalid-argument-type]
                    severity=severity,
                    severity_modification_type=severity_modification_type,
                    state=state,
                    source=source,
                    vpr_score=vpr_score,  # ty: ignore[invalid-argument-type]
                    vpr_v2_score=vpr_v2_score,  # ty: ignore[invalid-argument-type]
                    vpr_threat_intensity=vpr_threat_intensity,
                    weaponization=weaponization,
                    tags=tags,
                ),
            ).model_dump(mode='json', exclude_none=True),
        )

    def was(
        self,
        *,
        num_assets: int = 500,
        include_unlicensed: bool = True,
        since: datetime | int | None = None,
        first_found: datetime | int | None = None,
        last_fixed: datetime | int | None = None,
        last_found: datetime | int | None = None,
        indexed_at: datetime | int | None = None,
        asset_uuid: list[UUID | str] | None = None,
        asset_name: str | None = None,
        cvss4_base_score: dict[str, float] | None = None,
        epss_score: dict[str, float] | None = None,
        ipv4s: list[IPv4Address | str] | None = None,
        owasp_2010: list[
            Literal['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
        ]
        | None = None,
        owasp_2013: list[
            Literal['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
        ]
        | None = None,
        owasp_2017: list[
            Literal['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
        ]
        | None = None,
        owasp_2021: list[
            Literal['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
        ]
        | None = None,
        owasp_api_2019: list[
            Literal[
                'API1',
                'API2',
                'API3',
                'API4',
                'API5',
                'API6',
                'API7',
                'API8',
                'API9',
                'API10',
            ]
        ]
        | None = None,
        plugin_ids: list[int] | None = None,
        severity: list[Literal['info', 'low', 'medium', 'high', 'critical']]
        | None = None,
        severity_modification_type: list[Literal['NONE', 'ACCEPTED', 'RECASTED']]
        | None = None,
        state: list[Literal['OPEN', 'REOPENED', 'FIXED']] | None = None,
        vpr_score: dict[str, float] | None = None,
        vpr_v2_score: dict[str, float] | None = None,
        uuid: UUID | str | None = None,
        timeout: int | None = None,
        when_done: bool = False,
        adopt_existing: bool = True,
        iterator: Type[ExportsIterator] | None = ExportsIterator,
    ) -> ExportsIterator | UUID:
        """
        Initiate a WAS vulnerability export.
        :devportal:`API Documentation <was-export-findings>`
        Args:
            first_found:
                Findings first discovered after this timestamp will be returned.
            indexed_at:
                Findings indexed after this timestamp will be returned.
            last_fixed:
                Findings fixed after this timestamp will be returned. Note that this
                filter only applies to fixed data and should not be used when searching
                for active findings.
            last_found:
                Findings last observed after this timestamp will be returned.
            since:
                Findings last observed in any state after this timestamp will be
                returned.  Cannot be used with ``last_found``, ``first_found``, or
                ``last_fixed``.
            plugin_ids:
                Only return findings from the specified plugin ids.
            asset_uuid:
                Only return findings for the assets with specific asset-uuids.
            asset_name:
                Only return findings for the asset with given name.
            owasp_2010:
                A list of chapters from the OWASP Categories 2010 report for which you
                want to filter findings returned in the findings export.
            owasp_2013:
                A list of chapters from the OWASP Categories 2013 report for which you
                want to filter findings returned in the findings export.
            owasp_2017:
                A list of chapters from the OWASP Categories 2017 report for which you
                want to filter findings returned in the findings export.
            owasp_2021:
                A list of chapters from the OWASP Categories 2021 report for which you
                want to filter findings returned in the findings export.
            owasp_api_2019:
                A list of chapters from the OWASP Categories API 2019 report for which
                you want to filter findings returned in the findings export.
            severity_modification_type:
                Only return vulnerabilities with the specified modification type.
            severity:
                Only return findings with the specified severities.
            state:
                Only return findings with the specified states.
            vpr_score:
                Only returns findings that meet the specified VPR criteria. The filter
                is formatted as a dictionary with the mathematical operation as the key.
                Supported operations are:

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
            ipv4s:
                Restrict the export to only vulns assigned to assets with specific
                ip-addresses.
            include_unlicensed:
                Should findings for assets that are not licensed be included in
                the results?
            num_assets:
                As findings are grouped by asset, how many assets' findings
                should exist within each data chunk.
            uuid:
                A predefined export UUID to use for generating an ExportIterator. Using
                this parameter will ignore all the filter arguments.
            when_done:
                When creating the iterator, setting this flag to true will tell the
                iterator to wait until the export job has completed before processing
                the first chunk.  The default behaviour is to start processing chunks
                of data as soon as they become available.
            timeout:
                If specified, determines a timeout in seconds to wait for the export
                job to sit in the queue before cancelling the job and raising a
                ``TioExportsTimeout`` error.  Once a job has started to be processed,
                the timeout is ignored.
            iterator:
                Supports overloading the iterator class to be used to process the
                datachunks. If set to None, then the job ID will be returned instead
                of an iterator.
            adopt_existing:
                Should we automatically adopt an existing Job UUID with we receive a
                409 conflict?

        Examples:

            Iterating over the results of a WAS vuln export:
            >>> from tenable.io import TenableIO
            >>> tio = TenableIO("<apiKey>", "secret")
            >>> for vuln in tio.exports.was_vulns():
            ...     print(vuln)

            Getting findings that have been observed within the last 24 hours
            >>> import arrow
            >>> vulns = tio.exports.was(
            ...     since=int(arrow.now().shift(days=-1).timestamp())
            ... )
        """
        return self._export(
            export_type='was',
            version=None,
            when_done=when_done,
            iterator=iterator,
            timeout=timeout,
            export_uuid=uuid,
            adopt_existing=adopt_existing,
            payload=models.WASExportV1(
                num_assets=num_assets,
                include_unlicensed=include_unlicensed,
                filters=models.WASExportFiltersV1(
                    since=since,
                    first_found=first_found,
                    last_found=last_found,
                    indexed_at=indexed_at,
                    last_fixed=last_fixed,
                    asset_uuid=asset_uuid,  # ty: ignore[invalid-argument-type]
                    asset_name=asset_name,
                    cvss4_base_score=cvss4_base_score,  # ty: ignore[invalid-argument-type]
                    epss_score=epss_score,  # ty: ignore[invalid-argument-type]
                    ipv4s=ipv4s,  # ty: ignore[invalid-argument-type]
                    plugin_ids=plugin_ids,
                    owasp_2010=owasp_2010,
                    owasp_2013=owasp_2013,
                    owasp_2017=owasp_2017,
                    owasp_2021=owasp_2021,
                    owasp_api_2019=owasp_api_2019,
                    severity=severity,
                    severity_modification_type=severity_modification_type,
                    state=state,
                    vpr_score=vpr_score,  # ty: ignore[invalid-argument-type]
                    vpr_v2_score=vpr_v2_score,  # ty: ignore[invalid-argument-type]
                ),
            ).model_dump(mode='json', exclude_none=True),
        )
