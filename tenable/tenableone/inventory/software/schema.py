from enum import Enum
from typing import Any
from pydantic import BaseModel


class Part(Enum):
    APPLICATION = "APPLICATION"
    OPERATING_SYSTEM = "OPERATING_SYSTEM"
    HARDWARE = "HARDWARE"


class Software(BaseModel):
    application: str
    publisher: str
    type: list[Part]
    extra_properties: dict[str, Any]  # Supports arbitrary key-value pairs


class SoftwareValues(BaseModel):
    values: list[Software]
    total_count: int
    offset: int
    limit: int
    sort_by: str
    sort_direction: str
