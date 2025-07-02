from typing import Any, Optional
from enum import Enum
from pydantic import BaseModel


class Operator(Enum):
    EQUAL = "="
    NOT_EQUAL = "!="
    CONTAINS = "contains"
    NOT_CONTAINS = "not contains"
    EXISTS = "exists"
    NOT_EXISTS = "not exists"
    LOWER_THAN = "<"
    LOWER_OR_EQUALS = "<="
    GREATER_THAN = ">"
    GREATER_OR_EQUALS = ">="
    OLDER_THAN = "older than"
    NEWER_THAN = "newer than"
    WITHIN_LAST = "within last"
    BETWEEN = "between"


class QueryMode(Enum):
    SIMPLE = "simple"
    ADVANCED = "advanced"


class PropertyFilter(BaseModel):
    property: str
    operator: Operator
    value: list[str]


class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"


class AssetClass(Enum):
    IAC = "IAC"
    STORAGE = "STORAGE"
    DEVICE = "DEVICE"
    APPLICATION = "APPLICATION"
    GENERAL = "GENERAL"
    CONTAINER = "CONTAINER"
    ACCOUNT = "ACCOUNT"
    RESOURCE = "RESOURCE"
    IDENTITY = "IDENTITY"
    ROLE = "ROLE"
    GROUP = "GROUP"
    UNKNOWN = "UNKNOWN"


class ControlType(Enum):
    STRING = "STRING"
    NUMBER = "NUMBER"
    DATE = "DATE"
    BOOLEAN = "BOOLEAN"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"


class SelectionControl(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    deprecated: Optional[bool] = None
    third_party: Optional[bool] = None


class Control(BaseModel):
    type: ControlType
    multiple_allowed: bool
    regex: Optional[dict[str, Any]] = None
    selection: Optional[list[SelectionControl]] = None


class Field(BaseModel):
    key: str
    readable_name: str
    control: Control
    operators: list[Operator]
    sortable: bool
    filterable: bool
    description: str


class Properties(BaseModel):
    data: list[Field]


class Sort(BaseModel):
    name: str
    order: SortDirection


class Pagination(BaseModel):
    total: int
    offset: int
    limit: int
    sort: Sort
