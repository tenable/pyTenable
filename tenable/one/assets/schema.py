from typing import Any, Optional
from enum import Enum
from pydantic import BaseModel


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


class Control(BaseModel):
    type: str
    multiple_allowed: bool
    regex: Optional[dict[str, Any]] = None
    selection: Optional[list[dict[str, Any]]] = None


class AssetField(BaseModel):
    key: str
    readable_name: str
    control: Control
    operators: list[str]
    sortable: bool
    filterable: bool
    weight: float
    object_types: list[AssetClass]
    description: str


class AssetProperties(BaseModel):
    asset_properties: dict[str, AssetField]
