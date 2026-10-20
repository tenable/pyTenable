from typing import Any, Literal
from uuid import UUID

from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.cloud._common import AcceptedResponse, accepted_error_map
from tenable.utils import scrub

from .models.assets import (
    AcrReason,
    Asset,
    AssetAcrUpdateRequest,
    AssetDeleteRequest,
    AssetImport,
    AssetImportCreateResponse,
    AssetImportJob,
    AssetImportJobListResponse,
    AssetImportRequest,
    AssetListResponse,
    AssetMoveRequest,
    AssetQueryFilter,
    AssetSummary,
    BulkJobResponse,
)

AssetFilter = AssetQueryFilter | tuple[str, str, str] | str


class AssetsAPI(APIEndpoint):
    _path = "/assets"

    def _bulk_job(self, path: str, *, json: Any) -> bytes:
        # The bulk job endpoints live outside of the /assets path and respond with a
        # 202 Accepted, so we call the client directly and recover the response body.
        try:
            resp = self._client._post(
                path, json=json, error_map=accepted_error_map(self._client)
            )
        except AcceptedResponse as accepted:
            resp = accepted.response
        return resp.content

    def get(self) -> list[AssetSummary]:
        """
        Returns up to 5,000 assets. Use the asset exports to retrieve all assets.

        Returns:
            List of asset summary objects.
        """
        resp = self._get(response_model=AssetListResponse)
        return resp.assets

    def details(self, asset_id: UUID | str) -> Asset:
        """
        Returns the details for the specified asset.

        Args:
            asset_id: The UUID of the asset.

        Returns:
            Requested asset object.
        """
        return self._get(f"/{scrub(asset_id)}", response_model=Asset)

    def update_acr(
        self,
        score: int,
        *,
        asset_ids: list[UUID | str] | None = None,
        fqdns: list[str] | None = None,
        ipv4s: list[str] | None = None,
        mac_addresses: list[str] | None = None,
        netbios_names: list[str] | None = None,
        reasons: list[AcrReason] | None = None,
        note: str | None = None,
    ) -> None:
        """
        Overwrites the Tenable-provided Asset Criticality Rating (ACR) for the matching
        assets. Requires a Tenable Lumin license. At least one asset identifier must
        be provided.

        Args:
            score: The ACR to assign to the assets. Must be from ``1`` to ``10``.
            asset_ids: The UUIDs of the assets to update.
            fqdns: The FQDNs of the assets to update.
            ipv4s: The IPv4 addresses of the assets to update.
            mac_addresses: The MAC addresses of the assets to update.
            netbios_names: The NetBIOS names of the assets to update.
            reasons: The reasons for updating the ACR.
            note: Any notes to clarify the circumstances behind the update.

        Example:
            >>> cloud.vm.assets.update_acr(
            ...     8,
            ...     asset_ids=["436224b4-e3e7-4761-ad47-e32daaebec6b"],
            ...     reasons=["Business Critical"],
            ... )
        """
        self._bulk_job(
            "/api/v2/assets/bulk-jobs/acr",
            json=AssetAcrUpdateRequest.model_validate(
                [
                    {
                        "acr_score": score,
                        "reason": reasons,
                        "note": note,
                        "asset": [
                            {
                                "id": asset_ids,
                                "fqdn": fqdns,
                                "ipv4": ipv4s,
                                "mac_address": mac_addresses,
                                "netbios_name": netbios_names,
                            }
                        ],
                    }
                ]
            ),
        )

    def move(
        self,
        source: UUID | str,
        destination: UUID | str,
        targets: list[str] | str,
    ) -> int:
        """
        Moves assets from one network to another.

        Args:
            source: The UUID of the network the assets are currently assigned to.
            destination: The UUID of the network to move the assets to.
            targets:
                The IPv4 addresses of the assets to move. Each entry may be an
                address, a range, or a CIDR (e.g. ``"192.0.2.0/24"``).

        Returns:
            The number of assets moved.

        Example:
            >>> cloud.vm.assets.move(
            ...     "00000000-0000-0000-0000-000000000000",
            ...     "4dee97b4-592b-4b5b-a8a9-d7a605a3723a",
            ...     ["192.0.2.57-192.0.2.69", "198.51.100.0/24"],
            ... )
        """
        resp = self._bulk_job(
            "/api/v2/assets/bulk-jobs/move-to-network",
            json=AssetMoveRequest.model_validate(
                {"source": source, "destination": destination, "targets": targets}
            ),
        )
        return BulkJobResponse.model_validate_json(resp).response.data.asset_count

    def bulk_delete(
        self,
        *filters: AssetFilter,
        filter_type: Literal["and", "or"] = "and",
        hard_delete: bool | None = None,
    ) -> int:
        """
        Deletes the assets matching the specified filters. The available filters can
        be retrieved with ``platform.filters.asset()``.

        Args:
            *filters:
                The asset filters to match against. Filters may be passed as
                ``(field, operator, value)`` tuples or ``"field:operator:value"``
                strings.
            filter_type:
                Should the assets match ``"and"`` all of the filters, or ``"or"``
                any of them? Defaults to ``"and"``.
            hard_delete:
                Should the assets be completely removed (including from your license
                count and all vulnerability data)?

        Returns:
            The number of assets deleted.

        Example:
            >>> cloud.vm.assets.bulk_delete(
            ...     ("host.hostname", "match", "example"),
            ...     "ipv4:eq:192.0.2.1",
            ...     filter_type="or",
            ... )
        """
        if not filters:
            raise ValueError("At least one filter is required.")
        resp = self._bulk_job(
            "/api/v2/assets/bulk-jobs/delete",
            json=AssetDeleteRequest.model_validate(
                {"query": {filter_type: list(filters)}, "hard_delete": hard_delete}
            ),
        )
        return BulkJobResponse.model_validate_json(resp).response.data.asset_count

    def import_jobs(self) -> list[AssetImportJob]:
        """
        Returns the list of asset import jobs.

        Returns:
            List of asset import job objects.
        """
        resp = self._client._get(
            "/import/asset-jobs", response_model=AssetImportJobListResponse
        )
        return resp.asset_import_jobs

    def import_job_details(self, job_id: UUID | str) -> AssetImportJob:
        """
        Returns the details for the specified asset import job.

        Args:
            job_id: The UUID of the asset import job.

        Returns:
            Requested asset import job object.
        """
        return self._client._get(
            f"/import/asset-jobs/{scrub(job_id)}", response_model=AssetImportJob
        )

    def import_assets(
        self, source: str, assets: list[AssetImport | dict[str, Any]]
    ) -> UUID:
        """
        Imports asset records into Tenable Vulnerability Management. The request size
        cannot exceed 5 MB. Imported assets are always assigned to the default network.

        Args:
            source:
                A user-defined name for the source of the import containing the asset
                records.
            assets:
                The asset records to import. Each record requires at least one of
                ``fqdn``, ``ipv4``, ``netbios_name``, or ``mac_address``.

        Returns:
            The UUID of the asset import job.

        Example:
            >>> job_id = cloud.vm.assets.import_assets(
            ...     "Custom Import",
            ...     [{"ipv4": ["192.0.2.57"], "operating_system": ["Windows 7 x64"]}],
            ... )
        """
        resp: AssetImportCreateResponse = self._client._post(
            "/import/assets",
            json=AssetImportRequest.model_validate(
                {"source": source, "assets": assets}
            ),
            response_model=AssetImportCreateResponse,
        )
        return resp.job_id


