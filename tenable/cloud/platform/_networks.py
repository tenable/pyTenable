from uuid import UUID

from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.utils import scrub

from .iterators import AsyncPaginationV1Iterator, PaginationV1Iterator
from .models.networks import (
    Network,
    NetworkAssetCount,
    NetworkCreate,
    NetworkListResponse,
    NetworkQueryParams,
    NetworkScanner,
    NetworkScannerBulkAssign,
    NetworkScannerListResponse,
)


class NetworksIterator(PaginationV1Iterator):
    path: str
    page: list[Network]
    params: NetworkQueryParams
    _method = "platform.networks._list_networks"


class AsyncNetworksIterator(AsyncPaginationV1Iterator):
    path: str
    page: list[Network]
    params: NetworkQueryParams
    _method = "platform.networks._list_networks"


class NetworksAPI(APIEndpoint):
    _path = "/networks"

    def _list_networks(
        self, *, path: str, params: NetworkQueryParams
    ) -> NetworkListResponse:
        return self._client._get(
            path, params=params, response_model=NetworkListResponse
        )

    def get(
        self,
        *,
        limit: int = 50,
        sort: str | None = None,
        include_deleted: bool | None = None,
    ) -> NetworksIterator:
        """
        Returns an iterator of network objects.

        Args:
            limit: Number of records to retrieve per page. Defaults to ``50``.
            sort:
                Sort expression, e.g. ``"name:asc"``.
            include_deleted:
                Whether to include deleted network objects in the response.

        Returns:
            Iterator yielding network objects.
        """
        params = NetworkQueryParams.model_validate(
            {"limit": limit, "sort": sort, "includeDeleted": include_deleted}
        )
        return NetworksIterator(self._client, path=self._path, params=params)

    def details(self, network_id: UUID | str) -> Network:
        """
        Returns the details for the specified network object.

        Args:
            network_id: The UUID of the network object.

        Returns:
            Requested network object.
        """
        return self._get(f"/{scrub(network_id)}", response_model=Network)

    def create(
        self,
        name: str,
        *,
        description: str | None = None,
        assets_ttl_days: int | None = None,
    ) -> Network:
        """
        Creates a new network object.

        Args:
            name: The name of the new network object.
            description: Description of the new network object.
            assets_ttl_days:
                The number of days to wait before assets age out. Minimum
                value is ``14``, maximum value is ``365``.

        Returns:
            Created network object.
        """
        return self._post(
            response_model=Network,
            json=NetworkCreate(
                name=name, description=description, assets_ttl_days=assets_ttl_days
            ),
        )

    def update(
        self,
        network_id: UUID | str,
        *,
        name: str | None = None,
        description: str | None = None,
        assets_ttl_days: int | None = None,
    ) -> Network:
        """
        Updates an existing network object. The default network object
        cannot be updated.

        Args:
            network_id: The UUID of the network object to update.
            name: New name of the network object.
            description: New description for the network object.
            assets_ttl_days: New assets TTL, in days, for the network object.

        Returns:
            Updated network object.
        """
        net = self.details(network_id)
        updated = NetworkCreate(
            name=name if name is not None else net.name,
            description=description if description is not None else net.description,
            assets_ttl_days=(
                assets_ttl_days if assets_ttl_days is not None else net.assets_ttl_days
            ),
        )
        return self._put(f"/{scrub(network_id)}", json=updated, response_model=Network)

    def delete(self, network_id: UUID | str) -> None:
        """
        Deletes the specified network object. The default network object
        cannot be deleted.

        Args:
            network_id: The UUID of the network object to delete.
        """
        self._delete(f"/{scrub(network_id)}")

    def asset_count(self, network_id: UUID | str, num_days: int) -> NetworkAssetCount:
        """
        Returns the total number of assets in the network along with the
        number of assets that have not been seen for the specified number of
        days.

        Args:
            network_id: The UUID of the network object.
            num_days:
                Return a count of assets that have not been seen for this
                number of days. Minimum value is ``1``, maximum value is
                ``365``.

        Returns:
            The network's asset counts.
        """
        return self._get(
            f"/{scrub(network_id)}/counts/assets-not-seen-in/{int(num_days)}",
            response_model=NetworkAssetCount,
        )

    def list_scanners(self, network_id: UUID | str) -> list[NetworkScanner]:
        """
        Lists all scanners and scanner groups assigned to the specified
        network object.

        Args:
            network_id: The UUID of the network object.

        Returns:
            List of scanner objects assigned to the network.
        """
        resp = self._get(
            f"/{scrub(network_id)}/scanners", response_model=NetworkScannerListResponse
        )
        return resp.scanners

    def assignable_scanners(self, network_id: UUID | str) -> list[NetworkScanner]:
        """
        Lists all scanners and scanner groups not yet assigned to a custom
        network object.

        Args:
            network_id: The UUID of the default network object.

        Returns:
            List of scanner objects assignable to a custom network.
        """
        resp = self._get(
            f"/{scrub(network_id)}/assignable-scanners",
            response_model=NetworkScannerListResponse,
        )
        return resp.scanners

    def assign_scanner(self, network_id: UUID | str, scanner_uuid: UUID | str) -> None:
        """
        Assigns a single scanner or scanner group to a network object.

        Args:
            network_id: The UUID of the network object.
            scanner_uuid: The UUID of the scanner or scanner group to assign.
        """
        self._post(f"/{scrub(network_id)}/scanners/{scrub(scanner_uuid)}")

    def assign_scanners(
        self, network_id: UUID | str, scanner_uuids: list[UUID | str]
    ) -> None:
        """
        Bulk assigns scanners and scanner groups to a network object. This
        overwrites the full list of scanners and scanner groups previously
        assigned to the network object; any scanners or scanner groups
        omitted from ``scanner_uuids`` are returned to the default network.

        Args:
            network_id: The UUID of the network object.
            scanner_uuids: The UUIDs of the scanners and scanner groups to assign.
        """
        self._post(
            f"/{scrub(network_id)}/scanners",
            json=NetworkScannerBulkAssign.model_validate(
                {"scanner_uuids": scanner_uuids}
            ),
        )


