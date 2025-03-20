from typing import Any
from pydantic import BaseModel

from tenable.inventory.schema import AssetClass


class Software(BaseModel):
    id: str
    asset_class: AssetClass
    name: str
    aes: int
    acr: int
    additional_properties: dict[str, Any]  # Supports arbitrary key-value pairs


class SoftwareValues(BaseModel):
    values: list[Software]
    total_count: int
