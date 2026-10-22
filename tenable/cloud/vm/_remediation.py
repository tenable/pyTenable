from copy import copy
from datetime import date, datetime
from typing import Any, Awaitable, Callable, Generic, Literal, TypeVar
from uuid import UUID

from restfly import APIEndpoint, APIIterator, AsyncAPIEndpoint, AsyncAPIIterator

from tenable.utils import scrub

from .models.remediation import (
    RemediationDetailsParams,
    RemediationDueDate,
    RemediationGoal,
    RemediationGoalDeleteRequest,
    RemediationGoalDetailsResponse,
    RemediationGoalRequest,
    RemediationProject,
    RemediationProjectDeleteRequest,
    RemediationProjectDetailsResponse,
    RemediationProjectRequest,
    RemediationSearchRequest,
    RemediationSearchResponse,
    RemediationSort,
)

T = TypeVar("T")

RemediationSortType = RemediationSort | tuple[str, str] | str
RemediationDueDateType = RemediationDueDate | dict[str, Any] | int | date


class RemediationIterator(APIIterator, Generic[T]):
    next: str | None = None
    """The next page token"""

    page: list[T]
    query: RemediationSearchRequest
    search: Callable[[RemediationSearchRequest], RemediationSearchResponse[T]]

    def _get_page(self) -> None:
        # The API only returns a pagination token when more results are available.
        if self.num_pages and not self.next:
            self.page = []
            return
        query = copy(self.query)
        query.next = self.next
        resp = self.search(query)
        self.total = resp.pagination.total
        self.next = resp.pagination.next
        self.page = resp.items


class AsyncRemediationIterator(AsyncAPIIterator, Generic[T]):
    next: str | None = None
    """The next page token"""

    page: list[T]
    query: RemediationSearchRequest
    search: Callable[
        [RemediationSearchRequest], Awaitable[RemediationSearchResponse[T]]
    ]

    async def _get_page(self) -> None:
        # The API only returns a pagination token when more results are available.
        if self.num_pages and not self.next:
            self.page = []
            return
        query = copy(self.query)
        query.next = self.next
        resp = await self.search(query)
        self.total = resp.pagination.total
        self.next = resp.pagination.next
        self.page = resp.items


