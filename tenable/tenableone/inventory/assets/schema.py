from typing import Any
from pydantic import BaseModel

from tenable.tenableone.inventory.schema import AssetClass


class Asset(BaseModel):
    id: str
    asset_class: AssetClass
    name: str
    aes: int
    acr: int
    extra_properties: dict[str, Any]  # Supports arbitrary key-value pairs


class Assets(BaseModel):
    data: list[Asset]
    pagination: dict[str, Any]
    sort_by: str
    sort_direction: str
