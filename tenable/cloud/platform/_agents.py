from typing import Literal
from uuid import UUID

from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.cloud._common import AsyncPaginationV1Iterator, PaginationV1Iterator
from tenable.utils import scrub

from .models.agents import (
    Agent,
    AgentConfig,
    AgentDetail,
    AgentExclusion,
    AgentExclusionCreate,
    AgentExclusionListResponse,
    AgentFilter,
    AgentGroup,
    AgentGroupListResponse,
    AgentListResponse,
    AgentQueryParams,
    AgentSchedule,
    AgentTask,
    AgentGroupTask,
    BulkAgentCriteria,
)


class AgentsIterator(PaginationV1Iterator):
    path: str
    page: list[Agent]
    params: AgentQueryParams
    _method = "platform.agents._list_agents"


class AsyncAgentsIterator(AsyncPaginationV1Iterator):
    path: str
    page: list[Agent]
    params: AgentQueryParams
    _method = "platform.agents._list_agents"


class AgentExclusionAPI(APIEndpoint):
    _path = "/scanners/null/agents/exclusions"

    def create(
        self,
        name: str,
        description: str | None = None,
        schedule: AgentSchedule | None = None,
    ) -> AgentExclusion:
        """
        Creates a new Agent exclusion

        Args:
            name: The name of the new exclusion.
            description: Description of the new exclusion.
            schedule: Schedule object of the new exclusion.

        Returns:
            Created exclusion object.
        """
        return self._post(
            response_model=AgentExclusion,
            json=AgentExclusionCreate(
                name=name, description=description, schedule=schedule
            ),
        )

    def update(
        self,
        id: int | UUID,
        *,
        name: str | None = None,
        description: str | None = None,
        schedule: AgentSchedule | None = None,
    ) -> AgentExclusion:
        """
        Updates an existing Agent exclusion object

        Args:
            id: Unique ID of the exclusion object to edit.
            name: New name of the exclusion.
            description: New description for the exclusion.
            schedule: Updated schedule object for the exclusion.

        Returns:
            Updated exclusion object.
        """
        excl = self.details(id)
        updated = AgentExclusionCreate(
            name=name if name is not None else excl.name,
            description=description if description is not None else excl.description,
            schedule=schedule if schedule is not None else excl.schedule,
        )
        return self._put(f"/{scrub(id)}", json=updated, response_model=AgentExclusion)

    def delete(self, id: int | UUID) -> None:
        """
        Deletes the specified agent exclusion.

        Args:
            id: Unique ID of the exclusion object to delete.
        """
        self._delete(f"/{scrub(id)}")

    def get(self) -> list[AgentExclusion]:
        """
        Gets the list of agent exclusions.

        Returns:
            List of exclusion objects.
        """
        resp = self._get(response_model=AgentExclusionListResponse)
        return resp.exclusions

    def details(self, id: int | UUID) -> AgentExclusion:
        """
        Gets the details for thew specific agent exclusion.

        Args:
            id: Unique id of the exclusion object to retrieve.

        Returns:
            Requested exclusion object.
        """
        return self._get(f"/{scrub(id)}", response_model=AgentExclusion)


class AgentGroupsAPI(APIEndpoint):
    _path = "/scanners/null/agent-groups"

    def create(self, name: str) -> AgentGroup:
        """
        Creates a new Agent group

        Args:
            name: The name of the new group.

        Returns:
            Created agent group object.
        """
        return self._post(response_model=AgentExclusion, json={"name": name})

    def update(self, id: int | UUID, *, name: str) -> AgentGroup:
        """
        Updates an existing Agent exclusion object

        Args:
            id: Unique ID of the group object to edit.
            name: New name of the group.

        Returns:
            Updated agent group object.
        """
        return self._put(
            f"/{scrub(id)}", json={"name": name}, response_model=AgentGroup
        )

    def delete(self, id: int | UUID) -> None:
        """
        Deletes the specified agent group.

        Args:
            id: Unique ID of the agent group object to delete.
        """
        self._delete(f"/{scrub(id)}")

    def get(self) -> list[AgentExclusion]:
        """
        Gets the list of agent groups.

        Returns:
            List of agent group objects.
        """
        resp = self._get(response_model=AgentGroupListResponse)
        return resp.groups

    def details(self, id: int | UUID) -> AgentExclusion:
        """
        Gets the details for thew specific agent group.

        Args:
            id: Unique id of the agent group object to retrieve.

        Returns:
            Requested agent group object.
        """
        return self._get(f"/{scrub(id)}", response_model=AgentGroup)

    def add(self, group_id: int | UUID, agent_id: int | UUID) -> None:
        """
        Adds an agent to the agent group.

        Args:
            group_id: Agent Group ID
            agent_id: Agent ID
        """
        self._put(f"/{scrub(group_id)}/agents/{scrub(agent_id)}")

    def remove(self, group_id: int | UUID, agent_id: int | UUID) -> None:
        """
        Removes an agent from the agent group.

        Args:
            group_id: Agent Group ID
            agent_id: Agent ID
        """
        self._delete(f"/{scrub(group_id)}/agents/{scrub(agent_id)}")


