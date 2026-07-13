from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import (
    BeforeValidator,
    Field,
    WrapSerializer,
    model_serializer,
    model_validator,
)

from tenable.cloud._common import (
    TIMEZONES,
    APIModel,
    BaseModel,
    PaginationV1,
    StrList,
    ser_list_to_str,
    val_str_to_list,
)

HealthState = Literal["HEALTHY", "WARNING", "CRITICAL", "SAFE MODE", "UNKNOWN"]
RRuleFreq = Literal["ONETIME", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]
WeekDays = Annotated[
    list[Literal["SU", "MO", "TU", "WE", "TH", "FR", "SA"]],
    BeforeValidator(val_str_to_list),
    WrapSerializer(ser_list_to_str),
]


class AgentFilter(BaseModel):
    field: str
    operator: str
    value: str

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        if isinstance(data, str):
            parts = data.split(":", 2)
            if len(parts) != 3:
                raise ValueError(f"{data} is not in a valid filter format.")
            return {"field": parts[0], "operator": parts[1], "value": parts[2]}
        elif isinstance(data, tuple) and len(data) == 3:
            return {"field": data[0], "operator": data[1], "value": data[2]}
        return data

    @model_serializer(mode="plain")
    def serialize_model(self) -> str:
        return f"{self.field}:{self.operator}:{self.value}"


class AgentQueryParams(BaseModel):
    filters: Annotated[list[AgentFilter] | None, Field(alias="f")] = None
    filter_type: Annotated[Literal["and", "or"] | None, Field(alias="ft")] = None
    wildcard: Annotated[str | None, Field(alias="w")] = None
    wildcard_fields: Annotated[StrList | None, Field(alias="wf")] = None
    limit: int | None = None
    offset: int | None = None
    sort: str | None = None


class AgentGroupRef(BaseModel):
    id: int
    name: str


class AgentRemoteSettingValue(BaseModel):
    value: str
    label: str | None = None


class AgentRemoteSetting(BaseModel):
    name: str
    setting: str
    type: str
    description: str | None = None
    min: int | None = None
    max: int | None = None
    backend_reload: bool | None = None
    service_restart: bool | None = None
    status: str | None = None
    value: str | None = None
    allowable_values: list[AgentRemoteSettingValue] | None = None
    default: str | None = None


class AgentHealthEvent(BaseModel):
    identifier: int
    state: int
    state_time: int
    details: str | None = None
    previous_details: str | None = None
    muted: bool | None = None
    state_name: str | None = None
    identifier_name: str | None = None
    previous_state_name: str | None = None


class Agent(APIModel):
    __api_path__ = "/scanners/null/agents/{model.uuid}"
    __api_save_request_model_kwargs__ = {"include": ["name"]}
    __api_save_method__ = "PATCH"

    id: int
    uuid: str
    name: str
    platform: str
    distro: str | None = None
    ip: str | None = None
    last_scanned: datetime | None = None
    plugin_feed_id: str | None = None
    core_build: str | None = None
    core_version: str | None = None
    linked_on: datetime | None = None
    last_connect: datetime | None = None
    status: Literal["on", "off", "init"] | None = None
    groups: list[AgentGroupRef] | None = None
    supports_remote_logs: bool | None = None
    network_uuid: str | None = None
    network_name: str | None = None
    profile_uuid: str | None = None
    profile_name: str | None = None
    supports_remote_settings: bool | None = None
    asset_uuid: str | None = None
    health: int | None = None
    health_state_name: str | None = None
    fredi_status: bool | None = None


class AgentDetail(Agent):
    remote_settings: list[AgentRemoteSetting] | None = None
    restart_pending: bool | None = None
    health_events: list[AgentHealthEvent] | None = None


class AgentListResponse(BaseModel):
    agents: list[Agent]
    pagination: PaginationV1


class AgentConfigUnlink(BaseModel):
    enabled: bool
    expiration: int | None = None


