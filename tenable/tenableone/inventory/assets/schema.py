from typing import Any
from pydantic import BaseModel

from tenable.tenableone.inventory.schema import AssetClass, Pagination


class Asset(BaseModel):
    id: str
    asset_class: AssetClass
    name: str
    aes: int
    acr: int
    extra_properties: dict[str, Any]  # Supports arbitrary key-value pairs


class Assets(BaseModel):
    data: list[Asset]
    pagination: Pagination