class AgentTasksAPI(APIEndpoint):
    _path = "/scanners/null"

    def _task(self, model: BulkAgentQuery, response_model: AgentTask) -> AgentTask:
        ...

    def add_many(
        self,
        group_id: int | UUID,
        *,
        filters: list[str | AgentFilter],
        all_agents: bool = True,
        wildcard: str | None = None,
        filter_type: Literal["and", "or"] = "and",
        hardcoded_filters: list[str | AgentFilter] | None = None,
        included: list[int] | list[UUID] | None = None,
        excluded: list[int] | list[UUID] | None = None,
    ) -> AgentGroupTask:
        
        


class AgentsAPI(APIEndpoint):
    _path = "/scanners/null/agents"

    exclusions: AgentExclusionAPI
    groups: AgentGroupsAPI

    def _list_agents(self, *, path: str, params: AgentQueryParams) -> AgentListResponse:
        return self._client._get(path, params=params, response_model=AgentListResponse)

    def get(
        self,
        group_id: int | None = None,
        *,
        filters: list[tuple[str, str, str] | str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] | None = None,
        wildcard: str | None = None,
        wildcard_fields: list[str] | None = None,
        limit: int = 50,
        sort: str | None = None,
    ) -> AgentsIterator:
        """
        Returns an iterator of agents.

        Args:
            group_id:
                If provided, only agents belonging to this agent group are returned.
                You can find agent group IDs via the agent-groups API.
            filters:
                List of filters in ``field:operator:value`` format, or as
                ``(field, operator, value)`` tuples, or as
                :class:`AgentFilter` objects.
            filter_type:
                When multiple filters are supplied, combine them with ``and``
                (all must match) or ``or`` (any must match).
            wildcard:
                Free-text wildcard search applied across all wildcard-searchable
                fields.
            wildcard_fields:
                list of fields to apply the wildcard filter against.
            limit:
                Number of records to retrieve per page. Defaults to ``50``.
                Maximum is ``5000``.
            sort:
                Sort expression, e.g. ``"name:asc"`` or
                ``"name:desc,platform:asc"``.

        Returns:
            Iterator yielding :class:`~.models.AgentListItem` objects.
        """
        if group_id is not None:
            path = f"/scanners/null/agent-groups/{scrub(group_id)}/agents"
        else:
            path = "/scanners/null/agents"

        schema = self._client.platform.filters.agent()

        params = AgentQueryParams.model_validate(
            {
                "filters": filters,
                "filter_type": filter_type,
                "wildcard": wildcard,
                "wildcard_fields": wildcard_fields,
                "limit": limit,
                "sort": sort,
            },
            context=schema,
        )
        return AgentsIterator(self._client, path=path, params=params)

    def details(self, agent_id: int | UUID | str) -> AgentDetail:
        """
        Returns details for the specified agent.

        Args:
            agent_id: The unique ID of the agent.

        Returns:
            :class:`~.models.AgentDetails` for the specified agent.
        """
        return self._get(f"/{scrub(agent_id)}", response_model=AgentDetail)

    def rename(self, agent_id: int | UUID | str, name: str) -> AgentDetail:
        """
        Renames an agent.

        Args:
            agent_id: The ID or UUID of the agent to rename.
            name: The new name for the agent.

        Returns:
            Updated agent details.
        """
        return self._patch(
            f"/{scrub(agent_id)}", json={"name": name}, response_model=AgentDetail
        )

    def unlink(self, agent_id: int | UUID | str) -> None:
        """
        Unlinks (deletes) an agent.

        Args:
            agent_id: The unique ID of the agent to unlink.
        """
        self._delete(f"/{scrub(agent_id)}")

    def get_config(self) -> AgentConfig:
        """
        Returns the global configuration settings for agents.
        """
        return self._get("/config", response_model=AgentConfig)

    def update_config(
        self,
        auto_unlink: bool | None = None,
        auto_unlink_expiration: int | None = None,
        concurrent_update: bool | None = None,
        concurrent_update_max_agents: int | None = None,
        software_update: bool | None = None,
        hybrid_scanning: bool | None = None,
    ) -> AgentConfig:
        """
        Updates the global configuration settings for agents.

        Args:
            auto_unlink: Should agents auto-unlink?
            auto_unlink_expiration:
                Number of days of inactivity before auto-unlinking occurs.
            concurrent_update: Enable concurrent updates?
            concurrent_update_max_agents:
                Max agents that can be updates simultaneously.
            software_update: Enable software updating for agents?
            hybrid_scanning:
                Enable hybrid scanning for agents?

        Returns:
            Updated agent configuration.
        """
        config = self.get_config()

        if auto_unlink is not None:
            config.auto_unlink.enabled = auto_unlink
        if auto_unlink_expiration is not None:
            config.auto_unlink.expiration = auto_unlink_expiration
        if concurrent_update is not None:
            config.concurrent_update.enabled = concurrent_update
        if concurrent_update_max_agents is not None:
            config.concurrent_update.max_agents = concurrent_update_max_agents
        if software_update is not None:
            config.software_update = software_update
        if hybrid_scanning is not None:
            config.hybrid_scanning = hybrid_scanning
        return self._put("/config", json=config, response_model=AgentConfig)


