from typing import Any

from pydantic import BaseModel


class WeaknessSeverityCounts(BaseModel):
    low: int
    medium: int
    high: int
    critical: int
    total: int


class Tag(BaseModel):
    id: str
    name: str
    product: str
    asset_count: int
    weakness_severity_counts: WeaknessSeverityCounts
    total_weakness_count: int
    tag: str
    extra_properties: dict[str, Any]  # Supports arbitrary key-value pairs


class Tags(BaseModel):
    values: list[Tag]
    total_count: int
    offset: int
    limit: int
    sort_by: str
    sort_direction: str
