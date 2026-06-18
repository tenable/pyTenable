from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import Field, model_serializer, model_validator

from tenable.cloud._common import BaseModel


class ActivityLogFilter(BaseModel):
    field: str
    operator: Literal["lt", "lte", "eq", "gte", "gt"]
    value: str

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        """Attempts to coerce the data into the appropriate format"""

        # For the format: field.operator:value
        if isinstance(data, str):
            try:
                field, rest = data.split(".")
                operator, value = rest.split(":")
            except ValueError:
                raise ValueError(f"{data} is not in a valid filter format.") from None
            else:
                return {"field": field, "operator": operator, "value": value}

        # For the format: (field, operator, value)
        elif isinstance(data, tuple) and len(data) == 3:
            return {"field": data[0], "operator": data[1], "value": data[2]}
        return data

    @model_serializer(mode="plain")
    def serialize_model(self) -> str:
        """Returns the API expected string"""
        return f"{self.field}.{self.operator}:{self.value}"


class ActivityLogSort(BaseModel):
    field: str
    direction: Literal["asc", "desc"]

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        """Attempts to coerce the data into the appropriate format"""
        if isinstance(data, str):
            try:
                field, direction = data.split(":")
            except ValueError:
                raise ValueError(f"{data} is not in a valid sort format.") from None
            else:
                return {"field": field, "direction": direction}
        elif isinstance(data, tuple) and len(data) == 2:
            return {"field": data[0], "direction": data[1]}
        return data

    @model_serializer(mode="plain")
    def serialize_model(self) -> str:
        return f"{self.field}:{self.direction}"


class ActivityLogQueryParams(BaseModel):
    filters: Annotated[list[ActivityLogFilter] | None, Field(alias="f")] = None
    filter_type: Annotated[Literal["and", "or"] | None, Field(alias="ft")] = None
    limit: Annotated[int, Field(gt=0, lt=501)] | None = None
    next: str | None = None
    sort: ActivityLogSort | None = None


class ActivityLogActor(BaseModel):
    id: UUID | None
    name: str | None


class ActivityLogTarget(BaseModel):
    id: str | None = None
    name: str | None = None
    type: str | None = None


class ActivityLogField(BaseModel):
    key: str
    value: str


class ActivityLogEvent(BaseModel):
    """
    Activity Log Event
    """

    id: str
    action: str
    crud: str
    actor: ActivityLogActor
    target: ActivityLogTarget
    description: str | None = None
    is_anonymous: bool | None = None
    is_failure: bool | None = None
    fields: list[ActivityLogField] | None = None
    received: datetime


class ActivityLogPagination(BaseModel):
    offset: int
    limit: int
    count: int
    total: int
    next: str | None = None


class ActivityLogResponse(BaseModel):
    pagination: ActivityLogPagination
    events: list[ActivityLogEvent]
