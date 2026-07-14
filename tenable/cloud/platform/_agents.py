from typing import Literal
from uuid import UUID

from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.utils import scrub

from .iterators import AsyncPaginationV1Iterator, PaginationV1Iterator
from .models.agents import (
    Agent,
    AgentConfig,
    AgentDetail,
    AgentDirective,
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
    BulkAgentCriteria,
    BulkAgentDirectiveQuery,
    BulkAgentNetworkQuery,
    BulkAgentProfileQuery,
    BulkAgentQuery,
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
        return self._post(response_model=AgentGroup, json={"name": name})

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

    def get(self) -> list[AgentGroup]:
        """
        Gets the list of agent groups.

        Returns:
            List of agent group objects.
        """
        resp = self._get(response_model=AgentGroupListResponse)
        return resp.groups

    def details(self, id: int | UUID) -> AgentGroup:
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


class AsyncAgentExclusionAPI(AsyncAPIEndpoint):
    _path = "/scanners/null/agents/exclusions"

    async def create(
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
        return await self._post(
            response_model=AgentExclusion,
            json=AgentExclusionCreate(
                name=name, description=description, schedule=schedule
            ),
        )

    async def update(
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
        excl = await self.details(id)
        updated = AgentExclusionCreate(
            name=name if name is not None else excl.name,
            description=description if description is not None else excl.description,
            schedule=schedule if schedule is not None else excl.schedule,
        )
        return await self._put(
            f"/{scrub(id)}", json=updated, response_model=AgentExclusion
        )

    async def delete(self, id: int | UUID) -> None:
        """
        Deletes the specified agent exclusion.

        Args:
            id: Unique ID of the exclusion object to delete.
        """
        await self._delete(f"/{scrub(id)}")

    async def get(self) -> list[AgentExclusion]:
        """
        Gets the list of agent exclusions.

        Returns:
            List of exclusion objects.
        """
        resp = await self._get(response_model=AgentExclusionListResponse)
        return resp.exclusions

    async def details(self, id: int | UUID) -> AgentExclusion:
        """
        Gets the details for the specific agent exclusion.

        Args:
            id: Unique id of the exclusion object to retrieve.

        Returns:
            Requested exclusion object.
        """
        return await self._get(f"/{scrub(id)}", response_model=AgentExclusion)


class AsyncAgentGroupsAPI(AsyncAPIEndpoint):
    _path = "/scanners/null/agent-groups"

    async def create(self, name: str) -> AgentGroup:
        """
        Creates a new Agent group

        Args:
            name: The name of the new group.

        Returns:
            Created agent group object.
        """
        return await self._post(response_model=AgentGroup, json={"name": name})

    async def update(self, id: int | UUID, *, name: str) -> AgentGroup:
        """
        Updates an existing agent group object

        Args:
            id: Unique ID of the group object to edit.
            name: New name of the group.

        Returns:
            Updated agent group object.
        """
        return await self._put(
            f"/{scrub(id)}", json={"name": name}, response_model=AgentGroup
        )

    async def delete(self, id: int | UUID) -> None:
        """
        Deletes the specified agent group.

        Args:
            id: Unique ID of the agent group object to delete.
        """
        await self._delete(f"/{scrub(id)}")

    async def get(self) -> list[AgentGroup]:
        """
        Gets the list of agent groups.

        Returns:
            List of agent group objects.
        """
        resp = await self._get(response_model=AgentGroupListResponse)
        return resp.groups

    async def details(self, id: int | UUID) -> AgentGroup:
        """
        Gets the details for the specific agent group.

        Args:
            id: Unique id of the agent group object to retrieve.

        Returns:
            Requested agent group object.
        """
        return await self._get(f"/{scrub(id)}", response_model=AgentGroup)

    async def add(self, group_id: int | UUID, agent_id: int | UUID) -> None:
        """
        Adds an agent to the agent group.

        Args:
            group_id: Agent Group ID
            agent_id: Agent ID
        """
        await self._put(f"/{scrub(group_id)}/agents/{scrub(agent_id)}")

    async def remove(self, group_id: int | UUID, agent_id: int | UUID) -> None:
        """
        Removes an agent from the agent group.

        Args:
            group_id: Agent Group ID
            agent_id: Agent ID
        """
        await self._delete(f"/{scrub(group_id)}/agents/{scrub(agent_id)}")


class AgentTasksAPI(APIEndpoint):
    _path = "/scanners/null"

    def task_status(self, task_uuid: UUID | str) -> AgentTask:
        """
        Returns the status of a bulk agent task.

        Args:
            task_uuid: The UUID of the task to check.

        Returns:
            Current status of the specified task.
        """
        return self._get(f"/agents/_bulk/{scrub(task_uuid)}", response_model=AgentTask)

    def group_task_status(
        self, group_id: int | UUID, task_uuid: UUID | str
    ) -> AgentTask:
        """
        Returns the status of a bulk agent group task.

        Args:
            group_id: The ID of the agent group.
            task_uuid: The UUID of the task to check.

        Returns:
            Current status of the specified task.
        """
        return self._get(
            f"/agent-groups/{scrub(group_id)}/agents/_bulk/{scrub(task_uuid)}",
            response_model=AgentTask,
        )

    def add_to_group(
        self,
        group_id: int | UUID,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-adds agents to an agent group.

        Args:
            group_id: The ID of the agent group.
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return self._post(
            f"/agent-groups/{scrub(group_id)}/agents/_bulk/add",
            json=BulkAgentQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
            ),
            response_model=AgentTask,
        )

    def remove_from_group(
        self,
        group_id: int | UUID,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-removes agents from an agent group.

        Args:
            group_id: The ID of the agent group.
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return self._post(
            f"/agent-groups/{scrub(group_id)}/agents/_bulk/remove",
            json=BulkAgentQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
            ),
            response_model=AgentTask,
        )

    def add_to_network(
        self,
        network_uuid: UUID | str,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-adds agents to a network.

        Args:
            network_uuid: The UUID of the network to add agents to.
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return self._post(
            "/agents/_bulk/addToNetwork",
            json=BulkAgentNetworkQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
                network_uuid=str(network_uuid),
            ),
            response_model=AgentTask,
        )

    def remove_from_network(
        self,
        network_uuid: UUID | str,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-removes agents from a network.

        Args:
            network_uuid: The UUID of the network to remove agents from.
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return self._post(
            "/agents/_bulk/removeFromNetwork",
            json=BulkAgentNetworkQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
                network_uuid=str(network_uuid),
            ),
            response_model=AgentTask,
        )

    def assign_to_profile(
        self,
        profile_uuid: UUID | str | None = None,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-assigns agents to an agent profile, or removes agents from their
        current profile when ``profile_uuid`` is ``None``.

        Args:
            profile_uuid:
                The UUID of the profile to assign. Pass ``None`` to remove
                agents from their current profile.
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return self._post(
            "/agents/_bulk/assignToProfile",
            json=BulkAgentProfileQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
                profile_uuid=str(profile_uuid) if profile_uuid is not None else None,
            ),
            response_model=AgentTask,
        )

    def send_directive(
        self,
        directive: AgentDirective,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Sends a bulk directive (restart or settings change) to agents.

        Args:
            directive:
                An :class:`~.models.AgentDirective` describing the instruction
                to send (``type="restart"`` or ``type="settings"``).
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return self._post(
            "/agents/_bulk/directive",
            json=BulkAgentDirectiveQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
                directive=directive,
            ),
            response_model=AgentTask,
        )

    def send_group_directive(
        self,
        group_id: int | UUID,
        directive: AgentDirective,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Sends a bulk directive (restart or settings change) to agents in a group.

        Args:
            group_id: The ID of the agent group.
            directive:
                An :class:`~.models.AgentDirective` describing the instruction
                to send (``type="restart"`` or ``type="settings"``).
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return self._post(
            f"/agent-groups/{scrub(group_id)}/agents/_bulk/directive",
            json=BulkAgentDirectiveQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
                directive=directive,
            ),
            response_model=AgentTask,
        )

    def unlink_many(
        self,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-unlinks (deletes) agents.

        Args:
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return self._post(
            "/agents/_bulk/unlink",
            json=BulkAgentQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
            ),
            response_model=AgentTask,
        )


class AsyncAgentTasksAPI(AsyncAPIEndpoint):
    _path = "/scanners/null"

    async def task_status(self, task_uuid: UUID | str) -> AgentTask:
        """
        Returns the status of a bulk agent task.

        Args:
            task_uuid: The UUID of the task to check.

        Returns:
            Current status of the task.
        """
        return await self._get(
            f"/agents/_bulk/{scrub(task_uuid)}", response_model=AgentTask
        )

    async def group_task_status(
        self, group_id: int | UUID, task_uuid: UUID | str
    ) -> AgentTask:
        """
        Returns the status of a bulk agent group task.

        Args:
            group_id: The ID of the agent group.
            task_uuid: The UUID of the task to check.

        Returns:
            Current status of the task.
        """
        return await self._get(
            f"/agent-groups/{scrub(group_id)}/agents/_bulk/{scrub(task_uuid)}",
            response_model=AgentTask,
        )

    async def add_to_group(
        self,
        group_id: int | UUID,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-adds agents to an agent group.

        Args:
            group_id: The ID of the agent group.
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return await self._post(
            f"/agent-groups/{scrub(group_id)}/agents/_bulk/add",
            json=BulkAgentQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
            ),
            response_model=AgentTask,
        )

    async def remove_from_group(
        self,
        group_id: int | UUID,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-removes agents from an agent group.

        Args:
            group_id: The ID of the agent group.
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return await self._post(
            f"/agent-groups/{scrub(group_id)}/agents/_bulk/remove",
            json=BulkAgentQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
            ),
            response_model=AgentTask,
        )

    async def add_to_network(
        self,
        network_uuid: UUID | str,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-adds agents to a network.

        Args:
            network_uuid: The UUID of the network to add agents to.
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return await self._post(
            "/agents/_bulk/addToNetwork",
            json=BulkAgentNetworkQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
                network_uuid=str(network_uuid),
            ),
            response_model=AgentTask,
        )

    async def remove_from_network(
        self,
        network_uuid: UUID | str,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-removes agents from a network.

        Args:
            network_uuid: The UUID of the network to remove agents from.
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return await self._post(
            "/agents/_bulk/removeFromNetwork",
            json=BulkAgentNetworkQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
                network_uuid=str(network_uuid),
            ),
            response_model=AgentTask,
        )

    async def assign_to_profile(
        self,
        profile_uuid: UUID | str | None = None,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-assigns agents to an agent profile, or removes agents from their
        current profile when ``profile_uuid`` is ``None``.

        Args:
            profile_uuid:
                The UUID of the profile to assign. Pass ``None`` to remove
                agents from their current profile.
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return await self._post(
            "/agents/_bulk/assignToProfile",
            json=BulkAgentProfileQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
                profile_uuid=str(profile_uuid) if profile_uuid is not None else None,
            ),
            response_model=AgentTask,
        )

    async def send_directive(
        self,
        directive: AgentDirective,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Sends a bulk directive (restart or settings change) to agents.

        Args:
            directive:
                An :class:`~.models.AgentDirective` describing the instruction
                to send (``type="restart"`` or ``type="settings"``).
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return await self._post(
            "/agents/_bulk/directive",
            json=BulkAgentDirectiveQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
                directive=directive,
            ),
            response_model=AgentTask,
        )

    async def send_group_directive(
        self,
        group_id: int | UUID,
        directive: AgentDirective,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Sends a bulk directive (restart or settings change) to agents in a group.

        Args:
            group_id: The ID of the agent group.
            directive:
                An :class:`~.models.AgentDirective` describing the instruction
                to send (``type="restart"`` or ``type="settings"``).
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return await self._post(
            f"/agent-groups/{scrub(group_id)}/agents/_bulk/directive",
            json=BulkAgentDirectiveQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
                directive=directive,
            ),
            response_model=AgentTask,
        )

    async def unlink_many(
        self,
        *,
        all_agents: bool = True,
        filters: list[str | AgentFilter] | None = None,
        filter_type: Literal["and", "or"] = "and",
        wildcard: str | None = None,
        hardcoded_filters: list[str | AgentFilter] | None = None,
        items: list[int | UUID] | None = None,
        not_items: list[int | UUID] | None = None,
    ) -> AgentTask:
        """
        Bulk-unlinks (deletes) agents.

        Args:
            all_agents: Match all agents when building criteria.
            filters:
                List of filters in ``field:operator:value`` format or as
                :class:`AgentFilter` objects.
            filter_type: Combine filters with ``and`` or ``or``.
            wildcard: Free-text wildcard search string.
            hardcoded_filters: Additional filters always combined with ``and``.
            items: Agent IDs or UUIDs to include.
            not_items: Agent IDs or UUIDs to exclude.

        Returns:
            Task object for tracking the bulk operation.
        """
        return await self._post(
            "/agents/_bulk/unlink",
            json=BulkAgentQuery(
                criteria=BulkAgentCriteria(
                    all_agents=all_agents,
                    wildcard=wildcard,
                    filters=filters,  # type: ignore[arg-type]
                    filter_type=filter_type,
                    hardcoded_filters=hardcoded_filters,  # type: ignore[arg-type]
                ),
                items=items,
                not_items=not_items,
            ),
            response_model=AgentTask,
        )


class AgentsAPI(APIEndpoint):
    _path = "/scanners/null/agents"

    exclusions: AgentExclusionAPI
    groups: AgentGroupsAPI
    tasks: AgentTasksAPI

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
            Iterator yielding agent objects.
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
            context={"filters": schema},
        )
        return AgentsIterator(self._client, path=path, params=params)

    def details(self, agent_id: int | UUID | str) -> AgentDetail:
        """
        Returns details for the specified agent.

        Args:
            agent_id: The unique ID of the agent.

        Returns:
            Specified agent details.
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

    exclusions: AsyncAgentExclusionAPI
    groups: AsyncAgentGroupsAPI
    tasks: AsyncAgentTasksAPI

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
            Async iterator yielding agent objects.
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
            Specified agent details.
        """
        return await self._get(f"/{scrub(agent_id)}", response_model=AgentDetail)

    async def rename(self, agent_id: int | UUID | str, name: str) -> AgentDetail:
        """
        Renames an agent.

        Args:
            agent_id: The ID or UUID of the agent to rename.
            name: The new name for the agent.

        Returns:
            Updated details for the agent.
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
