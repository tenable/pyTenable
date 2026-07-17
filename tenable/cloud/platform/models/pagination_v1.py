import re
from typing import Annotated, Any, Literal

from pydantic import (
    Field,
    ValidationInfo,
    model_serializer,
    model_validator,
)

from tenable.cloud._common import BaseModel, StrList


class SortObj(BaseModel):
    name: str
    order: Literal["asc", "desc"]


class PaginationV1(BaseModel):
    total: int
    offset: int
    limit: int
    sort: list[SortObj]


class PageV1Response(BaseModel):
    items: list[BaseModel]
    pagination: PaginationV1


class PaginationV1Query(BaseModel):
    limit: int
    offset: int = 0


class BaseFilterV1ItemControl(BaseModel):
    readable_regex: str | None = None
    type: str
    regex: str


class BaseFilterV1Item(BaseModel):
    name: str
    readable_name: str
    operators: list[str]
    control: BaseFilterV1ItemControl


class BaseFilterV1Sort(BaseModel):
    max_sort_fields: int
    fields: Annotated[list[str] | None, Field(alias="sortable_fields")] = None


class BaseFilterV1Resp(BaseModel):
    wildcards: Annotated[
        list[str], Field(alias="wildcard_fields", default_factory=list)
    ]
    sort: BaseFilterV1Sort
    filters: list[BaseFilterV1Item]

    def is_valid_filter(self, field: str, operator: str, value: str) -> bool:
        """
        Confirms whether the passed filter is valid against the current filter item.

        Args:
            field: Filter field name
            operator: Filter operator
            value: Filter value

        Returns:
            Boolean result if the filter is valid against the filter definition.
        """
        for filter in self.filters:
            if (
                field == filter.name
                and operator in filter.operators
                and (not filter.control.regex or re.search(filter.control.regex, value))
            ):
                return True
        return False


class QueryFilterV1(BaseModel):
    field: str
    operator: str
    value: str

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any, info: ValidationInfo) -> Any:
        filters = None
        if isinstance(info.context, dict):
            filters: BaseFilterV1Resp | None = info.context.get("filters")
        if isinstance(data, str):
            # Convert the raw string value into the expected model.
            parts = data.split(":", 2)
            if len(parts) != 3:
                raise ValueError(f"{data} is not in a valid filter format.")
            data = {"field": parts[0], "operator": parts[1], "value": parts[2]}
        elif isinstance(data, tuple) and len(data) == 3:
            # Convert the
            data = {"field": data[0], "operator": data[1], "value": data[2]}
        if isinstance(filters, BaseFilterV1Resp) and isinstance(data, dict):
            if not filters.is_valid_filter(**data):
                raise ValueError(f"{data} doesn't match any valid filter schemas.")
        return data

    @model_serializer(mode="plain")
    def serialize_model(self) -> str:
        return f"{self.field}:{self.operator}:{self.value}"


class QueryParamsV1(BaseModel):
    _filter_schema: BaseFilterV1Resp | None = None
    filters: Annotated[list[QueryFilterV1] | None, Field(alias="f")] = None
    filter_type: Annotated[Literal["and", "or"] | None, Field(alias="ft")] = None
    wildcard: Annotated[str | None, Field(alias="w")] = None
    wildcard_fields: Annotated[StrList | None, Field(alias="wf")] = None
    limit: int | None = None
    offset: int | None = None
    sort: str | None = None
