from typing import Any
from pydantic import BaseModel

from tenable.inventory.schema import AssetClass


class Asset(BaseModel):
    id: str
    asset_class: AssetClass
    name: str
    aes: int
    acr: int
    additional_properties: dict[str, Any]  # Supports arbitrary key-value pairs


class Assets(BaseModel):
    values: list[Asset]
    total_count: int
