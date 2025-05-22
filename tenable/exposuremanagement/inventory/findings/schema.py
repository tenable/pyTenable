from enum import StrEnum
from typing import Any, Literal
from uuid import UUID

from pydantic import PositiveInt, NonNegativeInt

from tenable.io.sync.models.common import BaseModel

class FindingSeverity(StrEnum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class FindingState(StrEnum):
    ACTIVE = "ACTIVE"
    RESURFACED = "RESURFACED"
    FIXED = "FIXED"

class Finding(BaseModel):
    id: UUID
    finding_name: str
    severity: FindingSeverity
    state: FindingState
    asset_id: UUID
    extra_properties: dict[str, Any] | None = None

class Findings(BaseModel):
    values: list[Finding]
    total_count: NonNegativeInt
    offset: NonNegativeInt
    limit: PositiveInt
    sort_by: str
    sort_direction: Literal["asc", "desc"]
