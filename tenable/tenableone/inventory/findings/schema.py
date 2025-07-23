from enum import Enum
from typing import Any
from uuid import UUID


from pydantic import BaseModel
from tenable.tenableone.inventory.schema import Pagination


class FindingSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class FindingState(str, Enum):
    ACTIVE = "ACTIVE"
    RESURFACED = "RESURFACED"
    FIXED = "FIXED"

class Finding(BaseModel):
    id: UUID
    name: str
    severity: FindingSeverity
    state: FindingState
    asset_id: UUID
    extra_properties: dict[str, Any] | None = None

class Findings(BaseModel):
    data: list[Finding]
    pagination: Pagination
