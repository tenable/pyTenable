from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from tenable.cloud._common import TIMEZONES, APIModel, BaseModel, StrList

from .agents import RRuleFreq, WeekDays
from .pagination_v1 import PaginationV1Query


class ExclusionRecurrenceRule(BaseModel):
    frequency: Annotated[RRuleFreq, Field(alias="freq")]
    interval: int | None = None
    by_weekday: Annotated[WeekDays | None, Field(alias="byweekday")] = None
    by_monthday: Annotated[int | None, Field(alias="bymonthday")] = None


class ExclusionSchedule(BaseModel):
    enabled: bool = False
    start_time: Annotated[datetime | None, Field(alias="starttime")] = None
    end_time: Annotated[datetime | None, Field(alias="endtime")] = None
    rrules: ExclusionRecurrenceRule | None = None
    timezone: TIMEZONES | None = None


class ExclusionCreate(BaseModel):
    name: str
    members: StrList
    description: str | None = None
    schedule: ExclusionSchedule | None = ExclusionSchedule(enabled=False)
    network_id: UUID | None = None


class Exclusion(APIModel):
    __api_path__ = "/exclusions/{model.id}"
    __api_save_request_model_kwargs__ = {
        "include": ["name", "description", "members", "schedule", "network_id"]
    }

    uuid: UUID
    id: int
    name: str
    description: str | None = None
    members: StrList
    schedule: ExclusionSchedule
    network_id: UUID | None = None
    created_on: Annotated[datetime, Field(alias="creation_date")]
    modified_on: Annotated[datetime, Field(alias="last_modification_date")]


class ExclusionPagination(BaseModel):
    total: int
    limit: int
    offset: int
    sort: str | None = None


class ExclusionListResponse(BaseModel):
    items: Annotated[list[Exclusion], Field(validation_alias="exclusions")]
    pagination: ExclusionPagination


class ExclusionQueryParams(PaginationV1Query):
    sort: str | None = None