class AsyncAssetsAPI(AsyncAPIEndpoint):
    _path = "/assets"

    async def _bulk_job(self, path: str, *, json: Any) -> bytes:
        # The bulk job endpoints live outside of the /assets path and respond with a
        # 202 Accepted, so we call the client directly and recover the response body.
        try:
            resp = await self._client._post(
                path, json=json, error_map=accepted_error_map(self._client)
            )
        except AcceptedResponse as accepted:
            resp = accepted.response
        return resp.content

    async def get(self) -> list[AssetSummary]:
        """
        Returns up to 5,000 assets. Use the asset exports to retrieve all assets.

        Returns:
            List of asset summary objects.
        """
        resp = await self._get(response_model=AssetListResponse)
        return resp.assets

    async def details(self, asset_id: UUID | str) -> Asset:
        """
        Returns the details for the specified asset.

        Args:
            asset_id: The UUID of the asset.

        Returns:
            Requested asset object.
        """
        return await self._get(f"/{scrub(asset_id)}", response_model=Asset)

    async def update_acr(
        self,
        score: int,
        *,
        asset_ids: list[UUID | str] | None = None,
        fqdns: list[str] | None = None,
        ipv4s: list[str] | None = None,
        mac_addresses: list[str] | None = None,
        netbios_names: list[str] | None = None,
        reasons: list[AcrReason] | None = None,
        note: str | None = None,
    ) -> None:
        """
        Overwrites the Tenable-provided Asset Criticality Rating (ACR) for the matching
        assets. Requires a Tenable Lumin license. At least one asset identifier must
        be provided.

        Args:
            score: The ACR to assign to the assets. Must be from ``1`` to ``10``.
            asset_ids: The UUIDs of the assets to update.
            fqdns: The FQDNs of the assets to update.
            ipv4s: The IPv4 addresses of the assets to update.
            mac_addresses: The MAC addresses of the assets to update.
            netbios_names: The NetBIOS names of the assets to update.
            reasons: The reasons for updating the ACR.
            note: Any notes to clarify the circumstances behind the update.

        Example:
            >>> await cloud.vm.assets.update_acr(
            ...     8,
            ...     asset_ids=["436224b4-e3e7-4761-ad47-e32daaebec6b"],
            ...     reasons=["Business Critical"],
            ... )
        """
        await self._bulk_job(
            "/api/v2/assets/bulk-jobs/acr",
            json=AssetAcrUpdateRequest.model_validate(
                [
                    {
                        "acr_score": score,
                        "reason": reasons,
                        "note": note,
                        "asset": [
                            {
                                "id": asset_ids,
                                "fqdn": fqdns,
                                "ipv4": ipv4s,
                                "mac_address": mac_addresses,
                                "netbios_name": netbios_names,
                            }
                        ],
                    }
                ]
            ),
        )

    async def move(
        self,
        source: UUID | str,
        destination: UUID | str,
        targets: list[str] | str,
    ) -> int:
        """
        Moves assets from one network to another.

        Args:
            source: The UUID of the network the assets are currently assigned to.
            destination: The UUID of the network to move the assets to.
            targets:
                The IPv4 addresses of the assets to move. Each entry may be an
                address, a range, or a CIDR (e.g. ``"192.0.2.0/24"``).

        Returns:
            The number of assets moved.

        Example:
            >>> await cloud.vm.assets.move(
            ...     "00000000-0000-0000-0000-000000000000",
            ...     "4dee97b4-592b-4b5b-a8a9-d7a605a3723a",
            ...     ["192.0.2.57-192.0.2.69", "198.51.100.0/24"],
            ... )
        """
        resp = await self._bulk_job(
            "/api/v2/assets/bulk-jobs/move-to-network",
            json=AssetMoveRequest.model_validate(
                {"source": source, "destination": destination, "targets": targets}
            ),
        )
        return BulkJobResponse.model_validate_json(resp).response.data.asset_count

    async def bulk_delete(
        self,
        *filters: AssetFilter,
        filter_type: Literal["and", "or"] = "and",
        hard_delete: bool | None = None,
    ) -> int:
        """
        Deletes the assets matching the specified filters. The available filters can
        be retrieved with ``platform.filters.asset()``.

        Args:
            *filters:
                The asset filters to match against. Filters may be passed as
                ``(field, operator, value)`` tuples or ``"field:operator:value"``
                strings.
            filter_type:
                Should the assets match ``"and"`` all of the filters, or ``"or"``
                any of them? Defaults to ``"and"``.
            hard_delete:
                Should the assets be completely removed (including from your license
                count and all vulnerability data)?

        Returns:
            The number of assets deleted.

        Example:
            >>> await cloud.vm.assets.bulk_delete(
            ...     ("host.hostname", "match", "example"),
            ...     "ipv4:eq:192.0.2.1",
            ...     filter_type="or",
            ... )
        """
        if not filters:
            raise ValueError("At least one filter is required.")
        resp = await self._bulk_job(
            "/api/v2/assets/bulk-jobs/delete",
            json=AssetDeleteRequest.model_validate(
                {"query": {filter_type: list(filters)}, "hard_delete": hard_delete}
            ),
        )
        return BulkJobResponse.model_validate_json(resp).response.data.asset_count

    async def import_jobs(self) -> list[AssetImportJob]:
        """
        Returns the list of asset import jobs.

        Returns:
            List of asset import job objects.
        """
        resp = await self._client._get(
            "/import/asset-jobs", response_model=AssetImportJobListResponse
        )
        return resp.asset_import_jobs

    async def import_job_details(self, job_id: UUID | str) -> AssetImportJob:
        """
        Returns the details for the specified asset import job.

        Args:
            job_id: The UUID of the asset import job.

        Returns:
            Requested asset import job object.
        """
        return await self._client._get(
            f"/import/asset-jobs/{scrub(job_id)}", response_model=AssetImportJob
        )

    async def import_assets(
        self, source: str, assets: list[AssetImport | dict[str, Any]]
    ) -> UUID:
        """
        Imports asset records into Tenable Vulnerability Management. The request size
        cannot exceed 5 MB. Imported assets are always assigned to the default network.

        Args:
            source:
                A user-defined name for the source of the import containing the asset
                records.
            assets:
                The asset records to import. Each record requires at least one of
                ``fqdn``, ``ipv4``, ``netbios_name``, or ``mac_address``.

        Returns:
            The UUID of the asset import job.

        Example:
            >>> job_id = await cloud.vm.assets.import_assets(
            ...     "Custom Import",
            ...     [{"ipv4": ["192.0.2.57"], "operating_system": ["Windows 7 x64"]}],
            ... )
        """
        resp: AssetImportCreateResponse = await self._client._post(
            "/import/assets",
            json=AssetImportRequest.model_validate(
                {"source": source, "assets": assets}
            ),
            response_model=AssetImportCreateResponse,
        )
        return resp.job_id