class RemediationAPI(APIEndpoint):
    _path = "/remediation"

    def _search_projects(
        self, query: RemediationSearchRequest
    ) -> RemediationSearchResponse[RemediationProject]:
        resp: RemediationSearchResponse[RemediationProject] = self._post(
            "/search",
            json=query,
            response_model=RemediationSearchResponse[RemediationProject],
        )
        return resp

    def _search_goals(
        self, query: RemediationSearchRequest
    ) -> RemediationSearchResponse[RemediationGoal]:
        resp: RemediationSearchResponse[RemediationGoal] = self._post(
            "/goal/search",
            json=query,
            response_model=RemediationSearchResponse[RemediationGoal],
        )
        return resp

    def projects(
        self,
        *,
        filters: dict[str, Any] | None = None,
        sort: list[RemediationSortType] | None = None,
        fields: list[str] | str | None = None,
        findings_type: str | None = None,
        limit: int = 100,
    ) -> RemediationIterator[RemediationProject]:
        """
        Searches for the remediation projects matching the specified criteria.

        Args:
            filters: The filter object to match the remediation projects against.
            sort:
                The properties to sort the results by, as `property:order` strings,
                `(property, order)` tuples, or `RemediationSort` objects.
            fields: The properties to include for each project.
            findings_type: The type of findings to evaluate.
            limit: The number of projects to return per page.

        Returns:
            Iterator supporting pagination of the remediation projects.

        Example:
            >>> for project in cloud.vm.remediation.projects(sort=["name:asc"]):
            ...     print(project.id, project.name)
        """
        query = RemediationSearchRequest.model_validate(
            {
                "filter": filters,
                "sort": sort,
                "fields": fields,
                "findings_type": findings_type,
                "limit": limit,
            }
        )
        return RemediationIterator[RemediationProject](
            self._client, search=self._search_projects, query=query
        )

    def project_detail(
        self, project_id: UUID | str, *, findings_type: str | None = None
    ) -> RemediationProject:
        """
        Returns the details for the specified remediation project.

        Args:
            project_id: The UUID of the remediation project.
            findings_type: The type of findings to evaluate.

        Returns:
            Requested remediation project object.

        Example:
            >>> cloud.vm.remediation.project_detail("7c41e8a9-3b62-4d05-9f18-2ae6b407d3c1")
        """
        resp = self._get(
            f"/{scrub(project_id)}",
            params=RemediationDetailsParams(findings_type=findings_type),
            response_model=RemediationProjectDetailsResponse,
        )
        return resp.root[0]

    def project_create(
        self,
        name: str,
        *,
        description: str | None = None,
        type: str | None = None,
        status: str | None = None,
        start_date: datetime | int | None = None,
        asset_filters: dict[str, Any] | str | None = None,
        finding_filters: dict[str, Any] | str | None = None,
        due_date: RemediationDueDateType | None = None,
        assignees: list[str] | None = None,
    ) -> None:
        """
        Creates a remediation project.  The response doesn't include the new
        project, so use :meth:`projects` to retrieve it.

        Args:
            name: The name of the remediation project.
            description: The description of the remediation project.
            type: The type of the remediation project, such as `Static`.
            status: The status of the remediation project, such as `ACTIVE`.
            start_date: When the remediation project starts.
            asset_filters: The asset filters to apply. Use `all` for every asset.
            finding_filters: The finding filters to apply.
            due_date:
                When the remediation project is due.  An integer is the number of
                days to complete within and a date or datetime is a fixed date.
            assignees: The users or user groups to assign to the project.

        Example:
            >>> cloud.vm.remediation.project_create(
            ...     "Critical patching",
            ...     asset_filters="all",
            ...     finding_filters={
            ...         "and": [
            ...             {"id": "severity", "operator": "eq", "value": "critical"}
            ...         ]
            ...     },
            ...     due_date=30,
            ...     assignees=["user@example.com"],
            ... )
        """
        self._post(
            "",
            json=RemediationProjectRequest.model_validate(
                {
                    "name": name,
                    "description": description,
                    "type": type,
                    "status": status,
                    "start_date": start_date,
                    "asset_filters": asset_filters,
                    "finding_filters": finding_filters,
                    "due_date": due_date,
                    "assignees": assignees,
                }
            ),
        )

    def project_update(
        self,
        project_id: UUID | str,
        name: str,
        *,
        description: str | None = None,
        type: str | None = None,
        status: str | None = None,
        start_date: datetime | int | None = None,
        asset_filters: dict[str, Any] | str | None = None,
        finding_filters: dict[str, Any] | str | None = None,
        due_date: RemediationDueDateType | None = None,
        assignees: list[str] | None = None,
    ) -> None:
        """
        Updates the specified remediation project.

        Args:
            project_id: The UUID of the remediation project.
            name: The name of the remediation project.
            description: The description of the remediation project.
            type: The type of the remediation project, such as `Static`.
            status: The status of the remediation project, such as `ACTIVE`.
            start_date: When the remediation project starts.
            asset_filters: The asset filters to apply. Use `all` for every asset.
            finding_filters: The finding filters to apply.
            due_date:
                When the remediation project is due.  An integer is the number of
                days to complete within and a date or datetime is a fixed date.
            assignees: The users or user groups to assign to the project.

        Example:
            >>> cloud.vm.remediation.project_update(
            ...     "7c41e8a9-3b62-4d05-9f18-2ae6b407d3c1",
            ...     "Critical patching",
            ...     status="SUSPENDED",
            ... )
        """
        self._put(
            f"/{scrub(project_id)}",
            json=RemediationProjectRequest.model_validate(
                {
                    "name": name,
                    "description": description,
                    "type": type,
                    "status": status,
                    "start_date": start_date,
                    "asset_filters": asset_filters,
                    "finding_filters": finding_filters,
                    "due_date": due_date,
                    "assignees": assignees,
                }
            ),
        )

    def project_delete(self, *project_ids: UUID | str) -> None:
        """
        Deletes the specified remediation projects.  The API responds the same way
        whether or not the projects exist.

        Args:
            *project_ids: The UUIDs of the remediation projects to delete.

        Example:
            >>> cloud.vm.remediation.project_delete("7c41e8a9-3b62-4d05-9f18-2ae6b407d3c1")
        """
        self._patch(
            json=RemediationProjectDeleteRequest.model_validate(
                {"project_ids": list(project_ids)}
            )
        )

    def goals(
        self,
        *,
        filters: dict[str, Any] | None = None,
        sort: list[RemediationSortType] | None = None,
        fields: list[str] | str | None = None,
        findings_type: str | None = None,
        limit: int = 100,
    ) -> RemediationIterator[RemediationGoal]:
        """
        Searches for the remediation goals matching the specified criteria.

        Args:
            filters: The filter object to match the remediation goals against.
            sort:
                The properties to sort the results by, as `property:order` strings,
                `(property, order)` tuples, or `RemediationSort` objects.
            fields: The properties to include for each goal.
            findings_type: The type of findings to evaluate.
            limit: The number of goals to return per page.

        Returns:
            Iterator supporting pagination of the remediation goals.

        Example:
            >>> for goal in cloud.vm.remediation.goals(sort=["name:asc"]):
            ...     print(goal.id, goal.name)
        """
        query = RemediationSearchRequest.model_validate(
            {
                "filter": filters,
                "sort": sort,
                "fields": fields,
                "findings_type": findings_type,
                "limit": limit,
            }
        )
        return RemediationIterator[RemediationGoal](
            self._client, search=self._search_goals, query=query
        )

    def goal_detail(
        self, goal_id: UUID | str, *, findings_type: str | None = None
    ) -> RemediationGoal:
        """
        Returns the details for the specified remediation goal.

        Args:
            goal_id: The UUID of the remediation goal.
            findings_type: The type of findings to evaluate.

        Returns:
            Requested remediation goal object.

        Example:
            >>> cloud.vm.remediation.goal_detail("e2a95c73-8d14-4f60-b3a7-16c8d5029e4b")
        """
        resp = self._get(
            f"/goal/{scrub(goal_id)}",
            params=RemediationDetailsParams(findings_type=findings_type),
            response_model=RemediationGoalDetailsResponse,
        )
        return resp.root[0]

    def goal_create(
        self,
        name: str,
        *,
        description: str | None = None,
        type: str | None = None,
        status: str | None = None,
        start_date: datetime | int | None = None,
        asset_filters: dict[str, Any] | str | None = None,
        finding_filters: dict[str, Any] | str | None = None,
        due_date: RemediationDueDateType | Literal["ongoing"] | None = None,
        minimum_percentage: int | None = None,
        conditions: list[Any] | str | None = None,
    ) -> None:
        """
        Creates a remediation goal.  The response doesn't include the new goal, so
        use :meth:`goals` to retrieve it.

        Args:
            name: The name of the remediation goal.
            description: The description of the remediation goal.
            type: The type of the remediation goal, such as `Static`.
            status: The status of the remediation goal, such as `ACTIVE`.
            start_date: When the remediation goal starts.
            asset_filters: The asset filters to apply. Use `all` for every asset.
            finding_filters: The finding filters that determine if the goal is met.
            due_date:
                When the remediation goal is due.  An integer is the number of days
                to meet the goal within, a date or datetime is a fixed date, and
                `ongoing` leaves the goal always in progress.
            minimum_percentage:
                The minimum percentage of findings to remediate for the goal to be
                met.
            conditions: The conditions that the remediation goal evaluates.

        Example:
            >>> cloud.vm.remediation.goal_create(
            ...     "Reduce critical findings",
            ...     asset_filters="all",
            ...     due_date=datetime(2026, 3, 27, tzinfo=timezone.utc),
            ...     minimum_percentage=80,
            ... )
        """
        self._post(
            "/goal",
            json=RemediationGoalRequest.model_validate(
                {
                    "name": name,
                    "description": description,
                    "type": type,
                    "status": status,
                    "start_date": start_date,
                    "asset_filters": asset_filters,
                    "finding_filters": finding_filters,
                    "due_date": due_date,
                    "minimum_percentage": minimum_percentage,
                    "conditions": conditions,
                }
            ),
        )

    def goal_update(
        self,
        goal_id: UUID | str,
        name: str,
        *,
        description: str | None = None,
        type: str | None = None,
        status: str | None = None,
        start_date: datetime | int | None = None,
        asset_filters: dict[str, Any] | str | None = None,
        finding_filters: dict[str, Any] | str | None = None,
        due_date: RemediationDueDateType | Literal["ongoing"] | None = None,
        minimum_percentage: int | None = None,
        conditions: list[Any] | str | None = None,
    ) -> None:
        """
        Updates the specified remediation goal.

        Args:
            goal_id: The UUID of the remediation goal.
            name: The name of the remediation goal.
            description: The description of the remediation goal.
            type: The type of the remediation goal, such as `Static`.
            status: The status of the remediation goal, such as `ACTIVE`.
            start_date: When the remediation goal starts.
            asset_filters: The asset filters to apply. Use `all` for every asset.
            finding_filters: The finding filters that determine if the goal is met.
            due_date:
                When the remediation goal is due.  An integer is the number of days
                to meet the goal within, a date or datetime is a fixed date, and
                `ongoing` leaves the goal always in progress.
            minimum_percentage:
                The minimum percentage of findings to remediate for the goal to be
                met.
            conditions: The conditions that the remediation goal evaluates.

        Example:
            >>> cloud.vm.remediation.goal_update(
            ...     "e2a95c73-8d14-4f60-b3a7-16c8d5029e4b",
            ...     "Reduce critical findings",
            ...     status="CLOSED",
            ... )
        """
        self._put(
            f"/goal/{scrub(goal_id)}",
            json=RemediationGoalRequest.model_validate(
                {
                    "name": name,
                    "description": description,
                    "type": type,
                    "status": status,
                    "start_date": start_date,
                    "asset_filters": asset_filters,
                    "finding_filters": finding_filters,
                    "due_date": due_date,
                    "minimum_percentage": minimum_percentage,
                    "conditions": conditions,
                }
            ),
        )

    def goal_delete(self, *goal_ids: UUID | str) -> None:
        """
        Deletes the specified remediation goals.  The API responds the same way
        whether or not the goals exist.

        Args:
            *goal_ids: The UUIDs of the remediation goals to delete.

        Example:
            >>> cloud.vm.remediation.goal_delete("e2a95c73-8d14-4f60-b3a7-16c8d5029e4b")
        """
        self._patch(
            "/goal",
            json=RemediationGoalDeleteRequest.model_validate(
                {"goal_ids": list(goal_ids)}
            ),
        )


