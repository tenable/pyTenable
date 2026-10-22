import json
from datetime import date, datetime, timezone
from typing import Annotated, Any, Generic, Literal, TypeVar
from uuid import UUID

from pydantic import (
    AliasChoices,
    BeforeValidator,
    Field,
    PlainSerializer,
    RootModel,
    model_validator,
)

from tenable.cloud._common import BaseModel, StrList


def val_json_str(value: Any) -> Any:
    """Attempts to decode a JSON-encoded string, returning the raw string otherwise"""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return value
    return value


def ser_json_str(value: Any) -> str:
    """Encodes the value as a JSON string unless it's already a string"""
    return value if isinstance(value, str) else json.dumps(value)


JsonStr = Annotated[Any, BeforeValidator(val_json_str), PlainSerializer(ser_json_str)]
""" Handles fields that the API transmits as JSON-encoded strings """

UnixSeconds = Annotated[datetime, PlainSerializer(lambda v: int(v.timestamp()))]
""" A datetime that the API expects as a unix timestamp in seconds """

DueDateRule = Literal["byFixedDate", "withinNumberOfDays", "ongoing"]
""" Supported due date rules """


class RemediationDueDate(BaseModel):
    name: DueDateRule
    value: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        """
        Coerces the shorthand forms of the due date rule into the API format:

        * An integer is the number of days to complete within.
        * A date or datetime is the fixed completion date.
        * The string ``ongoing`` is an ongoing rule (remediation goals only).
        """
        if isinstance(data, bool):
            return data
        if isinstance(data, int):
            data = {"name": "withinNumberOfDays", "value": data}
        elif isinstance(data, date):
            data = {"name": "byFixedDate", "value": data}
        elif data == "ongoing":
            data = {"name": "ongoing"}
        if isinstance(data, dict):
            data = dict(data)
            value = data.get("value")
            if isinstance(value, datetime):
                value = value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            elif isinstance(value, date):
                value = value.strftime("%Y-%m-%dT00:00:00Z")
            elif isinstance(value, int):
                value = str(value)
            if value is not None:
                data["value"] = value
        return data


class RemediationSort(BaseModel):
    property: str
    order: Literal["asc", "desc"]

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        """Accepts the `property:order` string and `(property, order)` formats"""
        if isinstance(data, str):
            try:
                prop, order = data.split(":")
            except ValueError:
                raise ValueError(f"{data} is not in a valid sort format.") from None
            return {"property": prop, "order": order}
        elif isinstance(data, tuple) and len(data) == 2:
            return {"property": data[0], "order": data[1]}
        return data


class RemediationSearchRequest(BaseModel):
    filter: dict[str, Any] | None = None
    limit: Annotated[int | None, Field(ge=1)] = None
    next: str | None = None
    sort: list[RemediationSort] | None = None
    fields: StrList | None = None
    findings_type: Annotated[str | None, Field(alias="findingsType")] = None


class RemediationDetailsParams(BaseModel):
    findings_type: Annotated[str | None, Field(alias="findingsType")] = None


class RemediationPagination(BaseModel):
    next: str | None = None
    total: int | None = None


T = TypeVar("T")


class RemediationSearchResponse(BaseModel, Generic[T]):
    items: Annotated[
        list[T], Field(validation_alias=AliasChoices("remediations", "goals"))
    ]
    pagination: RemediationPagination


class RemediationRequest(BaseModel):
    name: str
    description: str | None = None
    type: str | None = None
    status: str | None = None
    start_date: Annotated[UnixSeconds | None, Field(alias="startdate")] = None
    asset_filters: Annotated[JsonStr | None, Field(alias="assetfilters")] = None
    finding_filters: Annotated[JsonStr | None, Field(alias="findingfilters")] = None


class RemediationProjectRequest(RemediationRequest):
    due_date: Annotated[RemediationDueDate | None, Field(alias="projectduedate")] = None
    assignees: Annotated[list[str] | None, Field(alias="assignee")] = None

    @model_validator(mode="after")
    def validate_due_date(self) -> "RemediationProjectRequest":
        if self.due_date and self.due_date.name == "ongoing":
            raise ValueError("Remediation projects don't support ongoing due dates.")
        return self


class RemediationGoalRequest(RemediationRequest):
    due_date: Annotated[RemediationDueDate | None, Field(alias="goalduedate")] = None
    minimum_percentage: Annotated[
        int | None,
        Field(alias="minimumpercentage", ge=0, le=100),
        PlainSerializer(str),
    ] = None
    conditions: JsonStr | None = None


class RemediationProjectDeleteRequest(BaseModel):
    operation: Literal["remove"] = "remove"
    project_ids: Annotated[list[UUID], Field(alias="projectuuids", min_length=1)]


class RemediationGoalDeleteRequest(BaseModel):
    operation: Literal["remove"] = "remove"
    goal_ids: Annotated[list[UUID], Field(alias="goaluuids", min_length=1)]


class Remediation(BaseModel):
    container_id: Annotated[UUID | None, Field(alias="containeruuid")] = None
    user_id: Annotated[UUID | None, Field(alias="useruuid")] = None
    name: str
    description: str | None = None
    type: str | None = None
    status: str | None = None
    # The search operation returns a summary value while the details operation
    # returns a JSON-encoded object.
    progress: JsonStr | None = None
    start_date: Annotated[datetime | None, Field(alias="startdate")] = None
    asset_filters: Annotated[JsonStr | None, Field(alias="assetfilters")] = None
    finding_filters: Annotated[JsonStr | None, Field(alias="findingfilters")] = None
    # The API returns these as millisecond-precision unix timestamps, which pydantic
    # will automatically detect and convert.
    created_at: Annotated[datetime | None, Field(alias="create_tstamp")] = None
    updated_at: Annotated[datetime | None, Field(alias="update_tstamp")] = None


class RemediationProject(Remediation):
    id: Annotated[UUID, Field(alias="projectuuid")]
    due_date: Annotated[RemediationDueDate | None, Field(alias="projectduedate")] = None
    assignees: Annotated[list[str], Field(alias="assignee")] = Field(
        default_factory=list
    )


class RemediationGoal(Remediation):
    id: Annotated[UUID, Field(alias="goaluuid")]
    due_date: Annotated[RemediationDueDate | None, Field(alias="goalduedate")] = None
    due_at: Annotated[datetime | None, Field(alias="duedate")] = None
    goal_result: Annotated[str | None, Field(alias="goalresult")] = None
    minimum_percentage: Annotated[int | None, Field(alias="minimumpercentage")] = None
    conditions: JsonStr | None = None
    dashboards: list[Any] = Field(default_factory=list)


class RemediationProjectDetailsResponse(RootModel[list[RemediationProject]]): ...


class RemediationGoalDetailsResponse(RootModel[list[RemediationGoal]]): ...
