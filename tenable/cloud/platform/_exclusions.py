from typing import IO
from uuid import UUID

from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.utils import scrub

from .iterators import AsyncPaginationV1Iterator, PaginationV1Iterator
from .models.exclusions import (
    Exclusion,
    ExclusionCreate,
    ExclusionListResponse,
    ExclusionQueryParams,
    ExclusionSchedule,
)


class ExclusionsIterator(PaginationV1Iterator):
    path: str
    page: list[Exclusion]
    params: ExclusionQueryParams
    _method = "platform.exclusions._list_exclusions"


class AsyncExclusionsIterator(AsyncPaginationV1Iterator):
    path: str
    page: list[Exclusion]
    params: ExclusionQueryParams
    _method = "platform.exclusions._list_exclusions"


class ExclusionsAPI(APIEndpoint):
    _path = "/exclusions"

    def _list_exclusions(
        self, *, path: str, params: ExclusionQueryParams
    ) -> ExclusionListResponse:
        return self._client._get(
            path, params=params, response_model=ExclusionListResponse
        )

    def get(self, *, limit: int = 200, sort: str | None = None) -> ExclusionsIterator:
        """
        Returns an iterator of scan target exclusions.

        Args:
            limit: Number of records to retrieve per page. Defaults to ``200``.
                Maximum is ``500``.
            sort:
                Sort expression, e.g. ``"name:asc"`` or
                ``"last_modification_date:desc"``.

        Returns:
            Iterator yielding exclusion objects.
        """
        params = ExclusionQueryParams.model_validate({"limit": limit, "sort": sort})
        return ExclusionsIterator(self._client, path=self._path, params=params)

    def details(self, exclusion_id: int | UUID | str) -> Exclusion:
        """
        Returns the details for the specified scan target exclusion.

        Args:
            exclusion_id: The unique ID or UUID of the exclusion.

        Returns:
            Requested exclusion object.
        """
        return self._get(f"/{scrub(exclusion_id)}", response_model=Exclusion)

    def create(
        self,
        name: str,
        members: list[str],
        *,
        description: str | None = None,
        schedule: ExclusionSchedule | None = None,
        network_id: UUID | str | None = None,
    ) -> Exclusion:
        """
        Creates a new scan target exclusion.

        Args:
            name: The name of the new exclusion.
            members:
                The targets to exclude from scans. Each member should be an
                IPv4 address, IPv4 range, CIDR, or FQDN.
            description: Description of the new exclusion.
            schedule: Schedule object of the new exclusion.
            network_id:
                The UUID of the network object associated with scanners where
                the exclusion should apply. Defaults to the default network.

        Returns:
            Created exclusion object.
        """
        return self._post(
            response_model=Exclusion,
            json=ExclusionCreate(
                name=name,
                members=members,
                description=description,
                schedule=schedule,
                network_id=UUID(str(network_id)) if network_id is not None else None,
            ),
        )

    def update(
        self,
        exclusion_id: int | UUID | str,
        *,
        name: str | None = None,
        members: list[str] | None = None,
        description: str | None = None,
        schedule: ExclusionSchedule | None = None,
        network_id: UUID | str | None = None,
    ) -> Exclusion:
        """
        Updates an existing scan target exclusion.

        Args:
            exclusion_id: The unique ID or UUID of the exclusion to edit.
            name: New name of the exclusion.
            members: New list of targets to exclude from scans.
            description: New description for the exclusion.
            schedule: Updated schedule object for the exclusion.
            network_id: New network UUID to associate with the exclusion.

        Returns:
            Updated exclusion object.
        """
        excl = self.details(exclusion_id)
        updated = ExclusionCreate(
            name=name if name is not None else excl.name,
            members=members if members is not None else excl.members,
            description=description if description is not None else excl.description,
            schedule=schedule if schedule is not None else excl.schedule,
            network_id=(
                UUID(str(network_id)) if network_id is not None else excl.network_id
            ),
        )
        return self._put(
            f"/{scrub(exclusion_id)}", json=updated, response_model=Exclusion
        )

    def delete(self, exclusion_id: int | UUID | str) -> None:
        """
        Deletes the specified scan target exclusion.

        Args:
            exclusion_id: The unique ID or UUID of the exclusion to delete.
        """
        self._delete(f"/{scrub(exclusion_id)}")

    def import_exclusions(self, fobj: IO[bytes]) -> list[Exclusion]:
        """
        Imports scan target exclusions from an exclusion import file.

        Args:
            fobj: The file object of the exclusion(s) to import.

        Returns:
            List of the imported exclusion objects.
        """
        return self._post(
            "/import", files={"file": fobj}, response_model=list[Exclusion]
        )