class AsyncAgentsAPI(AsyncAPIEndpoint):
    _path = "/scanners/null/agents"

    async def _list_agents(
        self, *, path: str, params: AgentQueryParams
    ) -> AgentListResponse:
        return await self._client._get(
            path, params=params, response_model=AgentListResponse
        )

    async def get(
        self,
        group_id: int | None = None,
        *,
        filters: list[tuple[str, str, str] | str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] | None = None,
        wildcard: str | None = None,
        wildcard_fields: str | None = None,
        limit: int = 50,
        sort: str | None = None,
    ) -> AsyncAgentsIterator:
        """
        Returns an async iterator of agents.

        Args:
            group_id:
                If provided, only agents belonging to this agent group are returned.
            filters:
                List of filters in ``field:operator:value`` format, or as
                ``(field, operator, value)`` tuples, or as
                :class:`AgentFilter` objects.
            filter_type:
                When multiple filters are supplied, combine them with ``and``
                (all must match) or ``or`` (any must match).
            wildcard:
                Free-text wildcard search ap plied across all wildcard-searchable
                fields.
            wildcard_fields:
                list of fields to apply the wildcard filter against.
            limit:
                Number of records to retrieve per page. Defaults to ``50``.
                Maximum is ``5000``.
            sort:
                Sort expression, e.g. ``"name:asc"`` or
                ``"name:desc,platform:asc"``.

        Returns:
            Async iterator yielding :class:`~.models.AgentListItem` objects.
        """
        if group_id is not None:
            path = f"/scanners/null/agent-groups/{scrub(group_id)}/agents"
        else:
            path = "/scanners/null/agents"

        params = AgentQueryParams.model_validate(
            {
                "filters": filters,
                "filter_type": filter_type,
                "wildcard": wildcard,
                "wildcard_fields": wildcard_fields,
                "limit": limit,
                "sort": sort,
            }
        )
        return AsyncAgentsIterator(self._client, path=path, params=params)

    async def details(self, agent_id: int) -> AgentDetail:
        """
        Returns details for the specified agent.

        Args:
            agent_id: The unique ID of the agent.

        Returns:
            :class:`~.models.AgentDetails` for the specified agent.
        """
        return await self._get(f"/{scrub(agent_id)}", response_model=AgentDetail)

    async def rename(self, agent_id: int | UUID | str, name: str) -> AgentDetail:
        """
        Renames an agent.

        Args:
            agent_id: The ID or UUID of the agent to rename.
            name: The new name for the agent.

        Returns:
            Updated :class:`~.models.AgentDetails` for the agent.
        """
        return await self._patch(
            f"/{scrub(agent_id)}", json={"name": name}, response_model=AgentDetail
        )

    async def unlink(self, agent_id: int) -> None:
        """
        Unlinks (deletes) an agent.

        Args:
            agent_id: The unique ID of the agent to unlink.
        """
        await self._delete(f"/{scrub(agent_id)}")