class AsyncNetworksAPI(AsyncAPIEndpoint):
    _path = "/networks"

    async def _list_networks(
        self, *, path: str, params: NetworkQueryParams
    ) -> NetworkListResponse:
        return await self._client._get(
            path, params=params, response_model=NetworkListResponse
        )

    async def get(
        self,
        *,
        limit: int = 50,
        sort: str | None = None,
        include_deleted: bool | None = None,
    ) -> AsyncNetworksIterator:
        """
        Returns an async iterator of network objects.

        Args:
            limit: Number of records to retrieve per page. Defaults to ``50``.
            sort:
                Sort expression, e.g. ``"name:asc"``.
            include_deleted:
                Whether to include deleted network objects in the response.

        Returns:
            Async iterator yielding network objects.
        """
        params = NetworkQueryParams.model_validate(
            {"limit": limit, "sort": sort, "includeDeleted": include_deleted}
        )
        return AsyncNetworksIterator(self._client, path=self._path, params=params)

    async def details(self, network_id: UUID | str) -> Network:
        """
        Returns the details for the specified network object.

        Args:
            network_id: The UUID of the network object.

        Returns:
            Requested network object.
        """
        return await self._get(f"/{scrub(network_id)}", response_model=Network)

    async def create(
        self,
        name: str,
        *,
        description: str | None = None,
        assets_ttl_days: int | None = None,
    ) -> Network:
        """
        Creates a new network object.

        Args:
            name: The name of the new network object.
            description: Description of the new network object.
            assets_ttl_days:
                The number of days to wait before assets age out. Minimum
                value is ``14``, maximum value is ``365``.

        Returns:
            Created network object.
        """
        return await self._post(
            response_model=Network,
            json=NetworkCreate(
                name=name, description=description, assets_ttl_days=assets_ttl_days
            ),
        )

    async def update(
        self,
        network_id: UUID | str,
        *,
        name: str | None = None,
        description: str | None = None,
        assets_ttl_days: int | None = None,
    ) -> Network:
        """
        Updates an existing network object. The default network object
        cannot be updated.

        Args:
            network_id: The UUID of the network object to update.
            name: New name of the network object.
            description: New description for the network object.
            assets_ttl_days: New assets TTL, in days, for the network object.

        Returns:
            Updated network object.
        """
        net = await self.details(network_id)
        updated = NetworkCreate(
            name=name if name is not None else net.name,
            description=description if description is not None else net.description,
            assets_ttl_days=(
                assets_ttl_days if assets_ttl_days is not None else net.assets_ttl_days
            ),
        )
        return await self._put(
            f"/{scrub(network_id)}", json=updated, response_model=Network
        )

    async def delete(self, network_id: UUID | str) -> None:
        """
        Deletes the specified network object. The default network object
        cannot be deleted.

        Args:
            network_id: The UUID of the network object to delete.
        """
        await self._delete(f"/{scrub(network_id)}")

    async def asset_count(
        self, network_id: UUID | str, num_days: int
    ) -> NetworkAssetCount:
        """
        Returns the total number of assets in the network along with the
        number of assets that have not been seen for the specified number of
        days.

        Args:
            network_id: The UUID of the network object.
            num_days:
                Return a count of assets that have not been seen for this
                number of days. Minimum value is ``1``, maximum value is
                ``365``.

        Returns:
            The network's asset counts.
        """
        return await self._get(
            f"/{scrub(network_id)}/counts/assets-not-seen-in/{int(num_days)}",
            response_model=NetworkAssetCount,
        )

    async def list_scanners(self, network_id: UUID | str) -> list[NetworkScanner]:
        """
        Lists all scanners and scanner groups assigned to the specified
        network object.

        Args:
            network_id: The UUID of the network object.

        Returns:
            List of scanner objects assigned to the network.
        """
        resp = await self._get(
            f"/{scrub(network_id)}/scanners", response_model=NetworkScannerListResponse
        )
        return resp.scanners

    async def assignable_scanners(self, network_id: UUID | str) -> list[NetworkScanner]:
        """
        Lists all scanners and scanner groups not yet assigned to a custom
        network object.

        Args:
            network_id: The UUID of the default network object.

        Returns:
            List of scanner objects assignable to a custom network.
        """
        resp = await self._get(
            f"/{scrub(network_id)}/assignable-scanners",
            response_model=NetworkScannerListResponse,
        )
        return resp.scanners

    async def assign_scanner(
        self, network_id: UUID | str, scanner_uuid: UUID | str
    ) -> None:
        """
        Assigns a single scanner or scanner group to a network object.

        Args:
            network_id: The UUID of the network object.
            scanner_uuid: The UUID of the scanner or scanner group to assign.
        """
        await self._post(f"/{scrub(network_id)}/scanners/{scrub(scanner_uuid)}")

    async def assign_scanners(
        self, network_id: UUID | str, scanner_uuids: list[UUID | str]
    ) -> None:
        """
        Bulk assigns scanners and scanner groups to a network object. This
        overwrites the full list of scanners and scanner groups previously
        assigned to the network object; any scanners or scanner groups
        omitted from ``scanner_uuids`` are returned to the default network.

        Args:
            network_id: The UUID of the network object.
            scanner_uuids: The UUIDs of the scanners and scanner groups to assign.
        """
        await self._post(
            f"/{scrub(network_id)}/scanners",
            json=NetworkScannerBulkAssign.model_validate(
                {"scanner_uuids": scanner_uuids}
            ),
        )