class AsyncRemediationAPI(AsyncAPIEndpoint):
    _path = "/remediation"

    async def _search_projects(
        self, query: RemediationSearchRequest
    ) -> RemediationSearchResponse[RemediationProject]:
        resp: RemediationSearchResponse[RemediationProject] = await self._post(
            "/search",
            json=query,
            response_model=RemediationSearchResponse[RemediationProject],
        )
        return resp

    async def _search_goals(
        self, query: RemediationSearchRequest
    ) -> RemediationSearchResponse[RemediationGoal]:
        resp: RemediationSearchResponse[RemediationGoal] = await self._post(
            "/goal/search",
            json=query,
            response_model=RemediationSearchResponse[RemediationGoal],
        )
        return resp

    async def projects(
        self,
        *,
        filters: dict[str, Any] | None = None,
        sort: list[RemediationSortType] | None = None,
        fields: list[str] | str | None = None,
        findings_type: str | None = None,
        limit: int = 100,
    ) -> AsyncRemediationIterator[RemediationProject]:
        """
        Searches for the remediation projects matching the specified criteria.

        Args:
            filters: The filter object to match the remediation projects against.
            sort:
                The properties to sort the results by, as `property:order` strings,
                `(property, order)` tuples, or `RemediationSort` objects.
            fields: The properties to include for each project.
            findings_type: The type of findings to evaluate.
            limit: The number of projects to return per page.

        Returns:
            Iterator supporting pagination of the remediation projects.

        Example:
            >>> async for project in await cloud.vm.remediation.projects(sort=["name:asc"]):
            ...     print(project.id, project.name)
        """
        query = RemediationSearchRequest.model_validate(
            {
                "filter": filters,
                "sort": sort,
                "fields": fields,
                "findings_type": findings_type,
                "limit": limit,
            }
        )
        return AsyncRemediationIterator[RemediationProject](
            self._client, search=self._search_projects, query=query
        )

    async def project_detail(
        self, project_id: UUID | str, *, findings_type: str | None = None
    ) -> RemediationProject:
        """
        Returns the details for the specified remediation project.

        Args:
            project_id: The UUID of the remediation project.
            findings_type: The type of findings to evaluate.

        Returns:
            Requested remediation project object.

        Example:
            >>> await cloud.vm.remediation.project_detail("7c41e8a9-3b62-4d05-9f18-2ae6b407d3c1")
        """
        resp = await self._get(
            f"/{scrub(project_id)}",
            params=RemediationDetailsParams(findings_type=findings_type),
            response_model=RemediationProjectDetailsResponse,
        )
        return resp.root[0]

    async def project_create(
        self,
        name: str,
        *,
        description: str | None = None,
        type: str | None = None,
        status: str | None = None,
        start_date: datetime | int | None = None,
        asset_filters: dict[str, Any] | str | None = None,
        finding_filters: dict[str, Any] | str | None = None,
        due_date: RemediationDueDateType | None = None,
        assignees: list[str] | None = None,
    ) -> None:
        """
        Creates a remediation project.  The response doesn't include the new
        project, so use :meth:`projects` to retrieve it.

        Args:
            name: The name of the remediation project.
            description: The description of the remediation project.
            type: The type of the remediation project, such as `Static`.
            status: The status of the remediation project, such as `ACTIVE`.
            start_date: When the remediation project starts.
            asset_filters: The asset filters to apply. Use `all` for every asset.
            finding_filters: The finding filters to apply.
            due_date:
                When the remediation project is due.  An integer is the number of
                days to complete within and a date or datetime is a fixed date.
            assignees: The users or user groups to assign to the project.

        Example:
            >>> await cloud.vm.remediation.project_create(
            ...     "Critical patching",
            ...     asset_filters="all",
            ...     finding_filters={
            ...         "and": [
            ...             {"id": "severity", "operator": "eq", "value": "critical"}
            ...         ]
            ...     },
            ...     due_date=30,
            ...     assignees=["user@example.com"],
            ... )
        """
        await self._post(
            "",
            json=RemediationProjectRequest.model_validate(
                {
                    "name": name,
                    "description": description,
                    "type": type,
                    "status": status,
                    "start_date": start_date,
                    "asset_filters": asset_filters,
                    "finding_filters": finding_filters,
                    "due_date": due_date,
                    "assignees": assignees,
                }
            ),
        )

    async def project_update(
        self,
        project_id: UUID | str,
        name: str,
        *,
        description: str | None = None,
        type: str | None = None,
        status: str | None = None,
        start_date: datetime | int | None = None,
        asset_filters: dict[str, Any] | str | None = None,
        finding_filters: dict[str, Any] | str | None = None,
        due_date: RemediationDueDateType | None = None,
        assignees: list[str] | None = None,
    ) -> None:
        """
        Updates the specified remediation project.

        Args:
            project_id: The UUID of the remediation project.
            name: The name of the remediation project.
            description: The description of the remediation project.
            type: The type of the remediation project, such as `Static`.
            status: The status of the remediation project, such as `ACTIVE`.
            start_date: When the remediation project starts.
            asset_filters: The asset filters to apply. Use `all` for every asset.
            finding_filters: The finding filters to apply.
            due_date:
                When the remediation project is due.  An integer is the number of
                days to complete within and a date or datetime is a fixed date.
            assignees: The users or user groups to assign to the project.

        Example:
            >>> await cloud.vm.remediation.project_update(
            ...     "7c41e8a9-3b62-4d05-9f18-2ae6b407d3c1",
            ...     "Critical patching",
            ...     status="SUSPENDED",
            ... )
        """
        await self._put(
            f"/{scrub(project_id)}",
            json=RemediationProjectRequest.model_validate(
                {
                    "name": name,
                    "description": description,
                    "type": type,
                    "status": status,
                    "start_date": start_date,
                    "asset_filters": asset_filters,
                    "finding_filters": finding_filters,
                    "due_date": due_date,
                    "assignees": assignees,
                }
            ),
        )

    async def project_delete(self, *project_ids: UUID | str) -> None:
        """
        Deletes the specified remediation projects.  The API responds the same way
        whether or not the projects exist.

        Args:
            *project_ids: The UUIDs of the remediation projects to delete.

        Example:
            >>> await cloud.vm.remediation.project_delete("7c41e8a9-3b62-4d05-9f18-2ae6b407d3c1")
        """
        await self._patch(
            json=RemediationProjectDeleteRequest.model_validate(
                {"project_ids": list(project_ids)}
            )
        )

    async def goals(
        self,
        *,
        filters: dict[str, Any] | None = None,
        sort: list[RemediationSortType] | None = None,
        fields: list[str] | str | None = None,
        findings_type: str | None = None,
        limit: int = 100,
    ) -> AsyncRemediationIterator[RemediationGoal]:
        """
        Searches for the remediation goals matching the specified criteria.

        Args:
            filters: The filter object to match the remediation goals against.
            sort:
                The properties to sort the results by, as `property:order` strings,
                `(property, order)` tuples, or `RemediationSort` objects.
            fields: The properties to include for each goal.
            findings_type: The type of findings to evaluate.
            limit: The number of goals to return per page.

        Returns:
            Iterator supporting pagination of the remediation goals.

        Example:
            >>> async for goal in await cloud.vm.remediation.goals(sort=["name:asc"]):
            ...     print(goal.id, goal.name)
        """
        query = RemediationSearchRequest.model_validate(
            {
                "filter": filters,
                "sort": sort,
                "fields": fields,
                "findings_type": findings_type,
                "limit": limit,
            }
        )
        return AsyncRemediationIterator[RemediationGoal](
            self._client, search=self._search_goals, query=query
        )

    async def goal_detail(
        self, goal_id: UUID | str, *, findings_type: str | None = None
    ) -> RemediationGoal:
        """
        Returns the details for the specified remediation goal.

        Args:
            goal_id: The UUID of the remediation goal.
            findings_type: The type of findings to evaluate.

        Returns:
            Requested remediation goal object.

        Example:
            >>> await cloud.vm.remediation.goal_detail("e2a95c73-8d14-4f60-b3a7-16c8d5029e4b")
        """
        resp = await self._get(
            f"/goal/{scrub(goal_id)}",
            params=RemediationDetailsParams(findings_type=findings_type),
            response_model=RemediationGoalDetailsResponse,
        )
        return resp.root[0]

    async def goal_create(
        self,
        name: str,
        *,
        description: str | None = None,
        type: str | None = None,
        status: str | None = None,
        start_date: datetime | int | None = None,
        asset_filters: dict[str, Any] | str | None = None,
        finding_filters: dict[str, Any] | str | None = None,
        due_date: RemediationDueDateType | Literal["ongoing"] | None = None,
        minimum_percentage: int | None = None,
        conditions: list[Any] | str | None = None,
    ) -> None:
        """
        Creates a remediation goal.  The response doesn't include the new goal, so
        use :meth:`goals` to retrieve it.

        Args:
            name: The name of the remediation goal.
            description: The description of the remediation goal.
            type: The type of the remediation goal, such as `Static`.
            status: The status of the remediation goal, such as `ACTIVE`.
            start_date: When the remediation goal starts.
            asset_filters: The asset filters to apply. Use `all` for every asset.
            finding_filters: The finding filters that determine if the goal is met.
            due_date:
                When the remediation goal is due.  An integer is the number of days
                to meet the goal within, a date or datetime is a fixed date, and
                `ongoing` leaves the goal always in progress.
            minimum_percentage:
                The minimum percentage of findings to remediate for the goal to be
                met.
            conditions: The conditions that the remediation goal evaluates.

        Example:
            >>> await cloud.vm.remediation.goal_create(
            ...     "Reduce critical findings",
            ...     asset_filters="all",
            ...     due_date=datetime(2026, 3, 27, tzinfo=timezone.utc),
            ...     minimum_percentage=80,
            ... )
        """
        await self._post(
            "/goal",
            json=RemediationGoalRequest.model_validate(
                {
                    "name": name,
                    "description": description,
                    "type": type,
                    "status": status,
                    "start_date": start_date,
                    "asset_filters": asset_filters,
                    "finding_filters": finding_filters,
                    "due_date": due_date,
                    "minimum_percentage": minimum_percentage,
                    "conditions": conditions,
                }
            ),
        )

    async def goal_update(
        self,
        goal_id: UUID | str,
        name: str,
        *,
        description: str | None = None,
        type: str | None = None,
        status: str | None = None,
        start_date: datetime | int | None = None,
        asset_filters: dict[str, Any] | str | None = None,
        finding_filters: dict[str, Any] | str | None = None,
        due_date: RemediationDueDateType | Literal["ongoing"] | None = None,
        minimum_percentage: int | None = None,
        conditions: list[Any] | str | None = None,
    ) -> None:
        """
        Updates the specified remediation goal.

        Args:
            goal_id: The UUID of the remediation goal.
            name: The name of the remediation goal.
            description: The description of the remediation goal.
            type: The type of the remediation goal, such as `Static`.
            status: The status of the remediation goal, such as `ACTIVE`.
            start_date: When the remediation goal starts.
            asset_filters: The asset filters to apply. Use `all` for every asset.
            finding_filters: The finding filters that determine if the goal is met.
            due_date:
                When the remediation goal is due.  An integer is the number of days
                to meet the goal within, a date or datetime is a fixed date, and
                `ongoing` leaves the goal always in progress.
            minimum_percentage:
                The minimum percentage of findings to remediate for the goal to be
                met.
            conditions: The conditions that the remediation goal evaluates.

        Example:
            >>> await cloud.vm.remediation.goal_update(
            ...     "e2a95c73-8d14-4f60-b3a7-16c8d5029e4b",
            ...     "Reduce critical findings",
            ...     status="CLOSED",
            ... )
        """
        await self._put(
            f"/goal/{scrub(goal_id)}",
            json=RemediationGoalRequest.model_validate(
                {
                    "name": name,
                    "description": description,
                    "type": type,
                    "status": status,
                    "start_date": start_date,
                    "asset_filters": asset_filters,
                    "finding_filters": finding_filters,
                    "due_date": due_date,
                    "minimum_percentage": minimum_percentage,
                    "conditions": conditions,
                }
            ),
        )

    async def goal_delete(self, *goal_ids: UUID | str) -> None:
        """
        Deletes the specified remediation goals.  The API responds the same way
        whether or not the goals exist.

        Args:
            *goal_ids: The UUIDs of the remediation goals to delete.

        Example:
            >>> await cloud.vm.remediation.goal_delete("e2a95c73-8d14-4f60-b3a7-16c8d5029e4b")
        """
        await self._patch(
            "/goal",
            json=RemediationGoalDeleteRequest.model_validate(
                {"goal_ids": list(goal_ids)}
            ),
        )
