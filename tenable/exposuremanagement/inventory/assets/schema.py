from typing import Any
from pydantic import BaseModel

from tenable.exposuremanagement.inventory.schema import AssetClass


class Asset(BaseModel):
    asset_id: str
    asset_class: AssetClass
    asset_name: str
    aes: int
    acr: int
    extra_properties: dict[str, Any]  # Supports arbitrary key-value pairs


class Assets(BaseModel):
    values: list[Asset]
    total_count: int
    offset: int
    limit: int
    sort_by: str
    sort_direction: str