class AgentConfigConcurrency(BaseModel):
    enabled: bool
    max_agents: Annotated[int, Field(alias="max_concurrent_update")]


class AgentConfig(APIModel):
    __api_path__ = "/scanners/null/agents/config"

    auto_unlink: AgentConfigUnlink
    concurrent_update: AgentConfigConcurrency
    software_update: bool
    hybrid_scanning: Annotated[bool, Field(alias="hybrid_scanning_enabled")]


class RecurrenceRule(BaseModel):
    frequency: Annotated[
        Literal["ONETIME", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"], Field(alias="freq")
    ]
    interval: int | None = None
    by_weekday: Annotated[WeekDays, Field(alias="byweekday")]
    by_monthday: Annotated[int, Field(alias="bymonthday")]


class AgentSchedule(BaseModel):
    enabled: bool = False
    start_time: datetime | None = None
    end_time: datetime | None = None
    rrules: RecurrenceRule | None = None
    timezone: TIMEZONES | None = None


class AgentExclusionCreate(BaseModel):
    name: str
    description: str | None = None
    schedule: AgentSchedule | None = AgentSchedule(enabled=False)


class AgentExclusion(APIModel):
    __api_path__ = "/scanners/null/agents/exclusions/{model.id}"
    __api_save_request_model_kwargs__ = {"include": ["name", "description", "schedule"]}

    uuid: UUID
    id: int
    name: str
    description: str | None = None
    created_on: Annotated[datetime, Field(alias="creation_date")]
    modified_on: Annotated[datetime, Field(alias="last_modification_date")]
    core_updates_blocked: bool
    schedule: AgentSchedule


class AgentExclusionListResponse(BaseModel):
    exclusions: list[AgentExclusion]


class AgentGroup(APIModel):
    __api_path__ = "/scanners/null/agent-groups/{model.id}"
    __api_save_request_model_kwargs__ = {"include": ["name"]}

    id: int
    uuid: UUID
    name: str
    owner: str
    owner_id: int | None = None
    owner_name: str
    owner_uuid: UUID
    user_permissions: int
    agents_count: int
    agents: list[Agent]
    created_on: Annotated[datetime, Field(alias="creation_date")]
    modified_on: Annotated[datetime, Field(alias="last_modification_date")]

    def _agent_group_agent_path(self, agent_id: UUID) -> str:
        return f"{self.__api_path__.format(model=self)}/agents/{agent_id}"

    def add_agent(self, agent_id: UUID) -> None:
        self.__api_client__._put(self._agent_group_agent_path(agent_id))

    def remove_agent(self, agent_id: UUID) -> None:
        self.__api_client__._delete(self._agent_group_agent_path(agent_id))

    async def async_add_agent(self, agent_id: UUID) -> None:
        await self.__api_client__._put(self._agent_group_agent_path(agent_id))

    async def async_remove_agent(self, agent_id: UUID) -> None:
        await self.__api_client__._delete(self._agent_group_agent_path(agent_id))


class AgentGroupListResponse(BaseModel):
    groups: list[AgentGroup]


class AgentTask(BaseModel):
    id: Annotated[UUID, Field(alias="task_id")]
    container_uuid: UUID
    status: Literal["NEW", "RUNNING", "COMPLETED", "FAILED", "STALE"]
    message: str
    start_time: datetime
    end_time: datetime
    last_update_time: datetime
    total_work_units: int
    total_work_units_completed: int
    completion_percentage: int


class AgentGroupTask(BaseModel):
    group_uuid: int | UUID


class BulkAgentCriteria(BaseModel):
    all_agents: bool = True
    wildcard: str | None = None
    filters: list[AgentFilter]
    filter_type: Literal["and", "or"] = "and"
    hardcoded_filters: list[AgentFilter] | None = None


class BulkAgentQuery(BaseModel):
    criteria: BulkAgentCriteria | None = None
    items: list[int] | list[UUID] | None = None
    not_items: list[int] | list[UUID] | None = None