class AsyncExclusionsAPI(AsyncAPIEndpoint):
    _path = "/exclusions"

    async def _list_exclusions(
        self, *, path: str, params: ExclusionQueryParams
    ) -> ExclusionListResponse:
        return await self._client._get(
            path, params=params, response_model=ExclusionListResponse
        )

    async def get(
        self, *, limit: int = 200, sort: str | None = None
    ) -> AsyncExclusionsIterator:
        """
        Returns an async iterator of scan target exclusions.

        Args:
            limit: Number of records to retrieve per page. Defaults to ``200``.
                Maximum is ``500``.
            sort:
                Sort expression, e.g. ``"name:asc"`` or
                ``"last_modification_date:desc"``.

        Returns:
            Async iterator yielding exclusion objects.
        """
        params = ExclusionQueryParams.model_validate({"limit": limit, "sort": sort})
        return AsyncExclusionsIterator(self._client, path=self._path, params=params)

    async def details(self, exclusion_id: int | UUID | str) -> Exclusion:
        """
        Returns the details for the specified scan target exclusion.

        Args:
            exclusion_id: The unique ID or UUID of the exclusion.

        Returns:
            Requested exclusion object.
        """
        return await self._get(f"/{scrub(exclusion_id)}", response_model=Exclusion)

    async def create(
        self,
        name: str,
        members: list[str],
        *,
        description: str | None = None,
        schedule: ExclusionSchedule | None = None,
        network_id: UUID | str | None = None,
    ) -> Exclusion:
        """
        Creates a new scan target exclusion.

        Args:
            name: The name of the new exclusion.
            members:
                The targets to exclude from scans. Each member should be an
                IPv4 address, IPv4 range, CIDR, or FQDN.
            description: Description of the new exclusion.
            schedule: Schedule object of the new exclusion.
            network_id:
                The UUID of the network object associated with scanners where
                the exclusion should apply. Defaults to the default network.

        Returns:
            Created exclusion object.
        """
        return await self._post(
            response_model=Exclusion,
            json=ExclusionCreate(
                name=name,
                members=members,
                description=description,
                schedule=schedule,
                network_id=UUID(str(network_id)) if network_id is not None else None,
            ),
        )

    async def update(
        self,
        exclusion_id: int | UUID | str,
        *,
        name: str | None = None,
        members: list[str] | None = None,
        description: str | None = None,
        schedule: ExclusionSchedule | None = None,
        network_id: UUID | str | None = None,
    ) -> Exclusion:
        """
        Updates an existing scan target exclusion.

        Args:
            exclusion_id: The unique ID or UUID of the exclusion to edit.
            name: New name of the exclusion.
            members: New list of targets to exclude from scans.
            description: New description for the exclusion.
            schedule: Updated schedule object for the exclusion.
            network_id: New network UUID to associate with the exclusion.

        Returns:
            Updated exclusion object.
        """
        excl = await self.details(exclusion_id)
        updated = ExclusionCreate(
            name=name if name is not None else excl.name,
            members=members if members is not None else excl.members,
            description=description if description is not None else excl.description,
            schedule=schedule if schedule is not None else excl.schedule,
            network_id=(
                UUID(str(network_id)) if network_id is not None else excl.network_id
            ),
        )
        return await self._put(
            f"/{scrub(exclusion_id)}", json=updated, response_model=Exclusion
        )

    async def delete(self, exclusion_id: int | UUID | str) -> None:
        """
        Deletes the specified scan target exclusion.

        Args:
            exclusion_id: The unique ID or UUID of the exclusion to delete.
        """
        await self._delete(f"/{scrub(exclusion_id)}")

    async def import_exclusions(self, fobj: IO[bytes]) -> list[Exclusion]:
        """
        Imports scan target exclusions from an exclusion import file.

        Args:
            fobj: The file object of the exclusion(s) to import.

        Returns:
            List of the imported exclusion objects.
        """
        return await self._post(
            "/import", files={"file": fobj}, response_model=list[Exclusion]
        )
