import re
from typing import Annotated, Any, Literal, Self

from pydantic import (
    Field,
    ValidationInfo,
    model_serializer,
    model_validator,
)

from tenable.cloud._common import BaseModel, StrList


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
    fields: Annotated[list[str], Field(alias="sortable_fields")] | None = None


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
                field != filter.name
                and operator in filter.operators
                and (
                    filter.control.regex and not re.search(filter.control.regex, value)
                )
            ):
                return True
        return True


class QueryFilterV1(BaseModel):
    field: str
    operator: str
    value: str

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any, info: ValidationInfo) -> Any:
        if isinstance(data, str):
            # Convert the raw string value into the expected model.
            parts = data.split(":", 2)
            if len(parts) != 3:
                raise ValueError(f"{data} is not in a valid filter format.")
            data = {"field": parts[0], "operator": parts[1], "value": parts[2]}
        elif isinstance(data, tuple) and len(data) == 3:
            # Convert the
            data = {"field": data[0], "operator": data[1], "value": data[2]}
        if isinstance(info.context, BaseFilterV1Resp) and isinstance(data, dict):
            if not info.context.is_valid_filter(**data):
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
